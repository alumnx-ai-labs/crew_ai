# CrewAI Workbooks

Four runnable Python scripts that teach CrewAI step by step.

| File | What it teaches | Asks for input? |
|------|-----------------|-----------------|
| `01_single_agent.py` | One agent that explains a topic in simple words | Yes: a topic |
| `02_agent_with_tool.py` | Giving an agent Python tools (calculator, word counter) | No |
| `03_multi_agent_crew.py` | Researcher, Writer and Editor agents working in sequence | Yes: a topic |
| `04_hierarchical_crew.py` | A manager agent that delegates work (trip-planner example) | No |

## Setup (one time)

You need Python 3.10+ and an **Anthropic** API key.

**Windows (PowerShell)**
```powershell
cd C:\Users\SRIRAM\Downloads\crewai_workbooks\crewai_workbooks
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

**Mac/Linux**
```bash
cd crewai_workbooks
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

If PowerShell blocks the activate script, run `Set-ExecutionPolicy -Scope Process Bypass` and retry.

## Add your API key

Open `.env` and add your key:

```
ANTHROPIC_API_KEY=sk-ant-your-key
```

The scripts load `.env` automatically and use Claude Haiku 5.5 (`anthropic/claude-haiku-5-5`), plus Claude Sonnet 5.5 as the manager in script 04. Never share or commit your `.env`.

## Run each file

Activate the virtual environment first (`.venv\Scripts\Activate.ps1`), then:

```powershell
python 01_single_agent.py
python 02_agent_with_tool.py
python 03_multi_agent_crew.py
python 04_hierarchical_crew.py
```

- **01**: prompts `Enter a topic`. Press Enter for the default (`Photosynthesis`).
- **02**: no input. To try your own problem, edit the `problem` variable near the bottom of the file.
- **03**: prompts for an article topic. Press Enter for the default (`Chandrayaan-3`). The Researcher, Writer and Editor produce a ~250-word article.
- **04**: no input. A manager plans a 2-day trip to Mysuru. To change it, edit `inputs={"place": "Mysuru", "days": 2}` near the bottom of the file.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `No API key found` | Open `.env` and add `ANTHROPIC_API_KEY` |
| `ModuleNotFoundError: No module named 'crewai'` | Activate `.venv`, then run `pip install -r requirements.txt` |
| `429` or quota error | You hit the free-tier rate limit. Wait a minute and retry |
| Script 04 is slow or costly | The manager makes extra LLM calls. This is normal for a hierarchical crew |
