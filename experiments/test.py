import getpass
import os
from typing import Annotated, Literal, Sequence
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
import functools
import operator
from typing_extensions import TypedDict
from langgraph.graph import END, StateGraph, START
from ionic_langchain.tool import IonicTool
from langchain.agents import create_react_agent
from langchain.document_loaders import PyMuPDFLoader  # For loading PDFs
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.vectorstores.base import VectorStoreRetriever
from langchain_openai import OpenAI
from langchain_core.exceptions import OutputParserException
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.prompts import ChatPromptTemplate



# Set environment variables for API keys
def _set_if_undefined(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"Please provide your {var}")

_set_if_undefined("OPENAI_API_KEY")
# _set_if_undefined("IONIC_API_KEY")

# Initialize the OpenAI LLM for agent responses
open_ai_key = os.environ["OPENAI_API_KEY"]
model = "gpt-3.5-turbo-instruct"
temperature = 0.6
llm = OpenAI(openai_api_key=open_ai_key, model_name=model, temperature=temperature)

# Define IonicTool for product search (ShoppingAgent)
ionic_tool = IonicTool().tool()
ionic_tool.description = str(
    """
Ionic is an e-commerce shopping tool. Assistant uses the Ionic Commerce Shopping Tool to find, discover, and compare products from thousands of online retailers. Assistant should use the tool when the user is looking for a product recommendation or trying to find a specific product.

The user may specify the number of results, minimum price, and maximum price for which they want to see results.
Ionic Tool input is a comma-separated string of values:
  - query string (required, must not include commas)
  - number of results (default to 4, no more than 10)
  - minimum price in cents ($5 becomes 500)
  - maximum price in cents
For example, if looking for coffee beans between 5 and 10 dollars, the tool input would be `coffee beans, 5, 500, 1000`.

Return them as a markdown formatted list with each recommendation from tool results, being sure to include the full PDP URL.
"""
)

# Load and preprocess patient data from local PDF files
pdf_loader = PyMuPDFLoader("records/clinic_letter.pdf")  # Directory containing PDF files
documents = pdf_loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
split_docs = text_splitter.split_documents(documents)
embeddings = OpenAIEmbeddings(openai_api_key=open_ai_key)
vector_store = FAISS.from_documents(split_docs, embeddings)
retriever = VectorStoreRetriever(vectorstore=vector_store)

# Create a retrieval-based QA chain for querying patient data
patient_qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True
)

def agent_node(state, agent, name):
    try:
        result = agent.invoke(state)
        # print("Result from agent:", result)  # For debugging
        # Check if 'messages' key is present, if not, wrap 'recommendations' in a HumanMessage
        if "messages" not in result:
            if "recommendations" in result:
                recommendations_text = "\n".join(result["recommendations"])
                result["messages"] = [HumanMessage(content=recommendations_text, name=name)]
            else:
                raise KeyError("Expected key 'messages' or 'recommendations' not found in result.")
        return {
            "messages": [HumanMessage(content=result["messages"][-1].content, name=name)]
        }
    except KeyError as e:
        print("Error:", e)
        return {
            "messages": [HumanMessage(content="An error occurred. Please try again.", name=name)]
        }




members = ["PatientAgent", "ShoppingAgent"]
system_prompt = (
    "You are a supervisor managing a conversation between the following workers: {members}. "
    "Respond with the worker to act next. Each worker will perform a task and respond with "
    "their results. When finished, respond with FINISH."
)

options = ["FINISH"] + members

class routeResponse(BaseModel):
    next: Literal["FINISH", "PatientAgent", "ShoppingAgent"]

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

llm_supervisor = ChatOpenAI(model="gpt-4o")

def supervisor_agent(state):
    supervisor_chain = prompt | llm_supervisor.with_structured_output(routeResponse)
    return supervisor_chain.invoke(state)

# Define AgentState for each node in the graph
class AgentState(TypedDict):
    messages: Annotated[Sequence[HumanMessage], operator.add]
    next: str

