from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.config import CHUNK_SIZE, CHUNK_OVERLAP

class DocumentProcessor:
    def process_pdf(file_path:str):
        print(f"Processing pdf:{file_path}")
        loader = PyPDFLoader(file_path)
        document = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, 
                                                       chunk_overlap=CHUNK_OVERLAP)
        split = text_splitter.split_documents(document)
        return split
    
    def parent_child_process(file_path:str):
        """切两遍，一遍大的是父块不进入向量库，一遍小的进入"""
        print(f"Processing pdf with Parent-Child Mapping:{file_path}")
        loader = PyPDFLoader(file_path)
        document = loader.load()
        parent_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, add_start_index=True)
        child_splitter = RecursiveCharacterTextSplitter(chunk_size=400, add_start_index=True)
        return parent_splitter,child_splitter,document
    