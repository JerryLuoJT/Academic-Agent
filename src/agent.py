from src.document_processor import DocumentProcessor
from src.retriever import VectorRetriever
from src.chains import ChainManager

class HomeworkAgent:
    def __init__(self, file_path:str):
        #初始化pdf处理器，向量检索器，链
        split = DocumentProcessor.process_pdf(file_path)
        self.retriever = VectorRetriever.create_retriever(split)
        self.chains = ChainManager()
    
    def solve(self, question, requirement):
        #提取关键词-检索-生成方案-人工确认-生成答案
        print("\n--- 0. 正在提取关键词 ---")
        keyword_chain = self.chains.get_keyword_chain()
        keywords = keyword_chain.invoke({
            "question": question
        })
        print(f"提取到的关键词: {keywords}")

        print("\n--- 1. 正在检索资料并生成初始计划 ---")
        docs = self.retriever.invoke(keywords)
        # 把文档片段翻译成带页码的长字符串
        prepared = VectorRetriever.combine(docs)

        draft_chain = self.chains.get_draft_chain()
        current_plan = draft_chain.invoke({
            "context": prepared,
            "question": question,
            "requirements": requirement
        })
        translate_plan = self.chains.translate_chain()
        translate = translate_plan.invoke({
            "plan":current_plan
        })

        while True:
            print("\n================ 当前作业计划 ================\n")
            print(current_plan)
            print(translate)
            print("\n============================================\n")
            
            feedback = input("ANY Suggestion?(OR input ok and start writing final answer): ")
            
            if feedback.lower().strip() == 'ok':
                break
            else:
                print("\n--- 正在根据你的意见修改计划... ---")
                revise_chain = self.chains.get_revise_chain()
                current_plan = revise_chain.invoke({
                    "context": prepared,
                    "question": question,
                    "plan": current_plan,
                    "feedback": feedback
                })
                translate_revise = self.chains.translate_chain()
                translate = translate_revise.invoke({
                    "plan":current_plan
                })
        
        print("\n--- 2. 计划已确认，开始生成最终作业 ---")
        final_chain = self.chains.get_final_chain()
        final_answer = final_chain.invoke({
            "context": prepared,
            "question": question,
            "requirements": requirement,
            "plan": current_plan
        })
        print("\n================ 最终作业正文 ================\n")
        print(final_answer)
        print("\n============================================\n")

