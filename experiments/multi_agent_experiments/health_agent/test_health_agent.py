import getpass
import os
from typing import Annotated, Sequence, Literal
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_experimental.tools import PythonREPLTool
from langchain_core.messages import HumanMessage
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


def create_knowledge_base(documents):
    """Create a retriever tool from documents."""
    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(documents, embeddings)
    retriever = db.as_retriever()
    return create_retriever_tool(retriever, "HealthcareAgent", "Can retrieve medical documents information of patient")


# 3. **Tools Setup**
def setup_tools(retriever_tool):
    """Initialize all tools required for the workflow."""
    tavily_tool = TavilySearchResults(max_results=5)
    python_repl_tool = PythonREPLTool()
    return {
        "retriever_tool": retriever_tool,
        "tavily_tool": tavily_tool,
        "python_repl_tool": python_repl_tool,
    }


def create_agents(tools, llm):
    """Create specific agents using the tools."""
    healthcare_agent = create_react_agent(llm, tools=[tools["retriever_tool"]])
    code_agent = create_react_agent(llm, tools=[tools["python_repl_tool"]])

    return {
        "healthcare_agent": healthcare_agent,
        "code_agent": code_agent,
    }


def define_workflow(agents, llm):
    """Define the state graph for the workflow."""
    members = ["HealthcareAgent", "Coder"]

    # Supervisor prompt and LLM chain
    system_prompt = (
        "You are a supervisor tasked with managing a conversation between the"
        " following workers: {members}. Each worker has the following expertise:"
        "\n- HealthcareAgent: healthcare assistant designed to help users manage their health records and provide personalized medical insights."
        "\n- Coder: Write python code."
        " Given the following user request, respond with the worker to act next."
        " Each worker will perform a task and respond with their results and status."
        " When finished, respond with FINISH."
    )
    options = ["FINISH"] + members

    class routeResponse(BaseModel):
        next: Literal["FINISH", "HealthcareAgent", "Coder"]

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
    workflow.add_node("Coder", lambda state: agent_node(state, agents["code_agent"], "Coder", state["log"]))
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


# 7. **Main Execution (Updated)**
def main():
    setup_environment()
    documents = load_and_prepare_documents("/root/net_handle/experiments/multi_agent_experiments/lifestyle_agent/data")
    retriever_tool = create_knowledge_base(documents)
    tools = setup_tools(retriever_tool)

    llm = ChatOpenAI(model="gpt-4o")
    agents = create_agents(tools, llm)
    graph = define_workflow(agents, llm)

    log = []
    final_state = None
    for state in graph.stream(
        {
            "messages": [
                HumanMessage(
                    content="what are the medications that i bought ?"
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

    if final_state:
        print("\n--- Final Message ---\n")
        print(final_state["messages"][-1].content)


if __name__ == "__main__":
    main()