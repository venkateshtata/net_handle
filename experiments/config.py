# config.py
import os
import experiments.constants as cons

# Groq API key
GROQ_API_KEY = os.getenv(cons.GROQ_API_KEY)

# Set SERP API key here or load it from environment variables
SERP_API_KEY = os.getenv(cons.SERP_API_KEY)
