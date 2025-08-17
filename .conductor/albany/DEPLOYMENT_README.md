# Deployment README

This document provides instructions for deploying the RAG Evaluation Framework in a production environment.

## System Requirements

### Hardware Requirements
- CPU: 2+ cores recommended
- RAM: 8GB+ recommended
- Storage: 20GB+ free space for documents and results

### Software Requirements
- Operating System: Linux, macOS, or Windows
- Python: 3.8 or higher
- pip: 20.0 or higher

## Deployment Options

### 1. Local Deployment

#### Prerequisites
1. Install Python 3.8 or higher
2. Install pip
3. Install virtualenv: `pip install virtualenv`

#### Deployment Steps
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

4. Configure the environment:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

5. Run the application:
   ```bash
   python main.py --mode auto
   ```

### 2. Docker Deployment

#### Prerequisites
1. Install Docker
2. Install Docker Compose

#### Deployment Steps
1. Build the Docker image:
   ```bash
   docker build -t ragas-evaluator .
   ```

2. Create a `.env` file with your configuration

3. Run the container:
   ```bash
   docker run --env-file .env -v ./data:/app/data -v ./results:/app/results -v ./reports:/app/reports ragas-evaluator
   ```

### 3. Cloud Deployment (AWS Example)

#### Prerequisites
1. AWS Account
2. AWS CLI configured
3. Docker installed

#### Deployment Steps
1. Create an EC2 instance with Ubuntu 20.04 or higher

2. SSH into the instance:
   ```bash
   ssh -i your-key.pem ubuntu@your-instance-ip
   ```

3. Install Docker:
   ```bash
   sudo apt update
   sudo apt install docker.io docker-compose -y
   sudo usermod -aG docker ubuntu
   ```

4. Clone the repository:
   ```bash
   git clone <repository-url>
   cd ragas
   ```

5. Configure the environment:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

6. Build and run with Docker Compose:
   ```bash
   docker-compose up -d
   ```

## Configuration

### Environment Variables

Create a `.env` file with the following variables:

```
# OpenRouter Configuration
OPENROUTER_API_KEY=your_openrouter_api_key
EVALUATOR_MODEL=gpt-3.5-turbo
EVALUATOR_BASE_URL=https://openrouter.ai/api/v1

# RAG System Configuration
RAGFLOW_API_KEY=your_ragflow_api_key
RAGFLOW_BASE_URL=your_ragflow_endpoint

DIFY_API_KEY=your_dify_api_key
DIFY_BASE_URL=your_dify_endpoint
```

### Configuration File

Modify `config.json` to adjust application settings:

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

## Data Management

### Document Storage

Place all historical design documents in the `data/` directory. The framework supports:
- Text files (.txt)
- PDF documents (.pdf)
- Word documents (.docx)
- Excel spreadsheets (.xlsx, .xls)
- Images (.jpg, .png) with OCR support

### Test Cases

Update `data/test_cases.json` with your test scenarios. Each test case should include:
- A question or requirement
- Expected ground truth answer
- Tags for categorization

### Results and Reports

Evaluation results are stored in the `results/` directory, and reports are generated in the `reports/` directory. Ensure these directories are backed up regularly.

## Monitoring and Maintenance

### Log Management

The application logs to stdout/stderr by default. When running in production, redirect logs to files or a log management system:

```bash
python main.py --mode auto > logs/application.log 2> logs/error.log
```

### Performance Monitoring

- Monitor CPU and memory usage
- Track evaluation completion times
- Monitor API usage and costs

### Updates and Upgrades

1. Pull the latest code:
   ```bash
   git pull origin main
   ```

2. Update dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Restart the application

## Security Considerations

### API Keys

- Store API keys securely in environment variables
- Never commit API keys to version control
- Rotate API keys regularly

### Data Security

- Encrypt sensitive data at rest
- Use HTTPS for all API communications
- Implement access controls for the application

### Network Security

- Restrict access to the application server
- Use firewalls to limit incoming connections
- Keep systems updated with security patches

## Troubleshooting

### Common Issues

1. **API Key Errors**:
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

### Getting Help

If you encounter issues not covered in this document:
1. Check the application logs for error messages
2. Review the documentation in README.md and DEVELOPER_README.md
3. Create an issue in the repository with detailed information about the problem