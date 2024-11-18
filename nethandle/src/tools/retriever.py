from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.tools.retriever import create_retriever_tool

def create_knowledge_base(documents, agent_name, agent_description):
    """
    Create a retriever tool from documents.
    
    Parameters:
    - `documents`: List of split documents loaded from the data source.
    - `agent_name`: Name of the agent using the tool.
    - `agent_description`: Description of the agent's scope and tool capabilities.
    """
    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(documents, embeddings)
    retriever = db.as_retriever()
    return create_retriever_tool(
        retriever,
        "Retriever",
        description=f"Tool for retrieving information about {agent_description}."
    )
