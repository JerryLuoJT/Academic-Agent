from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from src.config import MODEL_NAME, TEMPERATURE
from src.prompts import DRAFT_PLAN_PROMPT, REVISE_PLAN_PROMPT, GENERATE_FINAL_PROMPT,TRANS_PROMPT, EXTRACT_KEYWORD_PROMPT

class ChainManager:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model=MODEL_NAME, temperature=TEMPERATURE)
        self.parser = StrOutputParser()

    def get_draft_chain(self):
        return DRAFT_PLAN_PROMPT | self.llm | self.parser
    
    def get_keyword_chain(self):
        return EXTRACT_KEYWORD_PROMPT | self.llm | self.parser
    
    def translate_chain(self):
        # 计划翻译成中文，方便用户理解
        return TRANS_PROMPT | self.llm | self.parser

    def get_revise_chain(self):
        return REVISE_PLAN_PROMPT | self.llm | self.parser

    def get_final_chain(self):
        return GENERATE_FINAL_PROMPT | self.llm | self.parser