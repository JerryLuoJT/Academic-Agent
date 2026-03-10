from langchain_core.prompts import ChatPromptTemplate

DRAFT_PLAN_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "你是一个严谨的学术助理。根据提供的参考资料，为用户的题目制定详细的答题大纲。大纲需明确划分段落，并标注计划引用哪些资料内容。不要直接写正文。用英文回答"),
    ("user", "参考资料:\n{context}\n\n题目: {question}\n特殊要求: {requirements}\n\n请输出答题计划：")
])

REVISE_PLAN_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "你是一个严谨的学术助理。请结合参考资料、原计划和用户的修改意见，重新输出更新后的完整大纲。用英文回答"),
    ("user", "参考资料:\n{context}\n\n题目: {question}\n当前计划: {plan}\n修改意见: {feedback}\n\n请输出更新后的答题计划：")
])

GENERATE_FINAL_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "你是一个严谨的学术助理。请严格按照确认的【答题计划】撰写最终答案。用英文回答\n\n"
               "【绝对规则】:\n"
               "1. 必须尽可能多地引用【参考资料】原文。\n"
               "2. 每次引用或化用，必须在句末使用括号标注来源（如：[第X页原文]）。\n"
               "3. 严禁编造资料外的信息。"),
    ("user", "参考资料:\n{context}\n\n题目: {question}\n要求: {requirements}\n\n确认的答题计划:\n{plan}\n\n请写出最终文章：")
])

TRANS_PROMPT =  ChatPromptTemplate.from_messages([
    ("system", "你是一个严谨的学术助理。请将以下答题计划翻译成中文，方便用户理解。"),
    ("user", "答题计划:\n{plan}\n\n请翻译成中文：")
])

EXTRACT_KEYWORD_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "你是一个专业的信息检索专家。你的任务是从用户的提问中提取出最核心的学术关键词，用于数据库检索。不要拓展原本的题目意思。\n"
               "【绝对规则】: 只输出关键词，用空格分隔。绝对不要输出任何前缀（如'关键词是'）、解释性文字或标点符号。用英文回答"),
    ("user", "{question}")
])