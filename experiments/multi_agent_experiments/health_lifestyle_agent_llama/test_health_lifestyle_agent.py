import getpass
import os
from typing import Annotated, Sequence, Literal
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_experimental.tools import PythonREPLTool
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# from groq_llm_wrapper import GroqLLMWrapper
from langchain_groq.chat_models import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
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
from transformers import AutoTokenizer
from langchain_ollama import OllamaEmbeddings

# embeddings_model_name = "meta-llama/Llama-3.2-11B-Vision"
# embeddings_model_name = 'meta-llama/Llama-3.2-1B'
embeddings_model_name = 'sentence-transformers/all-MiniLM-L6-v2'
# chat_model='llama-3.2-11b-vision-preview'
chat_model = 'llama-3.2-90b-vision-preview'


# 1. **Environment Setup**
def set_env_var(var: str):
    """Prompt for environment variables if not already set."""
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"Please provide your {var}")


def setup_environment():
    # set_env_var("OPENAI_API_KEY")
    set_env_var("TAVILY_API_KEY")
    set_env_var("GROQ_API_KEY")
    set_env_var("HUGGINGFACE_API_KEY")


# 2. **PDF Processing**
def load_and_prepare_documents(file_path: str, chunk_size: int = 1000, chunk_overlap: int = 0):
    """Load and split documents into chunks."""
    loader = PyPDFDirectoryLoader(file_path)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return text_splitter.split_documents(documents)


def get_embeddings(embeddings_model):
    # return OpenAIEmbeddings()
    if embeddings_model.lower() == 'huggingface':
        if embeddings_model_name == 'meta-llama/Llama-3.2-1B':
            tokenizer = AutoTokenizer.from_pretrained(embeddings_model_name)
            if tokenizer.pad_token is None:
                tokenizer.add_special_tokens({'pad_token': tokenizer.eos_token})

            # Pass the tokenizer with the added padding token to HuggingFaceEmbeddings
            embeddings = HuggingFaceEmbeddings(
                model_name=embeddings_model_name
            )

            embeddings._client.tokenizer = tokenizer
            print(f'Printing {embeddings_model} embeddings: {embeddings}')
            return embeddings

    elif embeddings_model.lower() == 'openai':
        print(f'Printing {embeddings_model} embeddings: {OpenAIEmbeddings()}')
        return OpenAIEmbeddings()
    
    elif embeddings_model.lower() == 'ollama':
        print(f'Printing {embeddings_model} embeddings: {OllamaEmbeddings(model=embeddings_model_name)}')
        return OllamaEmbeddings(model=embeddings_model_name)
    
    else:
        print(f'Printing embeddings: {HuggingFaceEmbeddings(model_name=embeddings_model_name)}')
        return HuggingFaceEmbeddings(model_name=embeddings_model_name)


def create_knowledge_base(documents, agent_name, agent_description):
    """Create a retriever tool from documents."""
    used_embeddings = 'OpenAI'
    # used_embeddings = 'Ollama'
    # used_embeddings = 'HuggingFace'
    embeddings = get_embeddings(used_embeddings)
    db = FAISS.from_documents(documents, embeddings)
    retriever = db.as_retriever()
    return create_retriever_tool(retriever, agent_name, agent_description)


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


def create_agents(tools1, tools2, llm):
    """Create specific agents using the tools."""
    healthcare_agent = create_react_agent(llm, tools=[tools1["retriever_tool"]])
    lifestyle_agent = create_react_agent(llm, tools=[tools2["retriever_tool"], tools2["tavily_tool"]])

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
        "\n- HealthcareAgent: healthcare assistant has access to the user's health records and designed to help users manage their health records and provide personalized medical insights."
        "\n- LifestyleAgent: lifestyle assistant has access to the user's lifestyle records and designed to help users gain insghts on their dietary preferences, wellness routines, and provide personalized lifestyle recommendations. It also has access to browsing internet."
        " Given the following user request, respond with the worker to act next."
        " Each worker will perform a task and respond with their results and status."
        " When finished, respond with FINISH."
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


def get_llm():
    # return ChatOpenAI(model="gpt-4o")
    return ChatGroq(model=chat_model, temperature=0.0, max_retries=2)


# 7. **Main Execution (Updated)**
def main():
    setup_environment()
    health_documents = load_and_prepare_documents("health_data")
    lifestyle_documents = load_and_prepare_documents("lifestyle_data")
    health_retriever_tool = create_knowledge_base(health_documents, "HealthcareAgent", "Can retrieve medical documents information of patient")
    lifestyle_retriever_tool = create_knowledge_base(lifestyle_documents, "LifestyleAgent", "Can retrieve lifestyle, dietary, and wellness information for personalized recommendations")

    health_tools = setup_tools(health_retriever_tool)
    lifestyle_tools = setup_tools(lifestyle_retriever_tool)

    llm = get_llm()
    agents = create_agents(health_tools, lifestyle_tools, llm)
    graph = define_workflow(agents, llm)

    log = []
    final_state = None
    for state in graph.stream(
        {
            "messages": [
                HumanMessage(
                    #content="Which food should i avoid based on my preferences?"
                    content="what are my dietary restrictions or food that i should avoid ? "
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