import getpass
import os
from typing import Annotated, Sequence, Literal
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.utilities.twilio import TwilioAPIWrapper
from langchain_experimental.tools import PythonREPLTool
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from typing_extensions import TypedDict
from langgraph.graph import END, StateGraph, START
from langgraph.prebuilt import create_react_agent
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain.tools.retriever import create_retriever_tool
import operator
from langchain_core.messages import BaseMessage, HumanMessage


# 1. **Environment Setup**
def set_env_var(var: str):
    """Prompt for environment variables if not already set."""
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"Please provide your {var}")


def setup_environment():
    set_env_var("OPENAI_API_KEY")
    set_env_var("TAVILY_API_KEY")


# 2. **PDF Processing**
def load_and_prepare_documents(file_path: str, chunk_size: int = 1000, chunk_overlap: int = 0):
    """Load and split documents into chunks."""
    loader = PyPDFDirectoryLoader(file_path)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return text_splitter.split_documents(documents)


def create_knowledge_base(documents, name,  agent_description):
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


# 3. **Tools Setup**
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
    twilio_tool = TwilioAPIWrapper(
        account_sid= "AC8cda509b991547746f51b4559f4b24d7",#os.environ.get("TWILIO_ACCOUNT_SID"),
        auth_token= "225c4fb55a2c430db88fb8ff80564664",#os.environ.get("TWILIO_AUTH_TOKEN"),
        from_number= "whatsapp:+14155238886",#os.environ.get("TWILIO_FROM_NUMBER"),
        #to_number=os.environ.get("TWILIO_TO_NUMBER"),
    )

    return {
        "health_retriever_tool": health_retriever_tool,
        "lifestyle_retriever_tool": lifestyle_retriever_tool,
        "tavily_tool": tavily_tool,
        "twilio_tool": twilio_tool
    }


def create_agents(tools, llm):
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
    visualize_system_message_health = SystemMessage(content=health_prompt)
    visualize_system_message_lifestyle = SystemMessage(content=lifestyle_prompt)
    healthcare_agent = create_react_agent(
        llm,
        tools=[tools["health_retriever_tool"]],
        #state_modifier=visualize_system_message_health
        #description="Agent for managing healthcare-related tasks. It has access to the user's medical records and retrieves insights."
    )
    lifestyle_agent = create_react_agent(
        llm,
        tools=[tools["lifestyle_retriever_tool"], tools["tavily_tool"]],
        #state_modifier=visualize_system_message_lifestyle
        #description="Agent for providing lifestyle recommendations. It has access to dietary preferences, wellness data, and internet search."
    )
    return {
        "healthcare_agent": healthcare_agent,
        "lifestyle_agent": lifestyle_agent,
    }


def define_workflow(agents, llm):
    """Define the state graph for the workflow."""
    members = ["HealthcareAgent", "LifestyleAgent"]

    # Supervisor prompt and LLM chain
    system_prompt = (
        "You are a supervisor tasked with managing a conversation between the"
        " following workers: {members}. Each worker has the following expertise:"
        "\n- HealthcareAgent: A healthcare assistant with access to the user's health records, medications, and medical insights. It is designed to answer questions related to healthcare and personal medical information."
        "\n- LifestyleAgent: A lifestyle assistant with access to the user's lifestyle preferences, including dietary data and wellness routines. It can provide lifestyle recommendations and browse the internet to find relevant information."
        " Your role is to decide which worker should handle the user's request."
        " Provide clear instructions to the selected worker and ensure the workflow is completed efficiently."
        " When all tasks are finished, respond with FINISH."
    )
    options = ["FINISH"] + members

    class routeResponse(BaseModel):
        next: Literal["FINISH", "HealthcareAgent", "LifestyleAgent"]

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="messages"),
            (
                "system",
                "Given the conversation above, who should act next?"
                " Or should we FINISH? Select one of: {options}",
            ),
        ]
    ).partial(options=str(options), members=", ".join(members))

    def supervisor_agent(state):
        supervisor_chain = prompt | llm.with_structured_output(routeResponse)
        decision = supervisor_chain.invoke(state)
        state["log"].append(f"Supervisor decided to assign task to: {decision.next}")
        return decision

    workflow = StateGraph(AgentState)

    # Define agents directly without wrapping in functools.partial
    workflow.add_node("HealthcareAgent", lambda state: agent_node(state, agents["healthcare_agent"], "HealthcareAgent", state["log"]))
    workflow.add_node("LifestyleAgent", lambda state: agent_node(state, agents["lifestyle_agent"], "LifestyleAgent", state["log"]))
    workflow.add_node("supervisor", supervisor_agent)

    for member in members:
        workflow.add_edge(member, "supervisor")

    conditional_map = {k: k for k in members}
    conditional_map["FINISH"] = END
    workflow.add_conditional_edges("supervisor", lambda x: x["next"], conditional_map)
    workflow.add_edge(START, "supervisor")

    return workflow.compile()


def agent_node(state, agent, name, log):
    """Run a node and format results."""
    result = agent.invoke(state)
    message_content = result["messages"][-1].content
    log.append(f"{name} completed task with response: {message_content}")
    return {"messages": [HumanMessage(content=message_content, name=name)]}


class AgentState(TypedDict):
    """Define the agent state format."""
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next: str
    log: list[str]


# 7. **Main Execution**
def main():
    setup_environment()
    health_documents = load_and_prepare_documents("health_data")
    lifestyle_documents = load_and_prepare_documents("lifestyle_data")
    '''health_retriever_tool = create_knowledge_base(
        health_documents,
        "HealthcareAgent",
        "retrieving medical document information for patients"
    )
    lifestyle_retriever_tool = create_knowledge_base(
        lifestyle_documents,
        "LifestyleAgent",
        "retrieving lifestyle, dietary, and wellness information for personalized recommendations"
    )'''

    #health_tools = setup_tools(health_retriever_tool)
    #lifestyle_tools = setup_tools(lifestyle_retriever_tool)
    tools = setup_tools(health_documents, lifestyle_documents)

    llm = ChatOpenAI(model="gpt-4o")
    agents = create_agents(tools, llm)
    graph = define_workflow(agents, llm)

    log = []
    final_state = None
    for state in graph.stream(
        {
            "messages": [
                HumanMessage(
                    content="Give me my name"
                )
            ],
            "log": log,
        }
    ):
        if "__end__" not in state:
            print(state)
            print("----")
        else:
            final_state = state

    # Print final log summary
    print("\n--- Final Summary of Workflow ---\n")
    for entry in log:
        print(entry)

    print("Sending message to whatsapp")
    tools["twilio_tool"].run("test message from model output", "whatsapp:+447774839645")

    if final_state:
        print("\n--- Final Message ---\n")
        print(final_state["messages"][-1].content)

    


if __name__ == "__main__":
    main()
