# Ragas + Ollama評価器 - OpenRouter Chat + Ollama Embeddings

from typing import Dict, List, Any
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import answer_relevancy, answer_correctness
from ragas.llms import LangchainLLMWrapper
from langchain_openai import ChatOpenAI
from langchain_community.embeddings import OllamaEmbeddings
from .base import BaseEvaluator

class RagasOllamaEvaluator(BaseEvaluator):
    """Ragas + Ollama評価器 - OpenRouter Chat + Ollama Embeddings"""
    
    def __init__(self, config: Dict[str, Any]):
        """Ragas + Ollama評価器を初期化"""
        super().__init__("RagasOllama", config)
        
        try:
            # OpenRouter Chat LLMを初期化
            self.eval_llm = LangchainLLMWrapper(ChatOpenAI(
                api_key=config["api_key"],
                base_url=config["base_url"],
                model=config.get("model", "gpt-3.5-turbo"),
                temperature=0,
                max_tokens=1000,
                timeout=30
            ))
            
            # Ollama Embeddingsを初期化
            ollama_base_url = config.get("ollama_base_url", "http://localhost:11434")
            ollama_model = config.get("ollama_embedding_model", "nomic-embed-text:latest")
            
            self.embeddings = OllamaEmbeddings(
                base_url=ollama_base_url,
                model=ollama_model
            )
            
            # Embeddingsテスト
            test_result = self.embeddings.embed_query("test")
            if len(test_result) > 0:
                print(f"✅ Ollama Embeddings初期化成功: {ollama_model}")
            else:
                raise ValueError("Embeddings test failed")
            
            self._available = True
            print(f"✅ {self.name}評価器初期化成功")
            print(f"   Chat: {config.get('model', 'gpt-3.5-turbo')} (OpenRouter)")
            print(f"   Embeddings: {ollama_model} (Ollama)")
            
        except Exception as e:
            print(f"❌ {self.name}評価器初期化失敗: {e}")
            self._available = False
    
    def evaluate_answers(self, questions: List[str], answers: List[str], 
                        ground_truths: List[str], contexts: List[List[str]] = None) -> Dict[str, List[float]]:
        """Ragas + Ollama評価を実行"""
        if not self._available:
            return {"relevancy": [None] * len(answers), "correctness": [None] * len(answers)}
        
        # 有効な回答のみを評価
        valid_indices = [i for i, answer in enumerate(answers) if answer and answer.strip()]
        if not valid_indices:
            return {"relevancy": [None] * len(answers), "correctness": [None] * len(answers)}
        
        # 評価データを準備
        eval_questions = [questions[i] for i in valid_indices]
        eval_answers = [answers[i] for i in valid_indices]
        eval_ground_truths = [ground_truths[i] for i in valid_indices]
        eval_contexts = [contexts[i] if contexts else ['関連コンテキスト'] for i in valid_indices]
        
        try:
            # データセットを作成
            dataset = Dataset.from_dict({
                'question': eval_questions,
                'answer': eval_answers,
                'ground_truth': eval_ground_truths,
                'contexts': eval_contexts
            })
            
            print(f"    データセット作成: {len(eval_questions)}件")
            
            # Ragas評価を実行 - カスタムEmbeddingsを使用
            result = evaluate(
                dataset, 
                metrics=[answer_relevancy, answer_correctness],
                llm=self.eval_llm,
                embeddings=self.embeddings,  # Ollama Embeddingsを指定
                raise_exceptions=False
            )
            
            print(f"    評価完了: {result}")
            
            # 結果を元のインデックスにマッピング
            relevancy_scores = [None] * len(answers)
            correctness_scores = [None] * len(answers)

            # Ragasの結果は辞書形式で、各メトリクスは単一値またはリスト
            import math

            # Answer Relevancy処理
            rel_result = result.get('answer_relevancy')
            if rel_result is not None:
                try:
                    if isinstance(rel_result, (list, tuple)):
                        # リストの場合
                        for i, idx in enumerate(valid_indices):
                            if i < len(rel_result):
                                score = rel_result[i]
                                relevancy_scores[idx] = score if score is not None and not math.isnan(score) else None
                    else:
                        # 単一値の場合
                        score = rel_result
                        if not math.isnan(score):
                            # 全ての有効インデックスに同じスコアを適用
                            for idx in valid_indices:
                                relevancy_scores[idx] = score
                except Exception as e:
                    print(f"    Relevancy処理エラー: {e}")
                    # エラーの場合、全てNoneのまま

            # Answer Correctness処理
            cor_result = result.get('answer_correctness')
            if cor_result is not None:
                try:
                    if isinstance(cor_result, (list, tuple)):
                        # リストの場合
                        for i, idx in enumerate(valid_indices):
                            if i < len(cor_result):
                                score = cor_result[i]
                                correctness_scores[idx] = score if score is not None and not math.isnan(score) else None
                    else:
                        # 単一値の場合
                        score = cor_result
                        if not math.isnan(score):
                            # 全ての有効インデックスに同じスコアを適用
                            for idx in valid_indices:
                                correctness_scores[idx] = score
                except Exception as e:
                    print(f"    Correctness処理エラー: {e}")
                    # エラーの場合、全てNoneのまま
            
            return {
                "relevancy": relevancy_scores,
                "correctness": correctness_scores
            }
            
        except Exception as e:
            print(f"❌ {self.name}評価失敗: {e}")
            import traceback
            traceback.print_exc()
            return {"relevancy": [None] * len(answers), "correctness": [None] * len(answers)}
    
    def get_supported_metrics(self) -> List[str]:
        """サポートされている評価指標"""
        return ["relevancy", "correctness"]
    
    def is_available(self) -> bool:
        """評価器が利用可能かチェック"""
        return self._available
