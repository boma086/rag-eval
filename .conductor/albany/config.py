import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenRouter Configuration for Evaluation LLM
EVALUATOR_CONFIG = {
    "api_key": os.getenv("OPENROUTER_API_KEY"),
    "base_url": os.getenv("EVALUATOR_BASE_URL", "https://openrouter.ai/api/v1"),
    "model": os.getenv("EVALUATOR_MODEL", "gpt-3.5-turbo")
}

# RAG System Configurations
RAGFLOW_CONFIG = {
    "api_key": os.getenv("RAGFLOW_API_KEY"),
    "base_url": os.getenv("RAGFLOW_BASE_URL")
}

DIFY_CONFIG = {
    "api_key": os.getenv("DIFY_API_KEY"),
    "base_url": os.getenv("DIFY_BASE_URL")
}