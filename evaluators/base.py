# 評価器基底クラス

from abc import ABC, abstractmethod
from typing import Dict, List, Any

class BaseEvaluator(ABC):
    """評価器の基底クラス"""
    
    def __init__(self, name: str, config: Dict[str, Any]):
        """
        評価器を初期化
        
        Args:
            name: 評価器名
            config: 設定辞書
        """
        self.name = name
        self.config = config
    
    @abstractmethod
    def evaluate_answers(self, questions: List[str], answers: List[str], 
                        ground_truths: List[str], contexts: List[List[str]] = None) -> Dict[str, List[float]]:
        """
        回答を評価
        
        Args:
            questions: 質問リスト
            answers: 回答リスト
            ground_truths: 正解リスト
            contexts: コンテキストリスト（オプション）
            
        Returns:
            評価結果辞書 {"metric_name": [scores]}
        """
        pass
    
    @abstractmethod
    def get_supported_metrics(self) -> List[str]:
        """サポートされている評価指標を取得"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """評価器が利用可能かチェック"""
        pass
    
    def get_info(self) -> Dict[str, Any]:
        """評価器情報を取得"""
        return {
            "name": self.name,
            "supported_metrics": self.get_supported_metrics(),
            "available": self.is_available(),
            "config": self.config
        }
