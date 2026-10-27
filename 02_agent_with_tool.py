"""
Workbook 2 - Giving an Agent a Tool
===================================

An LLM is great with words but can make mistakes with exact maths.
A TOOL is a normal Python function the agent is allowed to call.
Here we give our agent a calculator and a "word counter".

Setup:
    pip install crewai
    set OPENAI_API_KEY (or GEMINI_API_KEY)

Run:
    python 02_agent_with_tool.py
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
from crewai import Agent, Task, Crew, LLM
from crewai.tools import tool

llm = (
    LLM(model="gemini/gemini-2.5-flash")
    if os.getenv("GEMINI_API_KEY")
    else LLM(model="gpt-4o-mini")
)


# ------------------------------------------------------------
# STEP 1: Write tools. The docstring tells the agent WHEN to use it.
# ------------------------------------------------------------
@tool("Calculator")
def calculator(expression: str) -> str:
    """Solves a maths expression such as '25 * 4 + 10' and returns the answer."""
    allowed = set("0123456789+-*/(). %")
    if not set(expression) <= allowed:
        return "Only numbers and + - * / ( ) % are allowed."
    try:
        return str(eval(expression))  # safe: we only allowed maths characters
    except Exception as e:
        return f"Error: {e}"


@tool("Word Counter")
def word_counter(text: str) -> str:
    """Counts how many words are in a piece of text."""
    return f"{len(text.split())} words"


# ------------------------------------------------------------
# STEP 2: Give the tools to the agent
# ------------------------------------------------------------
maths_helper = Agent(
    role="Maths Homework Helper",
    goal="Solve word problems step by step and always check numbers with the Calculator",
    backstory="You are patient and never guess a number - you always calculate it.",
    tools=[calculator, word_counter],
    llm=llm,
    verbose=True,
)

problem_task = Task(
    description=(
        "Solve this problem: {problem}\n"
        "Show each step. Use the Calculator tool for every calculation."
    ),
    expected_output="Step-by-step solution with the final answer in bold.",
    agent=maths_helper,
)

crew = Crew(agents=[maths_helper], tasks=[problem_task], verbose=True)

if __name__ == "__main__":
    problem = (
        "A school bus carries 48 students per trip. 1,250 students need to go "
        "to a science fair. How many trips are needed, and how many students "
        "are on the last trip?"
    )
    result = crew.kickoff(inputs={"problem": problem})
    print("\n================ FINAL ANSWER ================\n")
    print(result.raw)

# ------------------------------------------------------------
# TRY IT YOURSELF
#  1. Write a new tool  @tool("Celsius to Fahrenheit")  and give it to the agent.
#  2. Remove tools=[...] and compare: does the agent still get the maths right?
# ------------------------------------------------------------
