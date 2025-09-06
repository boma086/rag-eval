# 評価器ファクトリー - Factory Pattern実装 (Legacy - すべて非同期バージョンを使用)

from typing import Dict, List, Any, Optional
from .base import BaseEvaluator

class EvaluatorFactory:
    """評価器ファクトリークラス - 評価器の生成と管理を統一"""
    
    # 利用可能な評価器タイプ (すべて非同期バージョンを使用)
    EVALUATOR_TYPES = {
        # 注: 同期評価器は削除されました。非同期バージョンを使用してください。
    }
    
    # デフォルト評価器の優先順位
    DEFAULT_PRIORITY = []  # 同期評価器は使用されません
    
    @classmethod
    def create_evaluator(cls, evaluator_type: str, config: Dict[str, Any]) -> Optional[BaseEvaluator]:
        """指定されたタイプの評価器を作成"""
        print(f"⚠️  {evaluator_type} 同期評価器は削除されました。非同期バージョンを使用してください。")
        return None
    
    @classmethod
    def create_all_evaluators(cls, config: Dict[str, Any], 
                            types: Optional[List[str]] = None) -> Dict[str, BaseEvaluator]:
        """全ての利用可能な評価器を作成"""
        print("⚠️  同期評価器はすべて削除されました。非同期バージョンを使用してください。")
        return {}
    
    @classmethod
    def get_evaluator_info(cls) -> Dict[str, Dict[str, Any]]:
        """全評価器の情報を取得"""
        print("⚠️  同期評価器はすべて削除されました。非同期バージョンを使用してください。")
        return {}
    
    @classmethod
    def _get_evaluator_description(cls, evaluator_type: str) -> str:
        """評価器の説明を取得"""
        return f"{evaluator_type} 同期評価器は削除されました。非同期バージョンを使用してください。"

class EvaluatorManager:
    """評価器マネージャー - Strategy Pattern実装 (Legacy - 非同期バージョンを使用)"""
    
    def __init__(self, chat_config: Dict[str, Any], embedding_config: Dict[str, Any]):
        """評価器マネージャーを初期化"""
        print("⚠️  EvaluatorManager はレガシークラスです。AsyncEvaluatorManager を使用してください。")
        self.evaluators = {}
        print(f"🔧 同期評価器はすべて削除されました。非同期バージョンを使用してください。")
    
    def evaluate_all(self, questions: List[str], answers: List[str], 
                    ground_truths: List[str], contexts: List[List[str]] = None) -> Dict[str, Dict[str, List[float]]]:
        """全評価器で評価を実行"""
        print("⚠️  同期評価器はすべて削除されました。非同期バージョンを使用してください。")
        return {}
    
    def get_evaluator_summary(self) -> Dict[str, Any]:
        """評価器の概要を取得"""
        print("⚠️  同期評価器はすべて削除されました。非同期バージョンを使用してください。")
        return {
            "total_evaluators": 0,
            "available_evaluators": [],
            "evaluator_details": {}
        }
