# Evaluation Metrics Framework

This module defines the evaluation metrics framework for assessing RAG systems.

## Standard Metrics (from Ragas)

1. **Faithfulness**
   - Measures if the answer is factual based on the given context
   - Score range: 0.0 - 1.0 (higher is better)

2. **Answer Relevancy**
   - Evaluates how relevant the answer is to the question
   - Score range: 0.0 - 1.0 (higher is better)

3. **Context Recall**
   - Assesses the retrieval mechanism's ability to return all relevant information
   - Score range: 0.0 - 1.0 (higher is better)

4. **Context Precision**
   - Measures the signal-to-noise ratio of retrieved context
   - Score range: 0.0 - 1.0 (higher is better)

5. **Answer Correctness**
   - Combines semantic similarity and factual accuracy
   - Score range: 0.0 - 1.0 (higher is better)

## Custom Metrics

1. **Technical Accuracy**
   - Evaluates the technical correctness of the response in software development context
   - Implementation in metrics/technical_accuracy.py

2. **Domain Relevance**
   - Measures how well the response addresses Japanese software development specific concerns
   - Implementation in metrics/domain_relevance.py

3. **Language Appropriateness**
   - Assesses the appropriateness of language use, particularly for Japanese technical terms
   - Implementation in metrics/japanese_language_appropriateness.py

## Automated vs Manual Evaluation

The framework supports both automated and manual evaluation:

1. **Automated Evaluation**
   - Uses LLMs to score responses based on predefined criteria
   - Fast and scalable for large numbers of test cases
   - Implementation uses the configured evaluator (OpenRouter)

2. **Manual Evaluation**
   - Human evaluators score responses using a web interface or spreadsheet
   - More accurate but time-consuming
   - Results can be imported into the system for comparison

3. **Hybrid Approach**
   - Combines both automated and manual evaluation
   - Allows for validation of automated scores against human judgment
   - Provides flexibility to choose the evaluation method per test case