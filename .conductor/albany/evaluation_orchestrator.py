# Evaluation Orchestration Module

This module orchestrates the entire evaluation process, integrating all components of the framework.

## Responsibilities

1. **System Initialization**
   - Load configuration from config.json
   - Initialize evaluator LLM
   - Initialize RAG system connectors

2. **Data Loading**
   - Load test cases from data/test_cases.json
   - Process documents using document_processor.py
   - Prepare evaluation datasets

3. **Evaluation Execution**
   - Submit queries to RAG systems
   - Collect responses and contexts
   - Execute automated evaluation using metrics_framework.py

4. **Result Management**
   - Store raw results
   - Calculate aggregated metrics
   - Generate detailed reports

5. **Reporting**
   - Generate CSV reports
   - Create visualizations (future implementation)
   - Export results in various formats

## Workflow

1. **Setup Phase**
   - Load configuration
   - Initialize all components
   - Verify connections to RAG systems

2. **Data Preparation Phase**
   - Load and process test cases
   - Load and process documents
   - Create evaluation datasets

3. **Execution Phase**
   - For each RAG system:
     - For each test case:
       - Submit query
       - Collect response
       - Evaluate response
   - Aggregate results

4. **Reporting Phase**
   - Generate detailed reports
   - Export results
   - (Optional) Launch web interface for manual evaluation

## Usage

```python
from evaluation_orchestrator import EvaluationOrchestrator

# Initialize orchestrator
orchestrator = EvaluationOrchestrator()

# Run full evaluation
results = orchestrator.run_evaluation()

# Generate reports
orchestrator.generate_reports(results)
```