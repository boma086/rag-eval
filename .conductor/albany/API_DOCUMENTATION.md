# API Documentation

This document provides documentation for the RAG Evaluation Framework's API.

## Configuration API

### Environment Variables

The framework uses environment variables for configuration. These are loaded from the `.env` file.

#### Required Variables

- `OPENROUTER_API_KEY`: Your OpenRouter API key for accessing language models
- `EVALUATOR_MODEL`: The model to use for evaluation (default: "gpt-3.5-turbo")
- `EVALUATOR_BASE_URL`: The base URL for the evaluator API (default: "https://openrouter.ai/api/v1")

#### RAG System Variables

- `RAGFLOW_API_KEY`: API key for RagFlow
- `RAGFLOW_BASE_URL`: Base URL for RagFlow API
- `DIFY_API_KEY`: API key for Dify
- `DIFY_BASE_URL`: Base URL for Dify API

### Configuration File

The `config.json` file provides additional configuration options:

```json
{
  "project_name": "RAG Evaluation Framework for Japanese Software Development",
  "version": "1.0.0",
  "configuration": {
    "evaluator": {
      "provider": "openrouter",
      "model": "gpt-3.5-turbo",
      "base_url": "https://openrouter.ai/api/v1"
    },
    "rag_systems": {
      "ragflow": {
        "enabled": true,
        "base_url": "your_ragflow_endpoint"
      },
      "dify": {
        "enabled": true,
        "base_url": "your_dify_endpoint"
      }
    }
  }
}
```

## Test Case API

### Test Case Format

Test cases are stored in `data/test_cases.json` as an array of objects with the following structure:

```json
{
  "id": 1,
  "question": "How should we implement user authentication?",
  "ground_truth": "Implement OAuth 2.0 with JWT tokens for secure authentication.",
  "tags": ["security", "authentication"]
}
```

### Loading Test Cases

```python
from evaluate_rag import load_test_cases

test_cases = load_test_cases("data/test_cases.json")
```

## Document Processing API

### Loading Documents

```python
from document_processor import load_documents

documents = load_documents("data/")
```

### Supported Formats

The document processor supports:
- Text files (.txt)
- PDF documents (.pdf)
- Word documents (.docx)
- Excel spreadsheets (.xlsx, .xls)
- Images (.jpg, .png) with OCR support

## RAG System Interface API

### Initializing RAG Systems

```python
from rag_system_interface import RAGSystemInterface

ragflow = RAGSystemInterface('ragflow', api_key='your_key', base_url='endpoint')
dify = RAGSystemInterface('dify', api_key='your_key', base_url='endpoint')
```

### Querying RAG Systems

```python
response = ragflow.query("How should we implement user authentication?")
```

### Response Format

All RAG systems return responses in a standardized format:

```json
{
  "answer": "The generated answer text",
  "contexts": ["context1", "context2", ...],
  "metadata": {
    "processing_time": 1.23,
    "model_used": "model_name",
    "timestamp": "2023-01-01T00:00:00Z"
  }
}
```

## Evaluation API

### Running Evaluations

```python
from evaluate_rag import evaluate_rag_pipeline
from ragas.metrics import AnswerCorrectness, Faithfulness, AnswerRelevancy

# Define metrics
metrics = [
    AnswerCorrectness(),
    Faithfulness(),
    AnswerRelevancy()
]

# Run evaluation
results = evaluate_rag_pipeline(dataset, metrics)
```

### Evaluation Metrics

#### Standard Ragas Metrics

- `AnswerCorrectness()`: Combines semantic similarity and factual accuracy
- `Faithfulness()`: Measures if the answer is factual based on the given context
- `AnswerRelevancy()`: Evaluates how relevant the answer is to the question
- `ContextRecall()`: Assesses the retrieval mechanism's ability to return all relevant information
- `ContextPrecision()`: Measures the signal-to-noise ratio of retrieved context

#### Custom Metrics

Custom metrics can be implemented by inheriting from the base metric classes in `metrics_framework.py`.

### Dataset Format

The evaluation function expects a dataset in the following format:

```python
data_samples = {
    "question": ["How should we implement user authentication?"],
    "answer": ["Based on our previous projects, implement OAuth 2.0..."],
    "contexts": [["In our previous project, we implemented OAuth 2.0..."]],
    "ground_truth": ["For user authentication, implement OAuth 2.0..."]
}
```

## Results API

### Saving Results

```python
import pandas as pd

# Convert results to pandas DataFrame
df = results.to_pandas()

# Save to CSV
df.to_csv("results/evaluation_results.csv", index=False)
```

### Loading Results

```python
import pandas as pd

# Load results from CSV
df = pd.read_csv("results/evaluation_results.csv")
```

## Reporting API

### Generating Reports

```python
from results_analyzer import ResultsAnalyzer

# Initialize analyzer
analyzer = ResultsAnalyzer('results/evaluation_results.csv')

# Generate reports
analyzer.generate_pdf_report('reports/evaluation_report.pdf')
analyzer.export_to_excel('reports/evaluation_results.xlsx')
```

## Continuous Evaluation API

### Scheduling Evaluations

```python
from continuous_evaluator import ContinuousEvaluator

# Initialize continuous evaluator
evaluator = ContinuousEvaluator()

# Schedule daily evaluations
evaluator.schedule_evaluation('daily', '0 0 * * *')

# Start monitoring
evaluator.start_monitoring()
```

### Running A/B Tests

```python
# Run A/B test
evaluator.run_ab_test('ragflow_v1', 'ragflow_v2', duration_days=7)
```

## Manual Evaluation API

### Launching Manual Evaluation Interface

```bash
python main.py --mode manual
```

The manual evaluation interface provides a web-based UI for human evaluators to:
- Review test cases
- Compare responses from different RAG systems
- Score responses manually
- Provide textual feedback

## Error Handling

The framework uses standard Python exception handling. Common exceptions include:

- `FileNotFoundError`: When required files are missing
- `ValueError`: When data is in an incorrect format
- `ConnectionError`: When there are issues connecting to APIs
- `KeyError`: When required configuration values are missing

All API functions should be called within appropriate try/except blocks to handle these exceptions gracefully.