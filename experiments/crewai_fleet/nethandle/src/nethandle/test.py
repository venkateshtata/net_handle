from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool
from langchain.agents import load_tools
import json
from crewai import Agent
from crewai import LLM
from crewai.tasks.task_output import TaskOutput
#from crewai_tools import PDFSearchTool
from crewai import LLM
from crewai_tools import DOCXSearchTool


llm = LLM(model="groq/llama3-8b-8192", api_key="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")


health_rag_tool = DOCXSearchTool(docx='/root/net_handle/experiments/crewai_fleet/nethandle/src/nethandle/user_data/health_monitoring_data.docx')
lifestyle_rag_tool = DOCXSearchTool(docx='/root/net_handle/experiments/crewai_fleet/nethandle/src/nethandle/user_data/lifestyle_advisor_data.docx')


# search_tool = SerperDevTool()



def callback_function(output: TaskOutput):
    # Do something after the task is completed
    # Example: Send an email to the manager
    print(f"""
        Task 1 completed!
        Task: {output.description}
        Output: {output.raw}
    """)


health_monitoring_agent = Agent(
    llm=llm,
    role="Monitor  the user's health by tracking key health metrics and integrating past medical records.",
    goal="Who is the Health Monitoring Agent? This agent tracks and analyzes the user's mood, stress, sleep, and other health metrics. It accesses past medical records to provide insights, suggests medical follow-ups, and send alerts",
    backstory="The Health Monitoring Agent was designed to act as a digital health companion. It continuously tracks the user's health metrics through wearables and self-reported data, cross-referencing this with medical records. The agent identify existing health risks, reminding users of medication, and booking appointments or coordinating care.",
)

health_monitoring_task = Task(
    description="Monitor the user's daily health metrics, identify trends or risks, and provide alerts or reminders for important health actions on the question: {topic}. ",
    agent=health_monitoring_agent,
    expected_output="A bullet list summary of the top 5 most important health metrics, trends, and insights on the question: {topic}.",
    #expected_output=(
        #"A detailed summary of the user's current health metrics, "
        #"trends based on past data, potential risks, and alerts or reminders for health-related tasks."
    #),
    tools=[health_rag_tool],
)


lifestyle_advisor_agent = Agent(
    llm=llm,
    role='Lifestyle and Dietary Wellness Assistant',
    goal="Provide personalized wellness and lifestyle guidance tailored to the user's health conditions and goals.",
    backstory="""You're a specialized assistant that analyzes lifestyle and dietary habits 
    to provide personalized recommendations. You focus on enhancing routines, managing stress, 
    and improving sleep through actionable insights. Your expertise lies in dietary deficiencies, 
    meal timing, and their impact on health.""",
    verbose=True
)


lifestyle_advisor_task = Task(
    description="Generate personalized lifestyle on the question: {topic} recommendations based on the user's health metrics, medical history, and goals.",
    agent=lifestyle_advisor_agent,
    #expected_output=(
        #"A set of actionable lifestyle suggestions, such as a tailored meal plan, exercise routine, "
        #"and relaxation techniques, that align with the user's health conditions and preferences."
    #),
    expected_output="A bullet list summary of the top 5 most important lifestyle recommendations on the question {topic}.",
    tools=[lifestyle_rag_tool],
    # context=[task1]
)


# Execute the crew
crew = Crew(
    agents=[health_monitoring_agent, lifestyle_advisor_agent],
    tasks=[health_monitoring_task, lifestyle_advisor_task],
    verbose=True
)


result = crew.kickoff(inputs={'topic': 'give summary of my doctor visits ?'})

print('result: ', result)
