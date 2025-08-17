# RAG多评价器系统用户手册

## 🚀 快速开始

### 1. 配置设置
```bash
# 复制配置示例
cp config_examples/evaluator_openrouter_ollama.env .env.local.evaluator
cp config_examples/rag_dify.env .env.local.dify

# 编辑配置文件，填入API密钥
nano .env.local.evaluator
nano .env.local.dify
```

### 2. 启动Ollama服务
```bash
ollama serve
ollama pull nomic-embed-text:latest
```

### 3. 运行多评价器评价
```bash
python main_multi_eval.py
```

### 4. 查看直观评分结果
```bash
python score_viewer.py
```

---

## 📋 详细使用指南

### 🔧 配置管理

#### 评价器配置选项
系统支持多种评价器配置，选择适合你的服务：

```bash
# OpenRouter + Ollama (推荐)
cp config_examples/evaluator_openrouter_ollama.env .env.local.evaluator

# 纯OpenAI
cp config_examples/evaluator_openai.env .env.local.evaluator

# Google Gemini + Ollama
cp config_examples/evaluator_gemini_ollama.env .env.local.evaluator

# 纯Ollama (本地)
cp config_examples/evaluator_ollama_only.env .env.local.evaluator
```

#### RAG系统配置
```bash
# Dify平台
cp config_examples/rag_dify.env .env.local.dify

# 通用OpenAI兼容API
cp config_examples/rag_universal_openai.env .env.local.universal
```

### 📊 多评价器系统

系统包含四种评价器，提供多角度评价：

#### 1. Ragas评价器 (ragas)
- **真正的Ragas框架** - 使用OpenRouter Chat + Ollama Embeddings
- **评价指标**: answer_relevancy, answer_correctness
- **优势**: 学术标准，专业RAG评价

#### 2. Ragas替代评价器 (ragas_alt)
- **LLM直接评价** - 模拟Ragas评价标准
- **评价指标**: relevancy, correctness, faithfulness
- **优势**: 无需Embeddings，更稳定

#### 3. 简单评价器 (simple)
- **基础评价** - 关联性和正确性
- **评价指标**: relevancy, correctness
- **优势**: 快速评价，易于理解

#### 4. 学术评价器 (academic)
- **四维评价** - 全面专业评价
- **评价指标**: relevancy, correctness, completeness, clarity
- **优势**: 详细分析，适合研究

### 🎯 评分等级系统

- 🏆 **优秀** (0.9+) - 表现卓越
- 🥇 **良好** (0.8+) - 表现良好
- 🥈 **中等** (0.7+) - 表现一般
- 🥉 **及格** (0.6+) - 基本合格
- ❌ **需改进** (<0.6) - 需要优化

## 🔍 使用示例

### 命令行使用
```bash
# 使用默认配置运行
python main_multi_eval.py

# 使用自定义测试用例
python main_multi_eval.py --test-cases data/my_test_cases.json

# 指定输出目录
python main_multi_eval.py --output my_results/

# 查看直观评分
python score_viewer.py results/multi_evaluation_results.csv

# 查看详细结果
python view_results.py results/multi_evaluation_results.csv

# 导出报告
python export_results.py results/multi_evaluation_results.csv
```

### 编程接口使用
```python
from evaluators.factory import EvaluatorManager
from config import EVALUATOR_CONFIG

# 初始化评价器管理器
manager = EvaluatorManager(EVALUATOR_CONFIG)

# 准备评价数据
questions = ["如何实现用户认证？"]
answers = ["使用OAuth 2.0和JWT令牌。"]
ground_truths = ["推荐使用OAuth 2.0和JWT实现安全认证。"]

# 执行评价
results = manager.evaluate_all(questions, answers, ground_truths)

# 查看结果
for evaluator_name, metrics in results.items():
    print(f"{evaluator_name}: {metrics}")
```

## 🛠️ 故障排除

### 常见问题

#### 1. 405错误 - 模型类型错误
```
ValueError: 405 Method Not Allowed
```
**原因**: 使用了Embedding模型作为Chat模型
**解决**: 确保`EVALUATOR_MODEL`是Chat模型，如`deepseek/deepseek-r1-distill-llama-70b:free`

#### 2. Embeddings错误
```
AttributeError: 'str' object has no attribute 'data'
```
**原因**: OpenRouter不支持Embeddings API
**解决**: 使用Ollama提供Embeddings服务

#### 3. 连接超时
```
ConnectionError: Connection timeout
```
**原因**: 网络连接问题或服务不可用
**解决**: 检查网络连接，确认服务状态

