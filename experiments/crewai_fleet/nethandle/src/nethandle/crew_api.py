from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from crewai import Agent, Task, Crew
from crewai_tools import DOCXSearchTool, CodeInterpreterTool, SerperDevTool, WebsiteSearchTool
from crewai import LLM
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException

class QueryResponse(BaseModel):
    result: dict

# Initialize FastAPI app
app = FastAPI()

# Define the input schema for the API
class QueryRequest(BaseModel):
    topic: str

# Define the output schema for the API
class QueryResponse(BaseModel):
    result: dict

# Initialize tools
CodeInterpreterTool_crewtool = CodeInterpreterTool()
SerperDevTool_t = SerperDevTool()
WebsiteSearchTool_crewtool = WebsiteSearchTool()

health_rag_tool = DOCXSearchTool(docx='/root/net_handle/experiments/crewai_fleet/nethandle/src/nethandle/user_data/health_monitoring_data.docx')
lifestyle_rag_tool = DOCXSearchTool(docx='/root/net_handle/experiments/crewai_fleet/nethandle/src/nethandle/user_data/lifestyle_advisor_data.docx')

# Initialize LLM
llm = LLM(model="groq/llama3-8b-8192", api_key="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")

# Healthcare Agent
health_monitoring_agent = Agent(
    llm=llm,
    role="Health Monitoring Expert",
    goal="Analyze and interpret the user's health data using internal documents only.",
    backstory="""This agent evaluates the user's medical data, wearables, and health-related documents."""
)

health_monitoring_task = Task(
    description="""Evaluate the user's health data for the question: {topic}.""",
    agent=health_monitoring_agent,
    expected_output="Analysis of user's health data and recommendations.",
    tools=[health_rag_tool],
)

# Lifestyle Advisor Agent
lifestyle_advisor_agent = Agent(
    llm=llm,
    role="Lifestyle Advisor and Wellness Expert",
    goal="Provide evidence-based advice on optimizing the user's lifestyle.",
    backstory="""This agent enhances the user's lifestyle by providing wellness advice."""
)

lifestyle_advisor_task = Task(
    description="""Provide lifestyle recommendations for the question: {topic}.""",
    agent=lifestyle_advisor_agent,
    expected_output="Detailed lifestyle recommendations.",
    tools=[SerperDevTool_t, WebsiteSearchTool_crewtool, CodeInterpreterTool_crewtool],
)

# Crew with agents and tasks
crew = Crew(
    agents=[health_monitoring_agent, lifestyle_advisor_agent],
    tasks=[health_monitoring_task, lifestyle_advisor_task],
    verbose=True
)

@app.post("/process_query", response_model=QueryResponse)
def process_query(query: QueryRequest):
    try:
        print(f"Received query: {query.topic}")
        # Trigger the workflow
        crew_output = crew.kickoff(inputs={'topic': query.topic})
        
        # Convert CrewOutput to a dictionary if necessary
        if hasattr(crew_output, "raw"):
            result_dict = {"response": crew_output.raw}
        else:
            result_dict = crew_output  # If already a dictionary
        
        print(f"Workflow result: {result_dict}")
        return QueryResponse(result=result_dict)
    except Exception as e:
        print(f"Error during workflow execution: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Run the app with Uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
