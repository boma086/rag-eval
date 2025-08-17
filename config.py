# RAG Evaluation System - 多配置文件支持

import os
import glob
from dotenv import load_dotenv
from pathlib import Path

def load_all_env_files():
    """加载所有配置文件"""
    # 加载默认.env文件
    if Path(".env").exists():
        load_dotenv(".env")

    # 加载所有.env.local.*文件
    config_files = glob.glob(".env.local.*")
    for config_file in sorted(config_files):
        print(f"📁 Loading config: {config_file}")
        load_dotenv(config_file, override=True)  # override=True 允许覆盖已有变量

    if config_files:
        print(f"✅ Loaded {len(config_files)} configuration files")
    else:
        print("ℹ️  No .env.local.* files found, using default .env")

# 加载所有配置文件
load_all_env_files()

# 评价器配置 (用于评分的LLM)
EVALUATOR_CONFIG = {
    "api_key": os.getenv("OPENROUTER_API_KEY"),
    "base_url": os.getenv("EVALUATOR_BASE_URL", "https://openrouter.ai/api/v1"),
    "model": os.getenv("EVALUATOR_MODEL", "gpt-3.5-turbo"),
    "ollama_base_url": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
    "ollama_embedding_model": os.getenv("OLLAMA_EMBEDDING_MODEL", "nomic-embed-text:latest")
}

# RAG系统配置 - 支持的RAG系统
RAG_SYSTEMS = {
    "ragflow": {
        "enabled": os.getenv("RAGFLOW_ENABLED", "false").lower() == "true",
        "api_key": os.getenv("RAGFLOW_API_KEY"),
        "base_url": os.getenv("RAGFLOW_BASE_URL"),
        "chat_id": os.getenv("RAGFLOW_CHAT_ID"),  # 可选，自动检测
    },
    "dify": {
        "enabled": os.getenv("DIFY_ENABLED", "true").lower() == "true",
        "api_key": os.getenv("DIFY_API_KEY"),
        "base_url": os.getenv("DIFY_BASE_URL"),
        "app_id": os.getenv("DIFY_APP_ID"),
        "user_id": os.getenv("DIFY_USER_ID", "rag-evaluator"),
    }
}

# 获取启用的RAG系统
def get_enabled_rag_systems():
    """返回所有启用的RAG系统配置"""
    return {name: config for name, config in RAG_SYSTEMS.items() if config.get("enabled", False)}

# 验证配置完整性
def validate_config():
    """验证必要的配置是否完整"""
    errors = []
    
    # 检查评价器配置
    if not EVALUATOR_CONFIG.get("api_key"):
        errors.append("OPENROUTER_API_KEY is required")
    
    # 检查启用的RAG系统
    enabled_systems = get_enabled_rag_systems()
    if not enabled_systems:
        errors.append("At least one RAG system must be enabled")
    
    # 检查每个启用的RAG系统配置
    for name, config in enabled_systems.items():
        if not config.get("api_key"):
            errors.append(f"{name.upper()}_API_KEY is required")
        if not config.get("base_url"):
            errors.append(f"{name.upper()}_BASE_URL is required")
    
    return errors
