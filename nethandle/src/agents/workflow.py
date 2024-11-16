from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage
from langgraph.graph import END, StateGraph, START
from typing import Literal
from pydantic import BaseModel
from typing import TypedDict
from typing import List, Literal
from langchain_core.messages import BaseMessage
from langchain_core.messages import HumanMessage

def agent_node(state, agent, name, log):
    """Run a node and format results."""
    result = agent.invoke(state)
    message_content = result["messages"][-1].content
    log.append(f"{name} completed task with response: {message_content}")
    return {"messages": [HumanMessage(content=message_content, name=name)]}


class AgentState(TypedDict):
    """Define the agent state format."""
    messages: List[BaseMessage]  # List of messages for the agent
    next: Literal["FINISH", "HealthcareAgent", "LifestyleAgent"]  # Next step
    log: List[str]  # Log of actions and decisions


def define_workflow(agents, llm):
    """Define the state graph for the workflow."""
    members = ["HealthcareAgent", "LifestyleAgent"]

    workflow = StateGraph(AgentState)

    # Define the system prompt
    system_prompt = (
        "You are a supervisor tasked with managing a conversation between the"
        " following workers: {members}. Each worker has the following expertise:"
        "\n- HealthcareAgent: A healthcare assistant with access to the user's health records, medications, and medical insights. It is designed to answer questions related to healthcare and personal medical information."
        "\n- LifestyleAgent: A lifestyle assistant with access to the user's lifestyle preferences, including dietary data and wellness routines. It can provide lifestyle recommendations and browse the internet to find relevant information."
        " Your role is to decide which worker should handle the user's request."
        " Provide clear instructions to the selected worker and ensure the workflow is completed efficiently."
        " When all tasks are finished, respond with FINISH."
    )

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
    ).partial(options=str(["FINISH"] + members), members=", ".join(members))

    def supervisor_agent(state):
        supervisor_chain = prompt | llm.with_structured_output(routeResponse)
        decision = supervisor_chain.invoke(state)
        state["log"].append(f"Supervisor decided to assign task to: {decision.next}")
        return decision

    workflow = StateGraph(AgentState)

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
