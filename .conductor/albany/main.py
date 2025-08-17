# Main Application Entry Point

This script serves as the main entry point for the RAG evaluation framework.

## Usage

```bash
# Run automated evaluation
python main.py --mode auto

# Run manual evaluation interface
python main.py --mode manual

# Run both automated and manual evaluation
python main.py --mode both

# Run with specific configuration
python main.py --config config.json --mode auto
```

## Command Line Arguments

- `--mode`: Evaluation mode (auto, manual, both)
- `--config`: Path to configuration file
- `--test-cases`: Path to test cases file
- `--documents`: Path to documents directory
- `--output`: Path to output results

## Process Flow

1. **Parse Command Line Arguments**
   - Validate provided arguments
   - Set default values for missing arguments

2. **Load Configuration**
   - Load config from specified file or default
   - Initialize all system components

3. **Execute Based on Mode**
   - Auto Mode: Run automated evaluation
   - Manual Mode: Launch manual evaluation interface
   - Both Mode: Run automated evaluation and then launch manual interface

4. **Generate Reports**
   - Create detailed evaluation reports
   - Export results in various formats