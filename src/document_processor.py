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