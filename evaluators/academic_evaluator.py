# 学術的評価器 - Ragasの代替として専門的評価を提供

from typing import Dict, List, Any
from langchain_openai import ChatOpenAI
from .base import BaseEvaluator
import json
import re

class AcademicEvaluator(BaseEvaluator):
    """学術的評価器 - RAG評価の学術標準に基づく評価"""
    
    def __init__(self, config: Dict[str, Any]):
        """学術的評価器を初期化"""
        super().__init__("Academic", config)
        
        try:
            # 評価LLMを初期化
            self.eval_llm = ChatOpenAI(
                api_key=config["api_key"],
                base_url=config["base_url"],
                model=config.get("model", "gpt-3.5-turbo"),
                temperature=0
            )
            self._available = True
            print(f"✅ {self.name}評価器初期化成功")
        except Exception as e:
            print(f"❌ {self.name}評価器初期化失敗: {e}")
            self._available = False
    
    def evaluate_answers(self, questions: List[str], answers: List[str], 
                        ground_truths: List[str], contexts: List[List[str]] = None) -> Dict[str, List[float]]:
        """学術的基準で回答を評価"""
        if not self._available:
            return {"relevancy": [None] * len(answers), 
                   "correctness": [None] * len(answers),
                   "completeness": [None] * len(answers),
                   "clarity": [None] * len(answers)}
        
        relevancy_scores = []
        correctness_scores = []
        completeness_scores = []
        clarity_scores = []
        
        for question, answer, ground_truth in zip(questions, answers, ground_truths):
            if answer and answer.strip():
                # 多次元評価を実行
                scores = self.evaluate_single_answer(question, answer, ground_truth)
                relevancy_scores.append(scores["relevancy"])
                correctness_scores.append(scores["correctness"])
                completeness_scores.append(scores["completeness"])
                clarity_scores.append(scores["clarity"])
            else:
                relevancy_scores.append(None)
                correctness_scores.append(None)
                completeness_scores.append(None)
                clarity_scores.append(None)
        
        return {
            "relevancy": relevancy_scores,
            "correctness": correctness_scores,
            "completeness": completeness_scores,
            "clarity": clarity_scores
        }
    
    def evaluate_single_answer(self, question: str, answer: str, ground_truth: str) -> Dict[str, float]:
        """単一回答の多次元評価"""
        
        evaluation_prompt = f"""
あなたは専門的なRAGシステム評価者です。以下の質問、回答、正解を分析し、4つの観点から0.0-1.0のスコアで評価してください。

質問: {question}

回答: {answer}

正解: {ground_truth}

以下の4つの観点から評価し、JSON形式で回答してください：

1. **関連性 (Relevancy)**: 回答が質問にどれだけ関連しているか
   - 1.0: 質問に完全に関連している
   - 0.8: 質問にほぼ関連している
   - 0.6: 質問に部分的に関連している
   - 0.4: 質問にわずかに関連している
   - 0.2: 質問にほとんど関連していない
   - 0.0: 質問に全く関連していない

2. **正確性 (Correctness)**: 回答が正解とどれだけ一致しているか
   - 1.0: 正解と完全に一致している
   - 0.8: 正解とほぼ一致している
   - 0.6: 正解と部分的に一致している
   - 0.4: 正解とわずかに一致している
   - 0.2: 正解とほとんど一致していない
   - 0.0: 正解と全く一致していない

3. **完全性 (Completeness)**: 回答が質問に対して十分な情報を提供しているか
   - 1.0: 質問に対して完全な情報を提供
   - 0.8: 質問に対してほぼ完全な情報を提供
   - 0.6: 質問に対して部分的な情報を提供
   - 0.4: 質問に対して最小限の情報を提供
   - 0.2: 質問に対して不十分な情報を提供
   - 0.0: 質問に対して情報を提供していない

4. **明確性 (Clarity)**: 回答がどれだけ明確で理解しやすいか
   - 1.0: 非常に明確で理解しやすい
   - 0.8: 明確で理解しやすい
   - 0.6: ある程度明確
   - 0.4: やや不明確
   - 0.2: 不明確
   - 0.0: 全く不明確

JSON形式で回答してください：
{{
    "relevancy": 0.8,
    "correctness": 0.7,
    "completeness": 0.9,
    "clarity": 0.8
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
                for metric in ["relevancy", "correctness", "completeness", "clarity"]:
                    score = scores_dict.get(metric, 0.0)
                    validated_scores[metric] = max(0.0, min(1.0, float(score)))
                
                return validated_scores
            else:
                print(f"JSON解析失敗: {result_text}")
                return {"relevancy": 0.0, "correctness": 0.0, "completeness": 0.0, "clarity": 0.0}
                
        except Exception as e:
            print(f"評価エラー: {e}")
            return {"relevancy": 0.0, "correctness": 0.0, "completeness": 0.0, "clarity": 0.0}
    
    def get_supported_metrics(self) -> List[str]:
        """サポートされている評価指標"""
        return ["relevancy", "correctness", "completeness", "clarity"]
    
    def is_available(self) -> bool:
        """評価器が利用可能かチェック"""
        return self._available
