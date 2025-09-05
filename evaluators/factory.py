# 評価器ファクトリー - Factory Pattern実装

from typing import Dict, List, Any, Optional
from .base import BaseEvaluator
from .ragas_ollama import RagasOllamaEvaluator  # Re-enabled with compatible versions

class EvaluatorFactory:
    """評価器ファクトリークラス - 評価器の生成と管理を統一"""
    
    # 利用可能な評価器タイプ
    EVALUATOR_TYPES = {
        "ragas": RagasOllamaEvaluator,  # Re-enabled with compatible versions
        # "academic": AcademicEvaluator  # Removed in favor of async version
    }
    
    # デフォルト評価器の優先順位
    DEFAULT_PRIORITY = ["ragas"]  # Re-enabled Ragas evaluator
    
    @classmethod
    def create_evaluator(cls, evaluator_type: str, config: Dict[str, Any]) -> Optional[BaseEvaluator]:
        """指定されたタイプの評価器を作成"""
        if evaluator_type not in cls.EVALUATOR_TYPES:
            raise ValueError(f"未対応の評価器タイプ: {evaluator_type}")
        
        evaluator_class = cls.EVALUATOR_TYPES[evaluator_type]
        
        try:
            evaluator = evaluator_class(config)
            if evaluator.is_available():
                return evaluator
            else:
                print(f"⚠️  {evaluator_type}評価器は利用不可")
                return None
        except Exception as e:
            print(f"❌ {evaluator_type}評価器作成失敗: {e}")
            return None
    
    @classmethod
    def create_all_evaluators(cls, config: Dict[str, Any], 
                            types: Optional[List[str]] = None) -> Dict[str, BaseEvaluator]:
        """全ての利用可能な評価器を作成"""
        if types is None:
            types = cls.DEFAULT_PRIORITY
        
        evaluators = {}
        
        for evaluator_type in types:
            evaluator = cls.create_evaluator(evaluator_type, config)
            if evaluator:
                evaluators[evaluator_type] = evaluator
        
        return evaluators
    
    @classmethod
    def get_evaluator_info(cls) -> Dict[str, Dict[str, Any]]:
        """全評価器の情報を取得"""
        info = {}
        
        for name, evaluator_class in cls.EVALUATOR_TYPES.items():
            # 一時的にダミー設定で情報を取得
            dummy_config = {
                "api_key": "dummy",
                "base_url": "dummy",
                "model": "dummy"
            }
            
            try:
                temp_evaluator = evaluator_class(dummy_config)
                info[name] = {
                    "name": temp_evaluator.name,
                    "supported_metrics": temp_evaluator.get_supported_metrics(),
                    "description": cls._get_evaluator_description(name)
                }
            except:
                info[name] = {
                    "name": name,
                    "supported_metrics": [],
                    "description": cls._get_evaluator_description(name)
                }
        
        return info
    
    @classmethod
    def _get_evaluator_description(cls, evaluator_type: str) -> str:
        """評価器の説明を取得"""
        descriptions = {
            "ragas": "Ragas框架 - OpenRouter Chat + Ollama Embeddings",  # Re-enabled with compatible versions
            # "academic": "学術的評価器 - 4次元専門評価（関連性、正確性、完整性、清晰度）"  # Removed in favor of async version
        }
        return descriptions.get(evaluator_type, "説明なし")

class EvaluatorManager:
    """評価器マネージャー - Strategy Pattern実装"""
    
    def __init__(self, chat_config: Dict[str, Any], embedding_config: Dict[str, Any]):
        """評価器マネージャーを初期化"""
        # 合并聊天和嵌入配置
        combined_config = {**chat_config, **embedding_config}
        self.config = combined_config
        self.evaluators = EvaluatorFactory.create_all_evaluators(combined_config)
        
        if not self.evaluators:
            raise ValueError("利用可能な評価器がありません")
        
        print(f"🔧 利用可能な評価器: {list(self.evaluators.keys())}")
    
    def evaluate_all(self, questions: List[str], answers: List[str], 
                    ground_truths: List[str], contexts: List[List[str]] = None) -> Dict[str, Dict[str, List[float]]]:
        """全評価器で評価を実行"""
        all_results = {}
        
        for evaluator_name, evaluator in self.evaluators.items():
            print(f"\n📊 {evaluator_name}評価器で評価中...")
            
            try:
                metrics = evaluator.evaluate_answers(questions, answers, ground_truths, contexts)
                all_results[evaluator_name] = metrics
                print(f"    ✅ 完了")
            except Exception as e:
                print(f"    ❌ 失敗: {e}")
                # デフォルト値で埋める
                default_metrics = {metric: [None] * len(answers) 
                                 for metric in evaluator.get_supported_metrics()}
                all_results[evaluator_name] = default_metrics
        
        return all_results
    
    def get_evaluator_summary(self) -> Dict[str, Any]:
        """評価器の概要を取得"""
        summary = {
            "total_evaluators": len(self.evaluators),
            "available_evaluators": list(self.evaluators.keys()),
            "evaluator_details": {}
        }
        
        for name, evaluator in self.evaluators.items():
            summary["evaluator_details"][name] = evaluator.get_info()
        
        return summary
