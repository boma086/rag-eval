# RAG连接器基础接口 - 策略模式实现

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import requests
import logging

logger = logging.getLogger(__name__)

class BaseRAGConnector(ABC):
    """RAG连接器抽象基类 - 策略模式"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.system_name = self.__class__.__name__.lower().replace('connector', '')
        
        # 验证配置
        errors = self.validate_config()
        if errors:
            raise ValueError(f"Configuration errors for {self.system_name}: {errors}")
        
        logger.info(f"{self.system_name} connector initialized")
    
    @abstractmethod
    def validate_config(self) -> List[str]:
        """验证配置，返回错误信息列表"""
        pass
    
    @abstractmethod
    def build_request(self, question: str, **kwargs) -> Dict[str, Any]:
        """构建请求配置"""
        pass
    
    @abstractmethod
    def parse_response(self, response_data: Dict[str, Any]) -> Dict[str, Any]:
        """解析响应数据"""
        pass
    
    def query(self, question: str, max_retries: int = 2, **kwargs) -> Dict[str, Any]:
        """
        查询RAG系统
        
        Args:
            question: 要查询的问题
            max_retries: 最大重试次数
            **kwargs: 额外参数
            
        Returns:
            {"answer": str, "contexts": list, "error": str}
        """
        last_error = None
        
        for attempt in range(max_retries + 1):
            try:
                # 构建请求
                request_config = self.build_request(question, **kwargs)
                
                # 发送请求
                response = requests.request(
                    method=request_config["method"],
                    url=request_config["url"],
                    headers=request_config["headers"],
                    json=request_config["body"],
                    timeout=60
                )
                
                # 检查HTTP状态
                response.raise_for_status()
                
                # 解析响应
                response_data = response.json()
                result = self.parse_response(response_data)
                
                logger.debug(f"{self.system_name} query successful on attempt {attempt + 1}")
                return result
                
            except requests.exceptions.RequestException as e:
                last_error = e
                if attempt < max_retries:
                    logger.warning(f"{self.system_name} attempt {attempt + 1} failed, retrying: {e}")
                    continue
                else:
                    error_msg = f"Request failed after {max_retries + 1} attempts: {e}"
                    logger.error(f"{self.system_name} {error_msg}")
                    return {"answer": "", "contexts": [], "error": error_msg}
            
            except Exception as e:
                error_msg = f"Unexpected error: {e}"
                logger.error(f"{self.system_name} {error_msg}")
                return {"answer": "", "contexts": [], "error": error_msg}
    
    def test_connection(self) -> bool:
        """测试连接是否正常"""
        try:
            result = self.query("Hello")
            return not result.get("error") and bool(result.get("answer"))
        except Exception:
            return False
    
    def get_system_info(self) -> Dict[str, Any]:
        """获取系统信息"""
        return {
            "name": self.system_name,
            "description": self.__class__.__doc__ or "",
            "config_valid": len(self.validate_config()) == 0
        }