import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# 模型配置
MODEL_NAME = "gemini-3-flash-preview" #免费版
TEMPERATURE = 0.2

# 文本切片配置
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150

# 检索配置
RETRIEVER_K = 5

# RRF权重：先sparse(bm25)后dense， 和为1
WEIGHTS = [0.2, 0.8]