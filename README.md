# NetHandle
Revolutionizing your digital life by transforming the way you interact with the internet. Making it effortless and intelligent.

## Run Project
```
pip install -r requirements.txt

streamlit run app.py
```

### Project Structure

```
net_handle/
├── README.md
├── requirements.txt       # Dependencies (e.g., Streamlit, LangChain, LlamaIndex, apscheduler, etc.)
├── app.py                 # Main Streamlit app entry point
├── config.py              # Configuration settings (e.g., agent intervals, API keys)
├── agents/                # Directory for agent-specific code
│   ├── __init__.py
│   ├── base_agent.py      # Base class for agents using LangChain and LlamaIndex
│   ├── shopping_agent.py  # Specific agent for shopping tasks
│   ├── events_agent.py    # Specific agent for event-finding tasks
│   └── query_prompts.py   # Contains LLM prompt templates for agents
├── backend/               # Backend logic for managing and orchestrating agents
│   ├── __init__.py
│   ├── agent_manager.py   # Manages active/sleeper agent states
│   ├── scheduler.py       # Handles sleeper agent scheduling (periodic checks)
│   └── data_fetcher.py    # Utilities for fetching and parsing external data sources
├── index/                 # LlamaIndex-specific files for building and maintaining indices
│   ├── __init__.py
│   ├── index_manager.py   # Creates, updates, and queries LlamaIndex indices
│   └── indices/           # Stores the index files or references to index structures
├── frontend/              # Streamlit components for UI layout and interactivity
│   ├── __init__.py
│   ├── layout.py          # Defines Streamlit layout and UI elements
│   └── components.py      # Custom components (e.g., dropdowns, notification panels)
└── tests/                 # Test cases for validating project components
    ├── __init__.py
    ├── test_agents.py     # Tests for agent functionality
    ├── test_scheduler.py  # Tests for scheduler logic
    ├── test_index.py      # Tests for LlamaIndex operations
    └── test_frontend.py   # Tests for frontend Streamlit components

```
