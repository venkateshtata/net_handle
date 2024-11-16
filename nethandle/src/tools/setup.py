from langchain_community.tools.tavily_search import TavilySearchResults
from tools.retriever import create_knowledge_base


def setup_tools(health_documents, lifestyle_documents):
    """
    Initialize tools with clear descriptions of their purposes and inputs.

    Parameters:
    - `retriever_tool`: The retrieval tool for specific document queries.
    """
    health_retriever_tool = create_knowledge_base(
        health_documents,
        "HealthcareAgent",
        "retrieving medical document information for patients"
    )
    lifestyle_retriever_tool = create_knowledge_base(
        lifestyle_documents,
        "LifestyleAgent",
        "retrieving lifestyle, dietary, and wellness information for personalized recommendations"
    )

    tavily_tool = TavilySearchResults(
        max_results=5,
        description="Tool for searching the internet for the most relevant results. "
                    "Input: A search query as a string."
    )
    
    return {
        "health_retriever_tool": health_retriever_tool,
        "lifestyle_retriever_tool": lifestyle_retriever_tool,
        "tavily_tool": tavily_tool
    }
