"""
Workbook 3 - A Team of Agents (Multi-Agent Crew)
================================================

Just like a school magazine team:
    Researcher  -> collects facts
    Writer      -> turns facts into an article
    Editor      -> checks and polishes the article

Each agent does ONE job well, and passes its work to the next.

Setup:
    pip install crewai
    set OPENAI_API_KEY (or GEMINI_API_KEY)

Run:
    python 03_multi_agent_crew.py
"""

import os

# Load API keys from a .env file next to this script (if present)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

if not (os.getenv("GEMINI_API_KEY") or os.getenv("OPENAI_API_KEY")):
    raise SystemExit(
        "No API key found. Copy .env.example to .env and add GEMINI_API_KEY "
        "or OPENAI_API_KEY (see README.md)."
    )
from crewai import Agent, Task, Crew, Process, LLM

llm = (
    LLM(model="gemini/gemini-2.5-flash", temperature=0.4)
    if os.getenv("GEMINI_API_KEY")
    else LLM(model="gpt-4o-mini", temperature=0.4)
)

# ------------------------------------------------------------
# STEP 1: Create the team (3 agents)
# ------------------------------------------------------------
researcher = Agent(
    role="Researcher",
    goal="Collect the 5 most important and correct facts about {topic}",
    backstory="You are curious and careful. You only share facts you are sure about.",
    llm=llm,
    verbose=True,
)

writer = Agent(
    role="Magazine Writer",
    goal="Write a fun, easy-to-read article about {topic} using the researcher's facts",
    backstory="You write for a school magazine. Your articles are short, clear and exciting.",
    llm=llm,
    verbose=True,
)

editor = Agent(
    role="Editor",
    goal="Make the article correct, clear and well formatted",
    backstory="You fix grammar, remove confusing sentences and add a catchy title.",
    llm=llm,
    verbose=True,
)

# ------------------------------------------------------------
# STEP 2: Create the tasks. 'context' passes one task's output to the next.
# ------------------------------------------------------------
research_task = Task(
    description="Find 5 key facts about {topic}. Add one surprising fact.",
    expected_output="A numbered list of 5 facts plus 1 surprising fact.",
    agent=researcher,
)

write_task = Task(
    description="Write a 250-word article on {topic} using the research.",
    expected_output="A 250-word article with an intro, body and conclusion.",
    agent=writer,
    context=[research_task],  # writer receives researcher's output
)

edit_task = Task(
    description="Proofread the article, add a catchy title and 3 subheadings.",
    expected_output="Final polished article in Markdown format.",
    agent=editor,
    context=[write_task],  # editor receives writer's output
    output_file="final_article.md",  # saves the final result to a file
)

# ------------------------------------------------------------
# STEP 3: Build the crew.
#   Process.sequential -> tasks run one by one, in order
# ------------------------------------------------------------
crew = Crew(
    agents=[researcher, writer, editor],
    tasks=[research_task, write_task, edit_task],
    process=Process.sequential,
    verbose=True,
)

if __name__ == "__main__":
    topic = input("Article topic (e.g. Chandrayaan-3): ") or "Chandrayaan-3"
    result = crew.kickoff(inputs={"topic": topic})

    print("\n================ FINAL ARTICLE ================\n")
    print(result.raw)

    print("\n--------- What each agent produced ---------")
    for t in result.tasks_output:
        print(f"\n[{t.agent}]\n{t.raw[:300]}...")

    print("\nSaved to final_article.md")
    print("Tokens used:", result.token_usage)

# ------------------------------------------------------------
# TRY IT YOURSELF
#  1. Add a 4th agent "Quiz Maker" that creates 5 MCQs from the final article.
#  2. Change the topic to your favourite sport or film.
# ------------------------------------------------------------
