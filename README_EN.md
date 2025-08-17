# RAG Multi-Evaluator System

A professional evaluation framework for RAG (Retrieval-Augmented Generation) systems, supporting comprehensive assessment with multiple evaluators and RAG systems.

## 🌐 **Language / 言語**

- **English** (This document)
- [中文文档](README_CN.md)
- [日本語ドキュメント](README_JP.md)

## 🎯 **Key Features**

### 📊 **Multi-Evaluator Architecture**
- **Ragas Evaluator** - True Ragas framework (OpenRouter Chat + Ollama Embeddings)
- **Ragas Alternative** - LLM-based evaluation mimicking Ragas standards
- **Simple Evaluator** - Basic relevancy and correctness evaluation
- **Academic Evaluator** - 4-dimensional professional evaluation (relevancy, correctness, completeness, clarity)

### 🔌 **RAG System Support**
- **Dify** - Enterprise RAG platform
- **RagFlow** - Open-source RAG solution
- **Universal Connector** - Support for OpenAI-compatible APIs

### 🏗️ **Design Patterns**
- **Factory Pattern** - Unified evaluator creation and management
- **Strategy Pattern** - Flexible evaluation strategy selection
- **Adapter Pattern** - Unified RAG system interface

## 🚀 **Quick Start**

### 1. Environment Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Create configuration files from examples:

```bash
# Copy evaluator configuration
cp config_examples/evaluator_openrouter_ollama.env .env.local.evaluator

# Copy RAG system configuration
cp config_examples/rag_dify.env .env.local.dify

# Edit with your API keys
nano .env.local.evaluator
nano .env.local.dify
```

### 3. Start Ollama Service

```bash
# Install and start Ollama
ollama serve

# Pull embedding model
ollama pull nomic-embed-text:latest
```

### 4. Run Evaluation

```bash
# Run multi-evaluator assessment
python main_multi_eval.py

# View results with intuitive scoring
python score_viewer.py
```

## 📊 **Evaluation Results**

The system provides intuitive scoring with grades:

- 🏆 **Excellent** (0.9+)
- 🥇 **Good** (0.8+)  
- 🥈 **Average** (0.7+)
- 🥉 **Pass** (0.6+)
- ❌ **Needs Improvement** (<0.6)

Example output:
```
🎯 RAG System Evaluation Overview
📊 RAG Systems: dify
🔍 Evaluators: academic, ragas, simple
❓ Test Questions: 3

🔵 DIFY System Evaluation
  📊 academic evaluator:
    relevancy: 0.800 🥇 Good
    correctness: 0.700 🥉 Pass
    📈 Overall Score: 0.800 🥇 Good
  
  🎯 dify system overall: 0.690 🥉 Pass
```

## 🔧 **Configuration Examples**

The `config_examples/` directory contains configuration templates for various services:

### Evaluator Configurations
- `evaluator_openrouter_ollama.env` - OpenRouter + Ollama (Recommended)
- `evaluator_openai.env` - OpenAI API
- `evaluator_gemini_ollama.env` - Google Gemini + Ollama
- `evaluator_ollama_only.env` - Pure Ollama setup

### RAG System Configurations  
- `rag_dify.env` - Dify platform
- `rag_universal_openai.env` - Any OpenAI-compatible API

## 🏗️ **Project Structure**

```
ragas/
├── evaluators/                 # Evaluator modules
│   ├── factory.py              # Factory pattern implementation
│   ├── ragas_ollama.py         # True Ragas evaluator
│   └── ...
├── connectors/                 # RAG system connectors
│   ├── universal.py            # Universal OpenAI-compatible connector
│   └── ...
├── config_examples/            # Configuration templates
├── data/                       # Test datasets
└── results/                    # Evaluation results
```

## 🔍 **Usage Examples**

### Programmatic Interface

```python
from evaluators.factory import EvaluatorManager
from config import EVALUATOR_CONFIG

# Initialize evaluator manager
manager = EvaluatorManager(EVALUATOR_CONFIG)

# Prepare evaluation data
questions = ["How to implement user authentication?"]
answers = ["Use OAuth 2.0 and JWT tokens."]
ground_truths = ["Recommend OAuth 2.0 and JWT for secure authentication."]

# Run evaluation
results = manager.evaluate_all(questions, answers, ground_truths)
print(results)
```

### Command Line Usage

```bash
# Use custom test cases
python main_multi_eval.py --test-cases data/my_test_cases.json

# Specify output directory
python main_multi_eval.py --output my_results/
```

## 🛠️ **Troubleshooting**

### Common Issues

1. **405 Error** - Model type error
   - Ensure using Chat model, not Embedding model
   - Check model name has correct prefix (e.g., `openai/gpt-4`)

2. **Embeddings Error** - `'str' object has no attribute 'data'`
   - OpenRouter doesn't support Embeddings API
   - Use Ollama for Embeddings service

3. **Connection Timeout**
   - Check network connection
   - Increase timeout settings

### Debug Mode

```bash
# Enable verbose logging
export PYTHONPATH=.
python -c "
from evaluators.factory import EvaluatorFactory
info = EvaluatorFactory.get_evaluator_info()
print(info)
"
```

## 🤝 **Contributing**

1. Fork the project
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 **Acknowledgments**

- [Ragas](https://github.com/explodinggradients/ragas) - RAG evaluation framework
- [Ollama](https://ollama.ai/) - Local LLM service
- [OpenRouter](https://openrouter.ai/) - LLM API service
