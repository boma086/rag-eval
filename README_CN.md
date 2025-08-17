# RAG多评价器系统

一个专业的RAG（检索增强生成）系统评价框架，支持多种评价器和RAG系统的综合评估。

## 🎯 **核心特性**

### 📊 **多评价器架构**
- **Ragas评价器** - 使用真正的Ragas框架（OpenRouter Chat + Ollama Embeddings）
- **Ragas替代评价器** - LLM直接评价，模拟Ragas评价标准
- **简单评价器** - 基础的关联性和正确性评价
- **学术评价器** - 四维专业评价（关联性、正确性、完整性、清晰度）

### 🔌 **RAG系统支持**
- **Dify** - 企业级RAG平台
- **RagFlow** - 开源RAG解决方案
- **通用连接器** - 支持OpenAI兼容的API

### 🏗️ **设计模式**
- **工厂模式** - 统一评价器创建和管理
- **策略模式** - 灵活的评价策略选择
- **适配器模式** - 统一的RAG系统接口

## 🚀 **快速开始**

### 1. 环境准备

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置设置

创建配置文件：

**`.env.local.evaluator`** (评价器配置):
```env
# 评价器配置 (用于评分的LLM)
OPENROUTER_API_KEY=your_openrouter_api_key
EVALUATOR_BASE_URL=https://openrouter.ai/api/v1
EVALUATOR_MODEL=deepseek/deepseek-r1-distill-llama-70b:free

# Ollama Embeddings设置
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_EMBEDDING_MODEL=nomic-embed-text:latest
```

**`.env.local.dify`** (Dify RAG系统):
```env
DIFY_ENABLED=true
DIFY_API_KEY=your_dify_api_key
DIFY_BASE_URL=https://api.dify.ai/v1
DIFY_USER_ID=your_user_id
```

### 3. 启动Ollama服务

```bash
# 安装并启动Ollama
ollama serve

# 拉取嵌入模型
ollama pull nomic-embed-text:latest
```

### 4. 运行评价

```bash
# 运行多评价器评价
python main_multi_eval.py

# 查看结果
python view_results.py results/multi_evaluation_results.csv
```

## 📋 **配置要求详解**

### 🔧 **评价器配置**

| 配置项 | 说明 | 示例 |
|--------|------|------|
| `EVALUATOR_MODEL` | Chat模型（必须带前缀） | `deepseek/deepseek-r1-distill-llama-70b:free` |
| `OLLAMA_EMBEDDING_MODEL` | 嵌入模型 | `nomic-embed-text:latest` |

⚠️ **重要**: 
- OpenRouter模型必须带前缀（如 `openai/gpt-4`, `deepseek/deepseek-r1`）
- 不能使用嵌入模型作为Chat模型
- Ragas需要Chat模型和Embedding模型两种

### 🎯 **评价器类型**

1. **ragas** - 真正的Ragas框架
   - 使用OpenRouter Chat模型进行评价生成
   - 使用Ollama Embeddings进行相似度计算
   - 支持answer_relevancy和answer_correctness指标

2. **ragas_alt** - Ragas替代方案
   - 纯LLM评价，模拟Ragas评价标准
   - 支持relevancy、correctness、faithfulness指标

3. **simple** - 简单评价器
   - 基础的关联性和正确性评价
   - 适合快速评估

4. **academic** - 学术评价器
   - 四维评价：关联性、正确性、完整性、清晰度
   - 适合详细分析

## 🏗️ **项目结构**

```
ragas/
├── evaluators/                 # 评价器模块
│   ├── __init__.py             # 模块导出
│   ├── base.py                 # 基础评价器接口
│   ├── factory.py              # 工厂模式实现
│   ├── ragas_ollama.py         # Ragas+Ollama评价器
│   ├── ragas_alternative.py    # Ragas替代评价器
│   ├── simple_evaluator.py     # 简单评价器
│   └── academic_evaluator.py   # 学术评价器
├── connectors/                 # RAG系统连接器
│   ├── __init__.py
│   ├── base.py                 # 基础连接器接口
│   ├── universal.py            # 通用RAG连接器
│   ├── dify.py                 # Dify连接器
│   └── ragflow.py              # RagFlow连接器
├── data/                       # 测试数据
│   └── test_cases_jp.json      # 日语测试用例
├── results/                    # 评价结果
├── config.py                   # 配置管理
├── main_multi_eval.py          # 主程序
├── view_results.py             # 结果查看器
└── requirements.txt            # 依赖列表
```

## 🔍 **使用示例**

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
print(results)
```

### 命令行使用

```bash
# 使用自定义测试用例
python main_multi_eval.py --test-cases data/my_test_cases.json

# 指定输出目录
python main_multi_eval.py --output my_results/
```

## 📊 **评价结果格式**

评价结果保存为CSV格式，包含以下列：

- `question` - 测试问题
- `ground_truth` - 标准答案
- `{system}_answer` - RAG系统回答
- `{system}_{evaluator}_{metric}` - 评价分数

示例：
```csv
question,ground_truth,dify_answer,dify_ragas_relevancy,dify_ragas_correctness,...
如何实现认证？,使用OAuth 2.0...,推荐OAuth 2.0和JWT...,0.85,0.92,...
```

## 🛠️ **故障排除**

### 常见问题

1. **405错误** - 模型类型错误
   - 确保使用Chat模型，不是Embedding模型
   - 检查模型名称是否包含正确前缀

2. **Embeddings错误** - `'str' object has no attribute 'data'`
   - OpenRouter不支持Embeddings API
   - 使用Ollama提供Embeddings服务

3. **连接超时**
   - 检查网络连接
   - 增加超时时间设置

### 调试模式

```bash
# 启用详细日志
export PYTHONPATH=.
python -c "
from evaluators.factory import EvaluatorFactory
info = EvaluatorFactory.get_evaluator_info()
print(info)
"
```

## 🤝 **贡献指南**

1. Fork项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

## 📄 **许可证**

本项目采用MIT许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 **致谢**

- [Ragas](https://github.com/explodinggradients/ragas) - RAG评价框架
- [Ollama](https://ollama.ai/) - 本地LLM服务
- [OpenRouter](https://openrouter.ai/) - LLM API服务
