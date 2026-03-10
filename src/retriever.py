from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from src.config import RETRIEVER_K, WEIGHTS, SEARCH_MODE
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import ParentDocumentRetriever
from langchain_core.stores import InMemoryStore

class CustomEnsembleRetriever:
    def __init__(self, retrievers: list, weights):
        self.retrievers = retrievers
        self.weights = weights

    def invoke(self, query):
        # 1. 分别让 BM25 和 Chroma 去找最相关的段落
        bm25_docs = self.retrievers[0].invoke(query)
        vector_docs = self.retrievers[1].invoke(query)
        
        # 2. RRF (倒数排序融合) 核心算法
        rrf_score = {}
        # 将两路检索的结果拿出来打分合并
        for weight, docs in zip(self.weights, [bm25_docs, vector_docs]):
            for rank, doc in enumerate(docs): #返还按照从高到低的，rank就是计数器
                content = doc.page_content #文本内容是key
                if content not in rrf_score: 
                    rrf_score[content] = {"score": 0, "doc": doc}
                # 已经存入的文本，直接进行再次打分，因为已经被一个retriever检索到了
                # rank越小越靠前，加的分越多；再乘上分配的权重
                rrf_score[content]["score"] += weight / (rank + 60)
        
        # 3. 把打完分的所有段落按分数从高到低排序
        sorted_results = sorted(rrf_score.values(), key=lambda x: x["score"], reverse=True)
        
       
        return [item["doc"] for item in sorted_results[:RETRIEVER_K]]

class VectorRetriever:
    @staticmethod
    def create_retriever(splits):
        #加载embedding模型，把切好的文本向量化储存
        print("Creating vector into ChromaDB")
        # 本地embadding
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        print("Dense Retriever is creating")
        vectorstore = Chroma.from_documents(
            documents=splits, 
            embedding=embeddings
        )
        vector_retriever = vectorstore.as_retriever(search_kwargs={"k": RETRIEVER_K})
        print("Sparse Retriever is creating")
        texts = [doc.page_content for doc in splits]
        metadatas = [doc.metadata for doc in splits]
        bm25_retriever = BM25Retriever.from_texts(
            texts=texts,
            metadatas=metadatas,
            # 英文特供：全部转小写，并按空格切分成完整的单词列表
            preprocess_func=lambda text: text.lower().split()
        )       
        bm25_retriever.k = RETRIEVER_K
        print("Combining Two Retrievers")
        
        rrf_retriever = CustomEnsembleRetriever(retrievers=[bm25_retriever, vector_retriever],weights = WEIGHTS)
        return rrf_retriever

    
    @staticmethod
    def combine(docs:list):
        #把检索到的文本和对应页数合并成一个字符串
        return "\n\n".join(f"[Page{doc.metadata.get('page', 'unknown')}text]: {doc.page_content}" for doc in docs)
    
class ParentChildRetriever:
    def create_retriever(parent_splitter, child_splitter,document):
        print("Creating Parent-Child Retriever with Hash Mapping")
        # 1. 创建父子块的哈希映射
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        print("Dense Retriever is creating")
        vectorstore = Chroma(embedding_function=embeddings, collection_name="doc_retrieval_filter_metadata")
        store = InMemoryStore()
        
        
        
        retriever = ParentDocumentRetriever(
                vectorstore=vectorstore,
                docstore=store,
                child_splitter=child_splitter,
                parent_splitter=parent_splitter,
                search_kwargs = {"k": RETRIEVER_K}
            
            )
        print("3. [Parent-Child] 正在内部切分、计算哈希并建立映射...")
        retriever.add_documents(documents=document)
        print("✅ 父子块哈希映射检索架构构建完成！\n")
        return retriever
    

    
    def combine(docs:list):
        #把检索到的文本和对应页数合并成一个字符串
        return "\n\n".join(f"[Page{doc.metadata.get('page', 'unknown')}text]: {doc.page_content}" for doc in docs)
    