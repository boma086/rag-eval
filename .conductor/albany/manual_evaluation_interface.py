# Manual Evaluation Interface

This module provides a web-based interface for manual evaluation of RAG responses.

## Features

1. **Test Case Management**
   - Display test cases in a structured format
   - Filter by tags or categories
   - Search functionality

2. **Response Comparison**
   - Side-by-side comparison of responses from different RAG systems
   - Display retrieved contexts
   - Show metadata (processing time, model used, etc.)

3. **Evaluation Scoring**
   - Score each response for different metrics
   - Provide textual feedback for each score
   - Save evaluations to database/file

4. **Results Visualization**
   - Compare automated vs manual scores
   - View aggregated metrics per RAG system
   - Export evaluation results

## Implementation Plan

1. **Frontend**
   - Use a lightweight web framework (e.g., Streamlit, Flask)
   - Create intuitive UI for evaluators
   - Implement responsive design

2. **Backend**
   - Serve test cases and RAG responses
   - Handle evaluation submissions
   - Store manual evaluations

3. **Integration**
   - Interface with evaluation_orchestrator.py
   - Import manual evaluations into the main results
   - Compare manual and automated evaluations

## Usage Workflow

1. **Evaluator Login**
   - Simple authentication (could be single-user for initial implementation)

2. **Test Case Selection**
   - Browse or search available test cases
   - Select individual cases or batches for evaluation

3. **Evaluation Process**
   - View question and ground truth
   - Review responses from each RAG system
   - Score each response for multiple metrics
   - Provide textual feedback

4. **Results Review**
   - View previous evaluations
   - Compare with automated evaluations
   - Export results in various formats