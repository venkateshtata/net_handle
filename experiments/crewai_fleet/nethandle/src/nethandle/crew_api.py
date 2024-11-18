from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from crewai import Agent, Task, Crew
from crewai_tools import DOCXSearchTool, CodeInterpreterTool, SerperDevTool, WebsiteSearchTool, ScrapeWebsiteTool
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

# Healthcare tools
CodeInterpreterTool_crewtool = CodeInterpreterTool()

# Lifestyle tools
SerperDevTool_t = SerperDevTool(
    api_key="be965cf805f7f0d4d4ea2082dcde185304bb47d056e0ca09e905fa43ee2cf5c7",
    n_results=2,
)
WebsiteSearchTool_crewtool = WebsiteSearchTool()
ScrapeWebsiteTool_crewtool = ScrapeWebsiteTool()


health_rag_tool = DOCXSearchTool(docx='/root/net_handle/experiments/crewai_fleet/nethandle/src/nethandle/user_data/health_monitoring_data.docx')
lifestyle_rag_tool = DOCXSearchTool(docx='/root/net_handle/experiments/crewai_fleet/nethandle/src/nethandle/user_data/lifestyle_advisor_data.docx')


# model_name="groq/llama-3.1-70b-versatile"
model_name="groq/llama3-8b-8192"
#model_name = "openai/gpt-4o"
# model_name="ollama/llama3:70b"
llm = LLM(model=model_name, api_key="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")


health_monitoring_agent = Agent(
    llm=llm,
    role="Monitor  the user's health by tracking key health metrics and integrating past medical records.",
    goal="Who is the Health Monitoring Agent? This agent tracks and analyzes the user's mood, stress, sleep, and other health metrics. It accesses past medical records to provide insights, suggests medical follow-ups, and send alerts",
    backstory="The Health Monitoring Agent was designed to act as a digital health companion. It continuously tracks the user's health metrics through wearables and self-reported data, cross-referencing this with medical records. The agent identify existing health risks, reminding users of medication, and booking appointments or coordinating care.",
)

health_monitoring_agent = Agent(
    llm=llm,
    role="Health Monitoring Expert",
    goal="Analyze and interpret the user's health data, including blood pressure, glucose levels, and physical activity trends, using internal documents only. It does not use the internet for responses.",
    backstory="""This agent is a digital health assistant that continuously evaluates the user's 
    medical data, wearables, and internal health-related documents. It identifies patterns and provides 
    insights into how these metrics align with the user's health goals. The agent relies on lifestyle 
    insights from the Lifestyle Advisor Agent when necessary for a comprehensive response.""",
)

health_monitoring_task = Task(
    description="""Evaluate the user's walking routine by analyzing its impact on blood pressure and glucose levels 
    based on internal health-related documents for the question: {topic}. Collaborate with the Lifestyle Advisor Agent 
    if necessary to enrich the analysis with lifestyle insights.""",
    agent=health_monitoring_agent,
    expected_output="""A concise analysis of the user's health data on {topic} with:
    - Evaluation of blood pressure and glucose metrics in relation to current walking habits.
    - Insights into trends or irregularities in activity effectiveness.
    - Recommendations for adjustments to improve health outcomes.
    - Alerts for potential risks based on physical activity and health data.
    - Collaborative insights from the Lifestyle Advisor Agent, if applicable.""",
    tools=[health_rag_tool, CodeInterpreterTool_crewtool],
)


lifestyle_advisor_agent = Agent(
    llm=llm,
    role="Lifestyle Advisor and Wellness Expert",
    goal="Provide evidence-based advice on optimizing the user's lifestyle, focusing on fitness and wellness. This agent uses the internet to gather insights and assist the Healthcare Agent with supplemental information as needed.",
    backstory="""This agent enhances the user's lifestyle by aligning exercise routines, stress management practices, 
    and dietary habits with their health needs. It collaborates with the Healthcare Agent to ensure its recommendations 
    are enriched by broader health metrics and patterns, providing a holistic solution.""",
)

lifestyle_advisor_task = Task(
    description="""Provide recommendations to optimize the user's walking routine and suggest complementary exercises or habits 
    that can further support blood pressure and glucose management for the question: {topic}. Assist the Healthcare Agent 
    with supplemental insights if required using internet.""",
    agent=lifestyle_advisor_agent,
    expected_output="""A detailed list of lifestyle recommendations on {topic}, including:
    - Adjustments to the current walking routine for optimal impact on blood pressure and glucose.
    - Suggestions for complementary exercises or activities.
    - Tips for integrating habits that improve overall fitness and glucose management.
    - Collaborative insights shared with the Healthcare Agent as required.""",
    tools=[lifestyle_rag_tool, SerperDevTool_t, WebsiteSearchTool_crewtool, ScrapeWebsiteTool_crewtool],
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
