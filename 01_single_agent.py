"""
Workbook 1 - Your First CrewAI Agent (Single Agent)
====================================================

Goal: build ONE agent that explains any topic in simple words.

Setup (run once in your terminal):
    pip install crewai
    # Option A (OpenAI):  set OPENAI_API_KEY
    # Option B (Google Gemini, has a free tier): set GEMINI_API_KEY

    Windows (PowerShell):  $env:OPENAI_API_KEY="sk-..."
    Mac/Linux:             export OPENAI_API_KEY="sk-..."

Run:
    python 01_single_agent.py
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

# ------------------------------------------------------------
# STEP 1: Choose the "brain" (the LLM) for the agent
# ------------------------------------------------------------
if os.getenv("GEMINI_API_KEY"):
    llm = LLM(model="gemini/gemini-2.5-flash", temperature=0.3)
else:
    llm = LLM(model="gpt-4o-mini", temperature=0.3)  # uses OPENAI_API_KEY

# ------------------------------------------------------------
# STEP 2: Create the Agent  (WHO does the work)
#   role      -> the job title
#   goal      -> what it is trying to achieve
#   backstory -> its personality / experience
# ------------------------------------------------------------
teacher = Agent(
    role="Friendly Science Teacher",
    goal="Explain {topic} so that any school student can understand it",
    backstory=(
        "You have taught science for 15 years. You love using everyday "
        "examples like cricket, cooking and mobile phones to explain ideas."
    ),
    llm=llm,
    verbose=True,  # shows the agent's thinking in the terminal
)

# ------------------------------------------------------------
# STEP 3: Create the Task  (WHAT needs to be done)
# ------------------------------------------------------------
explain_task = Task(
    description=(
        "Explain the topic '{topic}' in simple language. "
        "Use one real-life example and finish with 3 quick quiz questions."
    ),
    expected_output=(
        "A short explanation (about 150 words), one example, "
        "and 3 quiz questions with answers."
    ),
    agent=teacher,
)

# ------------------------------------------------------------
# STEP 4: Put them in a Crew and start it (kickoff)
# ------------------------------------------------------------
crew = Crew(agents=[teacher], tasks=[explain_task], verbose=True)

if __name__ == "__main__":
    topic = input("Enter a topic (e.g. Photosynthesis): ") or "Photosynthesis"
    result = crew.kickoff(inputs={"topic": topic})

    print("\n================ FINAL ANSWER ================\n")
    print(result.raw)

# ------------------------------------------------------------
# TRY IT YOURSELF
#  1. Change the role to "Cricket Coach" and the topic to "Newton's laws".
#  2. Change temperature to 0.9 - does the answer become more creative?
#  3. Add  output_file="answer.md"  inside Task(...) to save the answer.
# ------------------------------------------------------------
