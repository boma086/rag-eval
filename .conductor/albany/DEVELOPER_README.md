# Developer README

This document provides detailed information for developers who want to contribute to or extend the RAG Evaluation Framework.

## Project Architecture

The RAG Evaluation Framework follows a modular architecture with clearly defined components:

1. **Core Modules**:
   - `config.py`: Configuration management
   - `main.py`: Application entry point and CLI interface
   - `evaluation_orchestrator.py`: Coordinates the entire evaluation process

2. **Data Processing**:
   - `document_processor.py`: Handles various document formats
   - `data/`: Directory for test cases and documents

3. **RAG System Integration**:
   - `rag_system_interface.py`: Unified interface for all RAG systems
   - `connectors/`: Individual connectors for each RAG system

4. **Evaluation Engine**:
   - `evaluate_rag.py`: Main evaluation script
   - `metrics_framework.py`: Framework for evaluation metrics
   - `metrics/`: Custom and advanced evaluation metrics

5. **User Interface**:
   - `manual_evaluation_interface.py`: Web interface for manual evaluation

6. **Analysis and Reporting**:
   - `results_analyzer.py`: Statistical analysis of results
   - `continuous_evaluator.py`: Continuous evaluation features
   - `reports/`: Generated reports

## Setting Up Development Environment

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd ragas
   ```

2. **Create Virtual Environment**:
   ```bash
   python3 -m venv ragas-env
   source ragas-env/bin/activate  # On Windows: ragas-env\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Development Dependencies** (if applicable):
   ```bash
   pip install -r requirements-dev.txt
   ```

## Code Structure and Standards

### Naming Conventions

- Use `snake_case` for variables and functions
- Use `PascalCase` for classes
- Use `UPPER_CASE` for constants
- Use descriptive names that clearly indicate purpose

### Code Documentation

- All functions and classes should have docstrings
- Use Google Python Style Guide for docstrings
- Complex logic should have inline comments explaining the "why"

### Type Hints

- Use type hints for all function parameters and return values
- Use `typing` module for complex types

### Error Handling

- Use try/except blocks for expected exceptions
- Provide meaningful error messages
- Log errors appropriately

## Testing

### Unit Tests

- Each module should have corresponding unit tests
- Tests should be placed in `tests/` directory
- Use `pytest` for running tests

### Integration Tests

- Test the interaction between different components
- Test with actual RAG systems when possible
- Validate evaluation metrics accuracy

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_document_processor.py

# Run tests with coverage
pytest --cov=.
```

## Contributing

### Git Workflow

1. Fork the repository
2. Create a feature branch from `main`
3. Make your changes
4. Write or update tests as needed
5. Ensure all tests pass
6. Commit your changes with a clear, descriptive commit message
7. Push to your fork
8. Create a pull request to the main repository

### Pull Request Guidelines

- Each pull request should address a single feature or bug fix
- Include a clear description of the changes
- Reference any related issues
- Ensure all tests pass
- Follow the code style guidelines

### Code Review Process

- All pull requests must be reviewed by at least one other developer
- Reviewers will check for code quality, functionality, and adherence to guidelines
- Address all review comments before merging

## Extending the Framework

### Adding New RAG Systems

1. Create a new connector in the `connectors/` directory
2. Implement the methods defined in `rag_system_interface.py`
3. Add configuration options in `config.json`
4. Update the interface factory in `rag_system_interface.py`

### Adding New Evaluation Metrics

1. Create a new metric file in the `metrics/` directory
2. Inherit from the appropriate base class in `metrics_framework.py`
3. Implement the calculation logic
4. Add the metric to the evaluation pipeline

### Adding New Document Formats

1. Extend the `document_processor.py` module
2. Implement parsing logic for the new format
3. Add required dependencies to `requirements.txt`
4. Update documentation

## Debugging

### Logging

- Use the `logging` module for debug information
- Set appropriate log levels (DEBUG, INFO, WARNING, ERROR)
- Log important events and errors

### Common Issues

1. **API Key Issues**:
   - Verify API keys in `.env` file
   - Check API key permissions
   - Ensure API endpoints are correct

2. **Document Processing Issues**:
   - Check file formats and encodings
   - Verify document parsing logic
   - Look for specific error messages

3. **Evaluation Issues**:
   - Check test case formatting
   - Verify ground truth data
   - Ensure RAG system connectivity

## Performance Considerations

- Optimize document processing for large files
- Implement caching where appropriate
- Use efficient data structures for large datasets
- Consider memory usage when processing multiple documents

## Security Considerations

- Never commit API keys or sensitive information
- Validate all inputs to prevent injection attacks
- Sanitize user-provided data
- Use secure communication protocols (HTTPS) when interacting with APIs

## Release Process

1. Update version number in `config.json`
2. Update `CHANGELOG.md` with changes
3. Create a release branch
4. Run all tests
5. Create a git tag
6. Push to repository
7. Create GitHub release