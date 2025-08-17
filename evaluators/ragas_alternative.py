# Ragas代替評価器 - Embeddings不要の専門評価

from typing import Dict, List, Any
from langchain_openai import ChatOpenAI
from .base import BaseEvaluator
import json
import re

class RagasAlternativeEvaluator(BaseEvaluator):
    """Ragas代替評価器 - Ragasの評価基準を模倣してEmbeddings不要で実装"""
    
    def __init__(self, config: Dict[str, Any]):
        """Ragas代替評価器を初期化"""
        super().__init__("RagasAlt", config)
        
        try:
            # 評価LLMを初期化
            self.eval_llm = ChatOpenAI(
                api_key=config["api_key"],
                base_url=config["base_url"],
                model=config.get("model", "gpt-3.5-turbo"),
                temperature=0
            )
            self._available = True
            print(f"✅ {self.name}評価器初期化成功 (Ragas代替)")
        except Exception as e:
            print(f"❌ {self.name}評価器初期化失敗: {e}")
            self._available = False
    
    def evaluate_answers(self, questions: List[str], answers: List[str], 
                        ground_truths: List[str], contexts: List[List[str]] = None) -> Dict[str, List[float]]:
        """Ragas基準で回答を評価"""
        if not self._available:
            return {"relevancy": [None] * len(answers), 
                   "correctness": [None] * len(answers),
                   "faithfulness": [None] * len(answers)}
        
        relevancy_scores = []
        correctness_scores = []
        faithfulness_scores = []
        
        for question, answer, ground_truth in zip(questions, answers, ground_truths):
            if answer and answer.strip():
                scores = self.evaluate_ragas_style(question, answer, ground_truth, 
                                                 contexts[0] if contexts else [])
                relevancy_scores.append(scores["relevancy"])
                correctness_scores.append(scores["correctness"])
                faithfulness_scores.append(scores["faithfulness"])
            else:
                relevancy_scores.append(None)
                correctness_scores.append(None)
                faithfulness_scores.append(None)
        
        return {
            "relevancy": relevancy_scores,
            "correctness": correctness_scores,
            "faithfulness": faithfulness_scores
        }
    
    def evaluate_ragas_style(self, question: str, answer: str, ground_truth: str, 
                           contexts: List[str]) -> Dict[str, float]:
        """Ragas風の評価を実行"""
        
        evaluation_prompt = f"""
あなたはRAG（Retrieval-Augmented Generation）システムの専門評価者です。
以下の質問、回答、正解、コンテキストを分析し、Ragasの評価基準に従って3つの指標で評価してください。

質問: {question}

回答: {answer}

正解: {ground_truth}

コンテキスト: {' '.join(contexts) if contexts else '利用可能なコンテキストなし'}

以下の3つのRagas指標で0.0-1.0のスコアで評価し、JSON形式で回答してください：

1. **Answer Relevancy (回答関連性)**:
   回答が質問にどれだけ関連しているかを評価します。
   - 質問の核心に直接答えているか
   - 不要な情報や逸脱がないか
   - 質問の意図を正しく理解しているか
   
   評価基準:
   - 1.0: 質問に完全に関連し、直接的で適切な回答
   - 0.8: 質問にほぼ関連し、わずかな逸脱のみ
   - 0.6: 質問に部分的に関連するが、一部不要な情報
   - 0.4: 質問に関連するが、多くの不要な情報
   - 0.2: 質問にわずかに関連するのみ
   - 0.0: 質問に全く関連しない

2. **Answer Correctness (回答正確性)**:
   回答が正解とどれだけ一致しているかを評価します。
   - 事実の正確性
   - 情報の完全性
   - 正解との意味的一致
   
   評価基準:
   - 1.0: 正解と完全に一致、すべての重要な情報を含む
   - 0.8: 正解とほぼ一致、重要な情報の大部分を含む
   - 0.6: 正解と部分的に一致、一部の重要な情報を含む
   - 0.4: 正解とわずかに一致、最小限の情報のみ
   - 0.2: 正解とほとんど一致しない
   - 0.0: 正解と全く一致しない

3. **Faithfulness (忠実性)**:
   回答がコンテキストに忠実で、幻覚（hallucination）がないかを評価します。
   - コンテキストに基づいた情報のみを使用しているか
   - コンテキストにない情報を勝手に追加していないか
   - 事実を歪曲していないか
   
   評価基準:
   - 1.0: コンテキストに完全に忠実、幻覚なし
   - 0.8: コンテキストにほぼ忠実、わずかな推論のみ
   - 0.6: コンテキストに部分的に忠実、一部推論あり
   - 0.4: コンテキストから逸脱、多くの推論
   - 0.2: コンテキストをほとんど無視
   - 0.0: コンテキストを完全に無視、幻覚多数

JSON形式で回答してください：
{{
    "relevancy": 0.8,
    "correctness": 0.7,
    "faithfulness": 0.9
}}
"""
        
        try:
            response = self.eval_llm.invoke(evaluation_prompt)
            result_text = response.content.strip()
            
            # JSONを抽出
            json_match = re.search(r'\{[^}]+\}', result_text)
            if json_match:
                scores_dict = json.loads(json_match.group())
                
                # スコアを検証・正規化
                validated_scores = {}
                for metric in ["relevancy", "correctness", "faithfulness"]:
                    score = scores_dict.get(metric, 0.0)
                    validated_scores[metric] = max(0.0, min(1.0, float(score)))
                
                return validated_scores
            else:
                print(f"JSON解析失敗: {result_text}")
                return {"relevancy": 0.0, "correctness": 0.0, "faithfulness": 0.0}
                
        except Exception as e:
            print(f"評価エラー: {e}")
            return {"relevancy": 0.0, "correctness": 0.0, "faithfulness": 0.0}
    
    def get_supported_metrics(self) -> List[str]:
        """サポートされている評価指標"""
        return ["relevancy", "correctness", "faithfulness"]
    
    def is_available(self) -> bool:
        """評価器が利用可能かチェック"""
        return self._available