# Define PatientAgent with symptom analysis and medication recommendation
class PatientAgent:
    def __init__(self):
        self.symptoms_to_medications = {}

    def invoke(self, state):
        query = state["messages"][-1].content
        # Use `query` as the key since it's expected by `patient_qa_chain`
        retrieved_info = patient_qa_chain({"query": query})  # Updated key to "query"
        # Extract information from retrieved documents
        detected_symptoms = self.detect_symptoms(retrieved_info["source_documents"])
        # Generate medication requests for ShoppingAgent
        medication_requests = self.request_medications(detected_symptoms)
        self.symptoms_to_medications.update(medication_requests)
        return {
            "messages": [
                HumanMessage(content=f"Detected symptoms and requested medications: {medication_requests}")
            ]
        }

    def detect_symptoms(self, documents):
        # Placeholder method to detect symptoms in retrieved documents
        symptoms = ["cough", "fever", "headache"]
        detected_symptoms = {}
        for symptom in symptoms:
            for doc in documents:
                if symptom in doc.page_content:
                    detected_symptoms[symptom] = True
        return detected_symptoms

    def request_medications(self, symptoms):
        # Placeholder for generating medication requests based on detected symptoms
        medication_requests = {symptom: f"{symptom} medication" for symptom in symptoms}
        return medication_requests
    
# Final Supervisor summary of symptoms and recommended medications
def generate_summary(symptoms_to_medications):
    summary = "Summary of detected symptoms and medications:\n"
    for symptom, medication in symptoms_to_medications.items():
        summary += f"- Symptom: {symptom}, Recommended Medication: {medication}\n"
    return summary



search = DuckDuckGoSearchRun()


shopping_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a shopping assistant to help user shop for medications and other lifestyle goods. Make use of search tool to search for products and respond only with JSON as `{{ \"recommendations\": [\"option1\", \"option2\"] }}`."),
        MessagesPlaceholder(variable_name="messages"),
        (
            "assistant",
            "Here's the structured data:\n{agent_scratchpad}\nRespond in the JSON format specified."
        )
    ]
).partial(
    tool_names=", ".join([tool.name for tool in [ionic_tool]]),
    tools=[search]
)


from langchain_core.output_parsers.base import BaseOutputParser

class JSONOutputParser(BaseOutputParser):
    def parse(self, output: str):
        # Strip any leading/trailing whitespace and ensure correct JSON parsing
        try:
            import json
            parsed_output = json.loads(output.strip("`"))
            return parsed_output
        except json.JSONDecodeError as e:
            raise OutputParserException(f"Could not parse JSON: {output}") from e




# Now, create the ShoppingAgent with the updated prompt
# shopping_agent = create_react_agent(llm=llm, tools=[ionic_tool], prompt=shopping_prompt)
shopping_agent = create_react_agent(
    llm=llm,
    tools=[ionic_tool],
    prompt=shopping_prompt,
    output_parser=JSONOutputParser()
)





# Define ShoppingAgent with Ionic tool for product searches
# shopping_agent = create_react_agent(llm, tools=[ionic_tool])

patient_node = functools.partial(agent_node, agent=PatientAgent(), name="PatientAgent")
shopping_node = functools.partial(agent_node, agent=shopping_agent, name="ShoppingAgent")

# Create the workflow graph
workflow = StateGraph(AgentState)
workflow.add_node("PatientAgent", patient_node)
workflow.add_node("ShoppingAgent", shopping_node)
workflow.add_node("supervisor", supervisor_agent)

for member in members:
    workflow.add_edge(member, "supervisor")

conditional_map = {k: k for k in members}
conditional_map["FINISH"] = END
workflow.add_conditional_edges("supervisor", lambda x: x["next"], conditional_map)
workflow.add_edge(START, "supervisor")

from langchain_core.messages import SystemMessage

# Define a simple action class with a `log` attribute
class Action:
    def __init__(self, log):
        self.log = log

# Create a single instance of PatientAgent
patient_agent_instance = PatientAgent()

# Update patient_node to use the created instance
patient_node = functools.partial(agent_node, agent=patient_agent_instance, name="PatientAgent")

# Execute the workflow as before
state = {
    "messages": [
        HumanMessage(content="Fetch patient medical details, suggest needed medications with exact names of each drug, and identify where to buy them.")
    ],
    "intermediate_steps": []  # Initialize intermediate_steps
}

while True:
    next_node = supervisor_agent(state)
    if next_node.next == "FINISH":
        break
    if next_node.next == "PatientAgent":
        result = patient_node(state)
    elif next_node.next == "ShoppingAgent":
        result = shopping_node(state)
    
    # Update state with the results from the node
    state["messages"].extend(result["messages"])
    
    # Structure each intermediate step with action and observation
    action = Action(log=next_node.next)  # Wrap action with log attribute
    observation = result["messages"][-1].content  # Last message content as observation
    state["intermediate_steps"].append((action, observation))  # Append as a tuple of objects

    print(result)
    print("----")

# Generate and print the final summary using the same instance
print(generate_summary(patient_agent_instance.symptoms_to_medications))