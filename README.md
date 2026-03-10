# 📚 Academic Agentic RAG: Dual-Engine Document Retrieval System 
# 学术级 Agentic RAG：双引擎文档检索系统

An advanced, highly precise Retrieval-Augmented Generation (RAG) system designed specifically for dense academic texts, complex reading comprehension (e.g., GRE passages), and multi-document synthesis. 
这是一个高级且极具精度的检索增强生成（RAG）系统，专为密集的学术文本、复杂的阅读理解（如 GRE 长难句）以及多文档交叉综合分析而设计。

Unlike standard RAG tutorials that struggle with the "Precision vs. Context" dilemma, this project implements a **Dual-Engine Architecture** featuring Hybrid Search (RRF) and Parent-Child (Small-to-Big) Hash Mapping.
不同于那些在“检索精度与上下文完整性”之间苦苦挣扎的普通 RAG 教程，本项目实现了**双引擎架构**，完美融合了混合检索（RRF）与父子块（Small-to-Big）哈希映射技术。

## ✨ Core Features | 核心功能

* **⚙️ Dual-Engine Architecture (Toggleable) | 双检索引擎架构 (一键切换)**
    Easily switch between retrieval strategies via `src/config.py` based on your query needs:
    通过 `src/config.py`，根据你的查询需求优雅地切换底层检索策略：
    * `parent_child`: Uses **Small-to-Big Retrieval**. Chunks documents into small pieces (e.g., 300 tokens) for highly precise vector matching, but seamlessly maps back to large parent blocks (e.g., 1200 tokens) via an in-memory hash store to provide the LLM with flawless, unbroken context.
      **父子块映射模式**：使用“由小到大”的检索逻辑。将文档切分为极小的子块（如 300 字）以实现极高精度的向量命中；同时通过内存哈希表瞬间映射回大型父块（如 1200 字），为大模型提供完美、无断层的上下文。
    * `hybrid`: Combines **Dense Vector Search** (semantic understanding) with **Sparse BM25 Search** (exact keyword matching), fused perfectly using the Reciprocal Rank Fusion (RRF) algorithm.
      **混合检索模式**：将稠密向量检索（语义理解）与稀疏 BM25 检索（精准关键词匹配）相结合，并通过倒数排序融合算法（RRF）实现完美的分数统合。


* **🧠 Local Embedding & Vector Store | 本地向量化与存储**
    Utilizes HuggingFace's `all-MiniLM-L6-v2` for rapid local embeddings and ChromaDB for persistent, high-dimensional vector storage.
    调用 HuggingFace 的 `all-MiniLM-L6-v2` 模型实现极速的本地文本向量化，并依靠 Chroma 向量数据库完成高维数据的持久化存储。

## 🛠️ Tech Stack | 技术栈

* **Framework:** LangChain (Core, Community, Classic)
* **Vector Database:** Chroma
* **Embeddings:** HuggingFace / Sentence Transformers
* **Sparse Retrieval:** Rank-BM25
* **Document Parsing:** PyPDF

## 🚀 Getting Started | 快速开始

### 1. Clone the Repository | 克隆仓库
```bash
git clone [https://github.com/yourusername/homework_agent.git](https://github.com/yourusername/homework_agent.git)
cd homework_agent
```
### 2. Set Up the Virtual Environment | 配置虚拟环境
It is highly recommended to run this project in an isolated virtual environment.
强烈建议在隔离的虚拟环境中运行此项目，避免依赖冲突。
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows use: .\.venv\Scripts\activate
```

### 3. Install Dependencies | 安装核心依赖
```bash
pip install -r requirements.txt
```
### 4. Configuration | 配置项目
1. Place your academic PDFs into the data/ directory. / 将你的学术 PDF 文献放入 data/ 文件夹。

2. Adjust your search strategy in src/config.py: / 在配置文件中设定你的检索引擎：
```python
# Choose your engine: "parent_child" OR "hybrid"
SEARCH_MODE = "parent_child"
```
3. Set up your .env file with your preferred LLM API keys. / 在 .env 文件中配置你调用大模型所需的 API 密钥。
### 5. Run the System | 启动系统
```python
python main.py
```
## 🧠 Why Parent-Child Retrieval? | 为什么选择父子块检索？
In complex academic texts, standard chunking often breaks the logical flow. If a chunk is too large, the vector search dilutes the specific details. If a chunk is too small, the LLM loses the overarching narrative.
在处理复杂的学术长难句时，标准的“一刀切”文本切分往往会破坏底层逻辑流。切得太大，向量搜索会稀释细节；切得太小，大模型又会丢失全局视野。

By decoupling the search layer (child chunks) from the generation layer (parent chunks), this system achieves surgical precision during retrieval while providing the LLM with a panoramic view of the context.
通过将**“检索层（子块）”与“生成层（父块）”**彻底解耦，本系统在检索阶段实现了外科手术级的精准打击，同时在生成阶段为大模型提供了全景式的上下文视野。