### 调试模式
```bash
# 检查评价器状态
python -c "
from evaluators.factory import EvaluatorFactory
info = EvaluatorFactory.get_evaluator_info()
for name, details in info.items():
    print(f'{name}: {details}')
"

# 测试Ollama连接
curl http://localhost:11434/api/tags

# 测试OpenRouter连接
curl -H "Authorization: Bearer YOUR_API_KEY" https://openrouter.ai/api/v1/models
```

---

## 🎯 支持的RAG系统

### 1. Dify
- **描述**: Dify RAG平台，支持多种AI应用
- **必需配置**: API密钥、API地址
- **可选配置**: 用户ID、应用ID

### 2. RagFlow
- **描述**: RagFlow开源RAG系统
- **必需配置**: API密钥、服务地址
- **可选配置**: Chat Assistant ID（自动检测）

### 3. OpenAI兼容系统
- **描述**: 支持OpenAI API格式的RAG系统
- **必需配置**: API密钥、API地址
- **可选配置**: 模型名称、系统提示词

---

## 📊 评价流程

### 1. 测试用例准备
创建 `data/test_cases.json` 文件：
```json
[
    {
        "question": "How should we implement user authentication?",
        "ground_truth": "Use OAuth 2.0 with JWT tokens for secure authentication..."
    },
    {
        "question": "What database design approach should we use?",
        "ground_truth": "Use PostgreSQL with normalized tables..."
    }
]
```

### 2. 运行评价
```bash
# 使用默认测试用例（英文）
python main.py

# 使用中文测试用例
python main.py --test-cases data/test_cases_chinese.json

# 指定输出目录
python main.py --output results_2024
```

### 3. 查看结果
```bash
# 查看最新结果（中文友好显示）
python view_results.py

# 查看指定结果文件
python view_results.py results/evaluation_results.csv

# 导出中文报告
python export_results.py
```

---

## 🔧 高级功能

### 多环境配置
```bash
# 创建生产环境配置
python generate_config.py --generate dify --name production

# 创建测试环境配置  
python generate_config.py --generate dify --name testing

# 系统会自动合并所有配置
python main.py
```

### 自定义参数
在配置文件中添加自定义参数：
```env
# Dify自定义输入
DIFY_BACKGROUND=You are a technical assistant for software engineering
DIFY_INSTRUCTION=Answer concisely and provide code examples when helpful
```

### 批量测试
```bash
# 创建多个RAG系统配置
python generate_config.py --generate dify ragflow --name comparison

# 运行对比评价
python main.py
```

---

## 🛠️ 故障排除

### 常见问题

#### 1. 配置文件未找到
```bash
# 检查配置文件
python generate_config.py --configs

# 重新创建配置
python generate_config.py --interactive
```

#### 2. RAG系统连接失败
```bash
# 检查API密钥和地址
python generate_config.py --info dify

# 测试连接
python -c "
from connectors.universal import UniversalRAGConnector
connector = UniversalRAGConnector('dify', {'api_key': 'your-key', 'base_url': 'your-url'})
print(connector.test_connection())
"
```

#### 3. 评价失败
- 检查OpenRouter API密钥是否有效
- 确认测试用例格式正确
- 查看详细错误信息

### 调试模式
```bash
# 启用详细日志
export PYTHONPATH=.
python -c "
import logging
logging.basicConfig(level=logging.DEBUG)
from evaluator import RAGEvaluator
evaluator = RAGEvaluator()
"
```

---

## 📚 最佳实践

### 1. 配置管理
- 为不同环境创建独立配置文件
- 使用有意义的配置名称
- 定期备份重要配置

### 2. 测试用例设计
- 覆盖不同类型的问题
- 提供高质量的标准答案
- 定期更新测试用例

### 3. 结果分析
- 关注相关性和正确性评分
- 比较不同RAG系统的表现
- 记录改进建议

---

## 🆘 获取帮助

### 命令行帮助
```bash
python generate_config.py --help
python main.py --help
python view_results.py --help
```

### 系统信息
```bash
# 查看支持的RAG系统
python generate_config.py --list

# 查看特定系统信息
python generate_config.py --info dify

# 查看现有配置
python generate_config.py --configs
```

### 示例工作流
```bash
# 1. 创建Dify配置
python generate_config.py --interactive
# 选择: 1 (Dify)
# 配置名称: production

# 2. 编辑配置文件
# 编辑 .env.local.production，填入真实API密钥

# 3. 运行评价
python main.py

# 4. 查看结果
python view_results.py
```

---

## 📝 更新日志

- **v1.0**: 基础评价功能
- **v2.0**: 模板化配置系统
- **v3.0**: 多配置文件支持

---

**祝您使用愉快！** 🎉
