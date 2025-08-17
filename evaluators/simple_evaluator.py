# シンプル評価器 - 直接LLM評価

from typing import Dict, List, Any
from langchain_openai import ChatOpenAI
from .base import BaseEvaluator

class SimpleEvaluator(BaseEvaluator):
    """シンプル評価器 - 直接LLM評価"""

    def __init__(self, config: Dict[str, Any]):
        """シンプル評価器を初期化"""
        super().__init__("Simple", config)

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
        """回答を評価"""
        if not self._available:
            return {"relevancy": [None] * len(answers), "correctness": [None] * len(answers)}

        relevancy_scores = []
        correctness_scores = []

        for question, answer, ground_truth in zip(questions, answers, ground_truths):
            if answer and answer.strip():
                # 関連性評価
                relevancy = self.evaluate_answer_relevancy(question, answer)
                relevancy_scores.append(relevancy)

                # 正確性評価
                correctness = self.evaluate_answer_correctness(question, answer, ground_truth)
                correctness_scores.append(correctness)
            else:
                relevancy_scores.append(None)
                correctness_scores.append(None)

        return {
            "relevancy": relevancy_scores,
            "correctness": correctness_scores
        }

    def evaluate_answer_relevancy(self, question: str, answer: str) -> float:
        """回答関連性を評価 (0.0-1.0)"""
        if not answer.strip():
            return 0.0
        
        prompt = f"""
質問と回答の関連性を0.0から1.0のスコアで評価してください。

質問: {question}
回答: {answer}

評価基準:
- 1.0: 回答が質問に完全に関連している
- 0.8: 回答が質問にほぼ関連している
- 0.6: 回答が質問に部分的に関連している
- 0.4: 回答が質問にわずかに関連している
- 0.2: 回答が質問にほとんど関連していない
- 0.0: 回答が質問に全く関連していない

スコアのみを数値で回答してください（例: 0.8）
"""
        
        try:
            response = self.eval_llm.invoke(prompt)
            score_text = response.content.strip()
            score = float(score_text)
            return max(0.0, min(1.0, score))  # 0.0-1.0の範囲に制限
        except Exception as e:
            print(f"関連性評価エラー: {e}")
            return 0.0

    def evaluate_answer_correctness(self, question: str, answer: str, ground_truth: str) -> float:
        """回答正確性を評価 (0.0-1.0)"""
        if not answer.strip():
            return 0.0
        
        prompt = f"""
質問、回答、正解を比較して、回答の正確性を0.0から1.0のスコアで評価してください。

質問: {question}
回答: {answer}
正解: {ground_truth}

評価基準:
- 1.0: 回答が正解と完全に一致している
- 0.8: 回答が正解とほぼ一致している
- 0.6: 回答が正解と部分的に一致している
- 0.4: 回答が正解とわずかに一致している
- 0.2: 回答が正解とほとんど一致していない
- 0.0: 回答が正解と全く一致していない

スコアのみを数値で回答してください（例: 0.8）
"""
        
        try:
            response = self.eval_llm.invoke(prompt)
            score_text = response.content.strip()
            score = float(score_text)
            return max(0.0, min(1.0, score))  # 0.0-1.0の範囲に制限
        except Exception as e:
            print(f"正確性評価エラー: {e}")
            return 0.0

    def get_supported_metrics(self) -> List[str]:
        """サポートされている評価指標"""
        return ["relevancy", "correctness"]

    def is_available(self) -> bool:
        """評価器が利用可能かチェック"""
        return self._available
