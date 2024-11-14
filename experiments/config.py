# config.py
import os
import constants

# Groq API key
GROQ_API_KEY = os.getenv(constants.GROQ_API_KEY)

# Set SERP API key here or load it from environment variables
SERP_API_KEY = os.getenv(constants.SERP_API_KEY)
