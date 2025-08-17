# 通用RAG连接器 - 基于模板系统

import requests
import logging
from typing import Dict, Any
from templates.processor import TemplateProcessor

logger = logging.getLogger(__name__)

class UniversalRAGConnector:
    """通用RAG连接器 - 支持所有模板化的RAG系统"""
    
    def __init__(self, system_name: str, config: Dict[str, Any]):
        """
        初始化通用连接器
        
        Args:
            system_name: RAG系统名称 (dify, ragflow, openai_compatible等)
            config: 系统配置
        """
        self.system_name = system_name
        self.config = config
        self.processor = TemplateProcessor(system_name, config)
        
        # 验证配置
        errors = self.processor.validate_config()
        if errors:
            raise ValueError(f"Configuration errors for {system_name}: {errors}")
        
        logger.info(f"Universal connector initialized for {system_name}")
    
    def query(self, question: str, max_retries: int = 2, **kwargs) -> Dict[str, Any]:
        """
        查询RAG系统

        Args:
            question: 要查询的问题
            max_retries: 最大重试次数
            **kwargs: 额外参数 (如自定义inputs等)

        Returns:
            {"answer": str, "contexts": list, "error": str}
        """
        last_error = None

        for attempt in range(max_retries + 1):
            try:
                # 构建请求配置
                request_config = self.processor.build_request_config(question, **kwargs)

                # 发送请求
                response = requests.request(
                    method=request_config["method"],
                    url=request_config["url"],
                    headers=request_config["headers"],
                    json=request_config["body"],
                    timeout=60  # 增加到60秒
                )

                # 检查HTTP状态
                response.raise_for_status()

                # 解析响应
                response_data = response.json()
                result = self.processor.parse_response(response_data)

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
            "template": self.processor.template["name"],
            "description": self.processor.template["description"],
            "config_valid": len(self.processor.validate_config()) == 0
        }
