from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from environment.setup import setup_environment
from pdf_processing.processor import load_and_prepare_documents
from tools.setup import setup_tools
from agents.creation import create_agents
from agents.workflow import define_workflow
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

import uvicorn  # Import uvicorn to run the server

# FastAPI app instance
app = FastAPI()

# Request and response models
class UserRequest(BaseModel):
    message: str

class AgentResponse(BaseModel):
    output: str
    log: list

# Load the environment and prepare tools
setup_environment()

health_documents = load_and_prepare_documents("../mock_data/health_data")
if not health_documents:
    raise Exception("Error: No documents were loaded for health_data.")
lifestyle_documents = load_and_prepare_documents("../mock_data/lifestyle_data")
if not lifestyle_documents:
    raise Exception("Error: No documents were loaded for lifestyle_data.")

tools = setup_tools(health_documents, lifestyle_documents)
llm = ChatOpenAI(model="gpt-4o")
agents = create_agents(tools, llm)
graph = define_workflow(agents, llm)

@app.post("/agent-workflow", response_model=AgentResponse)
async def agent_workflow(user_request: UserRequest):
    log = []
    final_state = None

    try:
        print("Starting workflow execution...")

        for state in graph.stream(
            {
                "messages": [
                    HumanMessage(content=user_request.message)
                ],
                "log": log,
            }
        ):
            print(f"Current state: {state}")
            supervisor_response = state.get("supervisor", {})
            print("supervisor_response: ", supervisor_response)
            # Recognize 'FINISH' as a valid terminal state
            if "__end__" in state or supervisor_response == {}:
                print("FINISH DETECTED!!")
                final_state = state

        # Handle incomplete workflows gracefully
        if not final_state:
            print("Workflow ended prematurely. Returning intermediate results.")
            return AgentResponse(
                output="Workflow did not reach an end state. Here's the last response:\n" +
                       state["LifestyleAgent"]["messages"][-1].content,
                log=log
            )

        # Extract the final message from the state
        final_message = final_state["LifestyleAgent"]["messages"][-1].content
        return AgentResponse(output=final_message, log=log)

    except Exception as e:
        print(f"Error occurred during workflow: {e}")
        raise HTTPException(status_code=500, detail=str(e))




# Main entry point to run the server
if __name__ == "__main__":
    # Start the server with uvicorn
    uvicorn.run("main.py:app", host="0.0.0.0", port=8000, reload=True)
