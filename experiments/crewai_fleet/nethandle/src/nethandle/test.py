from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool
from langchain.agents import load_tools
import json
from crewai import Agent
from crewai import LLM
from crewai.tasks.task_output import TaskOutput




# llm = LLM(model="gpt-4", temperature=0.7)


def callback_function(output: TaskOutput):
    # Do something after the task is completed
    # Example: Send an email to the manager
    print(f"""
        Task 1 completed!
        Task: {output.description}
        Output: {output.raw}
    """)


agent1 = Agent(
  role='Data Analyst',
  goal='Extract actionable insights',
  backstory="""You're a data analyst at a large company.
    You're responsible for analyzing data and providing insights
    to the business.
    You're currently working on a project to analyze the
    performance of our marketing campaigns."""
)

agent2 = Agent(
  role='Senior Data Researcher',
  goal='Uncover cutting-edge developments',
  backstory="""You're a meticulous analyst with a keen eye for detail. You're known for
    your ability to turn complex data into clear and concise reports, making
    it easy for others to understand and act on the information you provide."""
)


search_tool = SerperDevTool()

task1 = Task(
    description='Find and summarize the latest and most relevant news on AI',
    agent=agent1,
    expected_output='A bullet list summary of the top 5 most important AI news',
    # async_execution=True,
    tools=[search_tool],
    callback=callback_function
)

task2 = Task(
    description='Find and summarize the latest AI news',
    expected_output='A bullet list summary of the top 5 most important AI news',
    output_file='outputs/ai_news_summary.txt',
    # async_execution=True,
    agent=agent2,
    tools=[search_tool],
    # context=[task1]
)


# Execute the crew
crew = Crew(
    agents=[agent1, agent2],
    tasks=[task1, task2],
    verbose=True
)

result = crew.kickoff()
print('result: ', result)
# Accessing the task output
task_output = task1.output

print(f"Task Description: {task_output.description}")
print(f"Task Summary: {task_output.summary}")
print(f"Raw Output: {task_output.raw}")
if task_output.json_dict:
    print(f"JSON Output: {json.dumps(task_output.json_dict, indent=2)}")
if task_output.pydantic:
    print(f"Pydantic Output: {task_output.pydantic}")