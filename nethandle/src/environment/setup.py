import getpass
import os

def set_env_var(var: str):
    """Prompt for environment variables if not already set."""
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"Please provide your {var}")

def setup_environment():
    """Setup required environment variables."""
    set_env_var("OPENAI_API_KEY")
    set_env_var("TAVILY_API_KEY")
