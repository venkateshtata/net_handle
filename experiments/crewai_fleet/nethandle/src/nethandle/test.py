from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool
from langchain.agents import load_tools
import json
from crewai import Agent
from crewai import LLM
from crewai.tasks.task_output import TaskOutput
from crewai import LLM
from crewai_tools import DOCXSearchTool
from crewai_tools import CodeInterpreterTool
from crewai_tools import SerperDevTool
from crewai_tools import WebsiteSearchTool


# Healthcare tools
CodeInterpreterTool_crewtool = CodeInterpreterTool()

# Lifestyle tools
SerperDevTool_t = SerperDevTool()
WebsiteSearchTool_crewtool = WebsiteSearchTool()


health_rag_tool = DOCXSearchTool(docx='/root/net_handle/experiments/crewai_fleet/nethandle/src/nethandle/user_data/health_monitoring_data.docx')
lifestyle_rag_tool = DOCXSearchTool(docx='/root/net_handle/experiments/crewai_fleet/nethandle/src/nethandle/user_data/lifestyle_advisor_data.docx')


llm = LLM(model="groq/llama3-8b-8192", api_key="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")


# Updated Healthcare Agent
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
    expected_output="""A concise analysis of the user's health data with:
    - Evaluation of blood pressure and glucose metrics in relation to current walking habits.
    - Insights into trends or irregularities in activity effectiveness.
    - Recommendations for adjustments to improve health outcomes.
    - Alerts for potential risks based on physical activity and health data.
    - Collaborative insights from the Lifestyle Advisor Agent, if applicable.""",
    tools=[health_rag_tool, ],
)

# Updated Lifestyle Advisor Agent
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
    expected_output="""A detailed list of lifestyle recommendations, including:
    - Adjustments to the current walking routine for optimal impact on blood pressure and glucose.
    - Suggestions for complementary exercises or activities.
    - Tips for integrating habits that improve overall fitness and glucose management.
    - Collaborative insights shared with the Healthcare Agent as required.""",
    tools=[SerperDevTool_t, WebsiteSearchTool_crewtool, CodeInterpreterTool_crewtool],
)





# Execute the crew
crew = Crew(
    agents=[health_monitoring_agent, lifestyle_advisor_agent],
    tasks=[health_monitoring_task, lifestyle_advisor_task],
    verbose=True
)


result = crew.kickoff(inputs={'topic': 'What simple changes can I make to my meals and daily routine to help manage my morning blood sugar levels?'})

print('result: ', result)
