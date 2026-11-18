"""
Workbook 4 - A Crew with a Manager (Hierarchical Process)
=========================================================

In Workbook 3 the tasks ran in a fixed order (sequential).
Here a MANAGER agent decides who should do what - like a class
monitor giving jobs to the right students.

Setup:
    pip install crewai
    set ANTHROPIC_API_KEY

Run:
    python 04_hierarchical_crew.py
"""

import os

# Load API keys from a .env file next to this script (if present)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

if not os.getenv("ANTHROPIC_API_KEY"):
    raise SystemExit(
        "No API key found. Copy .env.example to .env and add ANTHROPIC_API_KEY "
        "(see README.md)."
    )
from crewai import Agent, Task, Crew, Process, LLM

worker_llm = LLM(model="anthropic/claude-haiku-5-5")
manager_llm = LLM(model="anthropic/claude-sonnet-5-5")  # a stronger model is better for managing

# ------------------------------------------------------------
# Specialist agents (the manager is created automatically)
# ------------------------------------------------------------
planner = Agent(
    role="Trip Planner",
    goal="Make a day-by-day plan for a school trip",
    backstory="You plan safe and fun trips for students.",
    llm=worker_llm,
)

budget_expert = Agent(
    role="Budget Expert",
    goal="Estimate the cost per student in Indian Rupees",
    backstory="You are good with numbers and always find ways to save money.",
    llm=worker_llm,
)

safety_officer = Agent(
    role="Safety Officer",
    goal="List safety rules and a packing checklist",
    backstory="You make sure every student stays safe and prepared.",
    llm=worker_llm,
)

# ------------------------------------------------------------
# One big task. No 'agent=' here - the manager delegates it.
# ------------------------------------------------------------
trip_task = Task(
    description=(
        "Plan a {days}-day school trip to {place} for 40 students. "
        "Include a day-wise plan, a cost estimate per student, "
        "and safety rules with a packing checklist."
    ),
    expected_output="A complete trip guide with 3 clear sections: Plan, Budget, Safety.",
)

crew = Crew(
    agents=[planner, budget_expert, safety_officer],
    tasks=[trip_task],
    process=Process.hierarchical,
    manager_llm=manager_llm,
    verbose=True,
)

if __name__ == "__main__":
    result = crew.kickoff(inputs={"place": "Mysuru", "days": 2})
    print("\n================ TRIP GUIDE ================\n")
    print(result.raw)
