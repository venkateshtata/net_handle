from environment.setup import setup_environment
from pdf_processing.processor import load_and_prepare_documents
from tools.retriever import create_knowledge_base
from tools.setup import setup_tools
from agents.creation import create_agents
from agents.workflow import define_workflow
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage


def main():
    setup_environment()

    health_documents = load_and_prepare_documents("/root/net_handle/nethandle/user_data/health_data")
    if not health_documents:
        print("Error: No documents were loaded for health_data.")
    else:
        print("health_data loaded")
    lifestyle_documents = load_and_prepare_documents("/root/net_handle/nethandle/user_data/lifestyle_data")
    if not lifestyle_documents:
        print("Error: No documents were loaded for lifestyle_data.")
    else:
        print("lifestyle_data loaded")
    

    health_retriever_tool = create_knowledge_base(health_documents, "HealthcareAgent", "retrieving medical document information for patients")
    lifestyle_retriever_tool = create_knowledge_base(lifestyle_documents, "LifestyleAgent", "retrieving lifestyle, dietary, and wellness information for personalized recommendations")

    health_tools = setup_tools(health_retriever_tool)
    lifestyle_tools = setup_tools(lifestyle_retriever_tool)

    llm = ChatOpenAI(model="gpt-4o")
    agents = create_agents(health_tools, lifestyle_tools, llm)
    graph = define_workflow(agents, llm)

    log = []
    final_state = None
    for state in graph.stream(
        {
            "messages": [
                HumanMessage(
                    content="I need a diabetes-friendly dinner recipe. Can you find one and confirm if it aligns with my health records and medications?"
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

    print("\n--- Final Summary of Workflow ---\n")
    for entry in log:
        print(entry)

    if final_state:
        print("\n--- Final Message ---\n")
        print(final_state["messages"][-1].content)

    return final_state

if __name__ == "__main__":
    main()
