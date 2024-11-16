from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import PyPDFDirectoryLoader

def load_and_prepare_documents(file_path: str, chunk_size: int = 1000, chunk_overlap: int = 0):
    """Load and split documents into chunks."""
    loader = PyPDFDirectoryLoader(file_path)
    try:
        documents = loader.load()
    finally:
        # Explicit cleanup if needed
        del loader
    
    if not documents:
        raise ValueError(f"No documents found in the directory: {file_path}")
    
    text_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return text_splitter.split_documents(documents)
