# Frequently Asked Questions

## General Questions

### What is the RAG Evaluation Framework?

The RAG Evaluation Framework is a comprehensive solution designed to evaluate the effectiveness of Retrieval-Augmented Generation (RAG) systems in the context of Japanese software development. It assesses how well RAG systems can leverage historical basic design documents to provide guidance and recommendations for new development tasks.

### Who should use this framework?

This framework is intended for:
- Software development teams using RAG systems
- AI/ML engineers evaluating RAG performance
- Technical leads making decisions about RAG system adoption
- Researchers working on RAG evaluation methodologies

### What RAG systems does the framework support?

The framework is designed to be extensible, but currently includes connectors for:
- RagFlow
- Dify

Additional RAG systems can be added by implementing connectors following the provided interface.

## Technical Questions

### What programming language is the framework written in?

The framework is written in Python 3.8 or higher.

### What are the system requirements?

- Python 3.8 or higher
- At least 8GB RAM (recommended)
- 20GB free disk space for documents and results
- An OpenRouter API key
- Access to RAG systems you want to evaluate

### How do I install the framework?

1. Clone or download the repository
2. Create a Python virtual environment
3. Install dependencies using `pip install -r requirements.txt`

### How do I configure the framework?

1. Copy `.env.example` to `.env` and add your API keys
2. Update `config.json` with your RAG system endpoints
3. Place your historical documents in the `data/` directory
4. Update `data/test_cases.json` with your test scenarios

## Evaluation Questions

### What metrics does the framework evaluate?

The framework evaluates both standard and custom metrics:

Standard metrics (from Ragas):
- Faithfulness
- Answer Relevancy
- Context Recall
- Context Precision
- Answer Correctness

Custom metrics:
- Technical Accuracy
- Domain Relevance
- Language Appropriateness

Advanced metrics:
- Consistency Score
- Novelty Score
- Cultural Appropriateness
- Implementation Feasibility

### How does automated evaluation work?

Automated evaluation uses LLMs to score RAG responses based on predefined criteria. The framework:
1. Submits test cases to RAG systems
2. Collects responses and retrieved contexts
3. Uses an evaluator LLM (configured via OpenRouter) to score responses
4. Calculates metrics based on these scores

### How does manual evaluation work?

Manual evaluation uses a web interface where human evaluators:
1. Review test cases and ground truth answers
2. Examine responses from different RAG systems
3. Score each response for multiple metrics
4. Provide textual feedback for each score

### Can I use both automated and manual evaluation?

Yes, the framework supports a hybrid approach that combines both automated and manual evaluation. This allows for validation of automated scores against human judgment and provides flexibility to choose the evaluation method per test case.

## Document Processing Questions

### What document formats are supported?

The framework supports:
- Text files (.txt)
- PDF documents (.pdf)
- Word documents (.docx)
- Excel spreadsheets (.xlsx, .xls)
- Images (.jpg, .png) with OCR support

### How are Japanese documents handled?

The framework properly handles Japanese text encoding and can process documents written in Japanese. For image-based Japanese documents, OCR processing is used to extract text.

### How do I add support for a new document format?

To add support for a new document format:
1. Extend the `document_processor.py` module
2. Implement parsing logic for the new format
3. Add required dependencies to `requirements.txt`
4. Update documentation

## RAG System Integration Questions

### How do I add a new RAG system?

To add a new RAG system:
1. Create a new connector in the `connectors/` directory
2. Implement the methods defined in `rag_system_interface.py`
3. Add configuration options in `config.json`
4. Update the interface factory in `rag_system_interface.py`

### What if my RAG system doesn't have an API?

If your RAG system doesn't have an API, you can:
1. Implement a connector that interacts with the system through its available interface (e.g., command line, file system)
2. Create a wrapper that exposes an API for the system
3. Modify the framework to work with your specific integration method

## Results and Reporting Questions

### What kind of reports does the framework generate?

The framework generates:
- Detailed CSV reports with metrics for each test case
- Comprehensive PDF reports with analysis and visualizations
- Excel spreadsheets with detailed results
- Charts and graphs of key metrics

### How are results analyzed?

Results are analyzed using:
- Statistical analysis (mean, median, standard deviation)
- Comparative analysis between different RAG systems
- Trend analysis over time (for continuous evaluation)
- Anomaly detection for identifying outliers

### Can I export results to other formats?

Yes, the framework can be extended to export results to other formats. Currently supported formats include CSV, Excel, JSON, and PDF. Additional formats can be added by extending the reporting module.

## Continuous Evaluation Questions

### What is continuous evaluation?

Continuous evaluation allows for ongoing monitoring of RAG system performance by running evaluations at regular intervals.

### How do I set up continuous evaluation?

1. Configure evaluation schedules in `config.json`
2. Run the continuous evaluator with `python continuous_evaluator.py`

### What kind of monitoring does continuous evaluation provide?

Continuous evaluation provides:
- Regular performance metrics tracking
- Performance trend analysis over time
- Alerts on significant performance changes
- A/B testing capabilities for comparing system versions

## Troubleshooting Questions

### I'm getting API key errors. What should I do?

1. Verify that your API keys are correctly set in the `.env` file
2. Check that your API keys have the necessary permissions
3. Ensure that API endpoints are correctly configured
4. Verify that your OpenRouter account has sufficient credits

### Document processing is failing. How can I fix this?

1. Check that your documents are in supported formats
2. Verify that document encodings are correct
3. Look for specific error messages in the application logs
4. Try processing a simple test document to isolate the issue

### Evaluation results seem incorrect. What could be wrong?

1. Check that your test cases are correctly formatted
2. Verify that ground truth data is accurate
3. Ensure that RAG systems are properly configured and accessible
4. Review the evaluation metrics to ensure they're appropriate for your use case

## Contribution Questions

### How can I contribute to the framework?

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write or update tests as needed
5. Ensure all tests pass
6. Commit your changes with a clear, descriptive commit message
7. Push to your fork
8. Create a pull request to the main repository

### What are the coding standards?

The project follows these coding standards:
- PEP 8 for Python code style
- Google Python Style Guide for docstrings
- Type hints for all function parameters and return values
- Comprehensive unit tests for all functionality

### How do I report bugs or request features?

1. Check existing issues to see if your bug or feature request already exists
2. If not, create a new issue with:
   - A clear, descriptive title
   - A detailed description of the bug or feature
   - Steps to reproduce (for bugs)
   - Expected behavior
   - Actual behavior (for bugs)