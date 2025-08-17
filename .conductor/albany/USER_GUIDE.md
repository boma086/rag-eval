# User Guide

This document provides instructions for users of the RAG Evaluation Framework.

## Getting Started

### Prerequisites

1. Python 3.8 or higher installed on your system
2. An OpenRouter API key (sign up at https://openrouter.ai/)
3. Access to RAG systems you want to evaluate (RagFlow, Dify, etc.)

### Installation

1. Clone or download the repository:
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

2. Edit the `.env` file and add your API keys:
   ```
   OPENROUTER_API_KEY=your_openrouter_api_key
   RAGFLOW_API_KEY=your_ragflow_api_key
   DIFY_API_KEY=your_dify_api_key
   ```

3. Update `config.json` with your RAG system endpoints if needed.

## Preparing Evaluation Data

### Document Preparation

Place your historical design documents in the `data/` directory. The framework supports:
- Text files (.txt)
- PDF documents (.pdf)
- Word documents (.docx)
- Excel spreadsheets (.xlsx, .xls)
- Images (.jpg, .png) with OCR support

### Test Case Creation

Update `data/test_cases.json` with your test scenarios. Each test case should include:
- A unique ID
- A question or requirement
- Expected ground truth answer
- Tags for categorization

Example test case:
```json
{
  "id": 1,
  "question": "How should we implement user authentication in our new Japanese language learning app?",
  "ground_truth": "For the Japanese language learning app, implement OAuth 2.0 with JWT tokens for secure authentication, use bcrypt for password hashing, and implement multi-factor authentication for enhanced security based on our previous project experiences.",
  "tags": ["security", "authentication"]
}
```

## Running Evaluations

### Automated Evaluation

To run automated evaluation:

```bash
python main.py --mode auto
```

This will:
1. Load test cases from `data/test_cases.json`
2. Process documents in the `data/` directory
3. Submit queries to configured RAG systems
4. Evaluate responses using both standard and custom metrics
5. Save results to the `results/` directory

### Manual Evaluation

To run the manual evaluation interface:

```bash
python main.py --mode manual
```

This will launch a web interface where you can:
1. Review test cases
2. Compare responses from different RAG systems
3. Score responses manually
4. Provide textual feedback

### Combined Evaluation

To run both automated and manual evaluation:

```bash
python main.py --mode both
```

## Understanding Results

### Result Files

After running evaluations, results are saved in the `results/` directory:
- `evaluation_results.csv`: Detailed metrics for each test case
- `summary.json`: Summary statistics for all evaluations

### Key Metrics

1. **Faithfulness**: Measures if the answer is factual based on the given context (0.0-1.0)
2. **Answer Relevancy**: Evaluates how relevant the answer is to the question (0.0-1.0)
3. **Context Recall**: Assesses the retrieval mechanism's ability to return all relevant information (0.0-1.0)
4. **Context Precision**: Measures the signal-to-noise ratio of retrieved context (0.0-1.0)
5. **Answer Correctness**: Combines semantic similarity and factual accuracy (0.0-1.0)
6. **Technical Accuracy**: Evaluates technical correctness in software development context (0.0-1.0)
7. **Domain Relevance**: Measures relevance to Japanese software development (0.0-1.0)

## Generating Reports

Reports are generated in the `reports/` directory:
- `evaluation_report.pdf`: Comprehensive PDF report with analysis
- `evaluation_results.xlsx`: Excel spreadsheet with detailed results
- `visualization.png`: Charts and graphs of key metrics

## Continuous Evaluation

To set up continuous evaluation:

1. Configure evaluation schedules in `config.json`
2. Run the continuous evaluator:
   ```bash
   python continuous_evaluator.py
   ```

This will:
- Run evaluations at configured intervals
- Track performance over time
- Alert on significant changes

## Troubleshooting

### Common Issues

1. **API Key Errors**:
   - Verify API keys in `.env` file
   - Check API key permissions
   - Ensure API endpoints are correct

2. **Document Processing Issues**:
   - Check file formats and encodings
   - Verify document parsing logic
   - Look for specific error messages in logs

3. **Evaluation Issues**:
   - Check test case formatting
   - Verify ground truth data
   - Ensure RAG system connectivity

### Getting Help

If you encounter issues not covered in this guide:
1. Check the application logs for error messages
2. Review the documentation in README.md
3. Create an issue in the repository with detailed information about the problem