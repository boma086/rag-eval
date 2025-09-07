# 评估器工厂 - 评估器的创建和管理

from typing import Dict, List, Any, Optional
from .base import BaseEvaluator
from .academic_evaluator import AcademicEvaluator
from .ragas_evaluator import RagasEvaluator
import asyncio
import logging

logger = logging.getLogger(__name__)

class EvaluatorFactory:
    """评估器工厂类"""
    
    # 可用的评估器类型
    EVALUATOR_TYPES = {
        "academic": AcademicEvaluator,
        "ragas": RagasEvaluator
    }
    
    # 默认评估器优先级
    DEFAULT_PRIORITY = ["ragas", "academic"]
    
    @classmethod
    async def create_evaluator_async(cls, evaluator_type: str, config: Dict[str, Any]) -> Optional[BaseEvaluator]:
        """异步创建评估器"""
        if evaluator_type not in cls.EVALUATOR_TYPES:
            raise ValueError(f"不支持的评估器类型: {evaluator_type}")
        
        evaluator_class = cls.EVALUATOR_TYPES[evaluator_type]
        
        try:
            evaluator = evaluator_class(config)
            if evaluator.is_available():
                return evaluator
            else:
                print(f"⚠️  {evaluator_type}评估器不可用")
                return None
        except Exception as e:
            print(f"❌ {evaluator_type}评估器创建失败: {e}")
            return None
    
    @classmethod
    async def create_all_evaluators_async(cls, config: Dict[str, Any], 
                                        types: Optional[List[str]] = None) -> Dict[str, BaseEvaluator]:
        """异步创建所有可用的评估器"""
        if types is None:
            types = cls.DEFAULT_PRIORITY
        
        evaluators = {}
        
        # 并发创建所有评估器
        tasks = []
        for evaluator_type in types:
            task = cls.create_evaluator_async(evaluator_type, config)
            tasks.append((evaluator_type, task))
        
        # 等待所有评估器创建完成
        for evaluator_type, task in tasks:
            evaluator = await task
            if evaluator:
                evaluators[evaluator_type] = evaluator
        
        return evaluators
    
    @classmethod
    def get_evaluator_info(cls) -> Dict[str, Dict[str, Any]]:
        """获取所有评估器信息"""
        info = {}
        
        for name, evaluator_class in cls.EVALUATOR_TYPES.items():
            # 使用临时配置获取信息
            dummy_config = {
                "api_key": "dummy",
                "base_url": "dummy",
                "model": "dummy",
                "timeout": 30
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
        """获取评估器描述"""
        descriptions = {
            "academic": "增强学术评估器 - 支持6维度质量评估（相关性、正确性、完整性、清晰度、连贯性、有用性）",
            "ragas": "Ragas框架评估器 - 完整的RAG评估指标集（相关性、正确性、忠实性、上下文精度、上下文召回率）"
        }
        return descriptions.get(evaluator_type, "无描述")

class EvaluatorManager:
    """评估器管理器"""
    
    def __init__(self, chat_config: Dict[str, Any], embedding_config: Dict[str, Any]):
        """初始化评估器管理器"""
        # 为混合模型评估器准备两种配置
        self.chat_config = chat_config.copy()
        self.embedding_config = embedding_config.copy()
        self.evaluators = {}  # 将在初始化时异步创建
        
        print(f"🔧 评估器管理器初始化完成")
    
    async def initialize_async(self):
        """异步初始化所有评估器"""
        # 为增强学术评估器合并配置
        enhanced_config = {
            **self.chat_config,
            "chat_api_key": self.chat_config.get("api_key"),
            "chat_base_url": self.chat_config.get("base_url"),
            "chat_model": self.chat_config.get("model"),
            "embedding_api_key": self.embedding_config.get("api_key"),
            "embedding_base_url": self.embedding_config.get("base_url"),
            "embedding_model": self.embedding_config.get("model"),
            "evaluation_mode": "hybrid"  # 使用混合模式：embedding计算相关性，聊天模型评估质量
        }
        
        self.evaluators = await EvaluatorFactory.create_all_evaluators_async(enhanced_config)
        
        if not self.evaluators:
            raise ValueError("没有可用的评估器")
        
        print(f"🔧 可用的评估器: {list(self.evaluators.keys())}")
    
    async def evaluate_all_async(self, questions: List[str], answers: List[str], 
                               ground_truths: List[str], contexts: List[List[str]] = None) -> Dict[str, Dict[str, List[float]]]:
        """异步执行所有评估器评估"""
        all_results = {}
        
        for evaluator_name, evaluator in self.evaluators.items():
            print(f"\n📊 使用{evaluator_name}评估器评估中...")
            
            try:
                # 使用带超时的异步评估
                metrics = await evaluator.evaluate_with_timeout(
                    questions, answers, ground_truths, contexts
                )
                all_results[evaluator_name] = metrics
                print(f"    ✅ 完成")
            except Exception as e:
                print(f"    ❌ 失败: {e}")
                # 使用默认值填充
                default_metrics = {metric: [None] * len(answers) 
                                 for metric in evaluator.get_supported_metrics()}
                all_results[evaluator_name] = default_metrics
        
        return all_results
    
    def get_evaluator_summary(self) -> Dict[str, Any]:
        """获取评估器概要"""
        summary = {
            "total_evaluators": len(self.evaluators),
            "available_evaluators": list(self.evaluators.keys()),
            "evaluator_details": {}
        }
        
        for name, evaluator in self.evaluators.items():
            summary["evaluator_details"][name] = evaluator.get_evaluator_info()
        
        return summary