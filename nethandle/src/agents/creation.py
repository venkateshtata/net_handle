from langchain_core.messages import SystemMessage
from langgraph.prebuilt import create_react_agent


def create_agents(tools1, tools2, llm):
    """
    Create specific agents with access to their respective tools.

    Parameters:
    - `tools1`: Tools for the HealthcareAgent.
    - `tools2`: Tools for the LifestyleAgent.
    - `llm`: The core LLM model driving the agents.
    """
    health_prompt = """
    Given the user's health records and prompts, provide insights into medication side effects, usage instructions, or potential conflicts. 
    Trigger alerts for:
    - Medication conflicts.
    - Change in prescription.
    - Scheduling reminders.
    """
    lifestyle_prompt = """
    Based on the user's lifestyle preferences, suggest:
    - Best offers or prices for medications or wellness products.
    - Alternative food or medication options.
    - Purchase links.
    Trigger alerts for:
    - Potential health conflicts with the suggested products.
    """
    healthcare_agent = create_react_agent(
        llm,
        tools=[tools1["retriever_tool"]],
    )
    lifestyle_agent = create_react_agent(
        llm,
        tools=[tools2["retriever_tool"], tools2["tavily_tool"]],
    )
    return {
        "healthcare_agent": healthcare_agent,
        "lifestyle_agent": lifestyle_agent,
    }
