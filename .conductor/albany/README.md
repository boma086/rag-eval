# RAG Evaluation Framework for Japanese Software Development

## Overview

This project provides a comprehensive framework for evaluating RAG (Retrieval-Augmented Generation) systems in the context of Japanese software development. The framework is designed to assess how effectively RAG systems like RagFlow and Dify can leverage historical basic design documents to offer guidance and recommendations for new development tasks.

## Key Features

1. **Multi-Format Document Support**
   - Supports various document formats including TXT, PDF, DOCX, XLSX, and images
   - Implements OCR for image-based documents
   - Handles Japanese text encoding appropriately

2. **Flexible Evaluation Metrics**
   - Standard metrics from Ragas library (Faithfulness, Answer Relevancy, etc.)
   - Custom metrics for technical accuracy and domain relevance
   - Advanced metrics for consistency and cultural appropriateness

3. **Multiple RAG System Integration**
   - Unified interface for RagFlow and Dify
   - Easy extensibility for other RAG systems
   - Standardized response format

4. **OpenRouter Integration**
   - Use OpenRouter API key to access various models (OpenAI, Gemini, etc.)
   - Configurable evaluator model selection
   - No need for direct OpenAI API key

5. **Comprehensive Test Management**
   - JSON-based test case management
   - Tag-based test case categorization
   - Ground truth for objective evaluation

6. **Automated and Manual Evaluation**
   - Automated evaluation using LLMs
   - Web-based interface for manual evaluation
   - Hybrid approach combining both methods

7. **Advanced Analysis and Reporting**
   - Statistical analysis of results
   - Data visualization capabilities
   - PDF and Excel report generation

8. **Continuous Evaluation**
   - Scheduled evaluations
   - Performance monitoring over time
   - A/B testing capabilities

## Project Structure

```
├── .env                      # Environment variables
├── config.py                 # Configuration loader
├── config.json               # Main configuration file
├── main.py                   # Application entry point
├── evaluate_rag.py           # Main evaluation script
├── evaluation_orchestrator.py # Evaluation process orchestrator
├── document_processor.py     # Multi-format document processor
├── metrics_framework.py      # Evaluation metrics framework
├── rag_system_interface.py   # Unified RAG system interface
├── results_analyzer.py       # Results analysis and reporting
├── continuous_evaluator.py   # Continuous evaluation module
├── manual_evaluation_interface.py # Web interface for manual evaluation
├── openrouter_integration.py # OpenRouter API integration
├── connectors/               # Directory for RAG system connectors
│   ├── ragflow.py            # RagFlow connector
│   └── dify.py               # Dify connector
├── metrics/                  # Directory for custom evaluation metrics
│   ├── technical_accuracy.py # Technical accuracy metric
│   ├── domain_relevance.py   # Domain relevance metric
│   ├── japanese_language_appropriateness.py # Language appropriateness metric
│   ├── advanced_metrics.py   # Advanced evaluation metrics
│   └── README.md             # Metrics documentation
├── data/                     # Directory for historical design documents and test cases
│   ├── sample_design_doc.txt # Sample design document
│   └── test_cases.json       # Test cases in JSON format
├── results/                  # Directory for storing evaluation results
│   └── README.md             # Results documentation
├── reports/                  # Directory for generated reports
│   └── README.md             # Reports documentation
└── requirements.txt          # Python dependencies
```

## Getting Started

### Prerequisites

- Python 3.8 or higher
- An OpenRouter API key (sign up at https://openrouter.ai/)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd ragas
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv ragas-env
   source ragas-env/bin/activate  # On Windows: ragas-env\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Configuration

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file and add your OpenRouter API key:
   ```
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   ```

3. Update `config.json` with your RAG system endpoints if needed.

### Data Preparation

1. Place your historical design documents in the `data/` directory.
2. Update `data/test_cases.json` with your test scenarios.

### Running Evaluations

1. Run automated evaluation:
   ```bash
   python main.py --mode auto
   ```

2. Run manual evaluation interface:
   ```bash
   python main.py --mode manual
   ```

3. Run both automated and manual evaluation:
   ```bash
   python main.py --mode both
   ```

## Documentation

- [Implementation Plan](IMPLEMENTATION_PLAN.md)
- [Project Summary](PROJECT_SUMMARY.md)
- [Metrics Framework](metrics_framework.py)
- [Document Processor](document_processor.py)
- [RAG System Interface](rag_system_interface.py)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.