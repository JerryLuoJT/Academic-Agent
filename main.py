import os
import sys
from src.agent import HomeworkAgent

def main():
    
    
    # 1. 获取用户输入的 PDF 路径
    pdf_path = input("Input PDF Path:").strip()
    
    # 检查文件是否存在
    if not os.path.exists(pdf_path):
        print(f"\n Can't Find'{pdf_path}'")
        print("Check the file path.")
        sys.exit(1)
        
    # 2. 获取题目和具体要求
    question = input("\nQuestion:").strip()
    if not question:
        question = "请总结这篇文档的核心观点。" # 默认问题
        print(f"No input question. Using Default: {question}")
        
    requirements = input("\nRequirements: ").strip()
    if not requirements:
        requirements = "结构清晰，逻辑严密，必须引用原文内容。" # 默认要求
        print(f"No input requirements. Using Default: {requirements}")
    
    # 3. 启动核心逻辑
    try:
        print("\n 正在初始化 Agent.请稍候...")
        agent = HomeworkAgent(pdf_path)
        agent.solve(question, requirements)
    except Exception as e:
        print(f"\n 运行过程中出现错误: {e}")
        print(" 提示：请检查你的 .env 文件中是否正确配置了 GOOGLE_API_KEY，以及网络是否畅通。")

if __name__ == "__main__":
    main()