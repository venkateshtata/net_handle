from langchain_community.tools.tavily_search import TavilySearchResults

def setup_tools(retriever_tool):
    """
    Initialize tools with clear descriptions of their purposes and inputs.

    Parameters:
    - `retriever_tool`: The retrieval tool for specific document queries.
    """
    tavily_tool = TavilySearchResults(
        max_results=5,
        description="Tool for searching the internet for the most relevant results. "
                    "Input: A search query as a string."
    )

    return {
        "retriever_tool": retriever_tool,
        "tavily_tool": tavily_tool
    }
