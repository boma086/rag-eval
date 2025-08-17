# RAG System Interface

This module defines a unified interface for interacting with different RAG systems like RagFlow and Dify.

## Interface Design

The interface provides methods for:
1. Initializing connections to RAG systems
2. Submitting queries/questions
3. Retrieving responses and contexts
4. Handling authentication and error cases

## Supported RAG Systems

1. **RagFlow**
   - Connector implementation: connectors/ragflow.py
   - API documentation: [Link to RagFlow API docs]

2. **Dify**
   - Connector implementation: connectors/dify.py
   - API documentation: [Link to Dify API docs]

## Usage Example

```python
from rag_system_interface import RAGSystemInterface

# Initialize RagFlow
ragflow = RAGSystemInterface('ragflow', api_key='your_key', base_url='endpoint')

# Initialize Dify
dify = RAGSystemInterface('dify', api_key='your_key', base_url='endpoint')

# Submit a query to both systems
question = "How should we implement user authentication?"
ragflow_response = ragflow.query(question)
dify_response = dify.query(question)

# Responses will include:
# - answer: The generated response
# - contexts: Retrieved context documents
# - metadata: Processing time, model used, etc.
```

## Response Format

All RAG systems will return responses in a standardized format:
{
  "answer": "The generated answer text",
  "contexts": ["context1", "context2", ...],
  "metadata": {
    "processing_time": 1.23,
    "model_used": "model_name",
    "timestamp": "2023-01-01T00:00:00Z"
  }
}