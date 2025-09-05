# RAG多评价器系统

一个专业的RAG系统评价框架，支持多种评价器和RAG系统的综合评估，专门针对日文应用场景优化。

## 🚀 **快速开始**

### 1. 环境准备
```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Linux/Mac

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置设置

**评价器配置** (`.env.local.evaluator`):
```env
# 聊天模型配置 (用于评分的LLM)
CHAT_API_KEY=your_openrouter_api_key
CHAT_BASE_URL=https://openrouter.ai/api/v1
CHAT_MODEL=moonshotai/kimi-k2:free

# 嵌入模型配置 (用于专用评分的LLM)
EMBEDDING_BASE_URL=http://localhost:11434
EMBEDDING_MODEL=nomic-embed-text:latest
EMBEDDING_API_KEY=
```

**RAG系统配置** (`.env.local.dify`):
```env
DIFY_ENABLED=true
DIFY_API_KEY=your_dify_api_key
DIFY_BASE_URL=https://api.dify.ai/v1
DIFY_USER_ID=rag-evaluator
```

### 3. 启动服务
```bash
# 启动Ollama (需要单独运行)
ollama pull nomic-embed-text:latest
```

### 4. 运行评价
```bash
# 运行完整评价
python3 main_multi_eval_async.py

## 🧪 **测试验证**

运行系统测试：
```bash
python3 test_system.py
```

# 查看结果
# 结果保存在 results/multi_evaluation_results.csv
```

## 🧠 **评价器架构**

### 📊 **当前可用评价器**

#### 1. **学术评价器** (AcademicEvaluator)
- **模型**: 单一聊天模型 (OpenRouter API)
- **指标**: 相关性、正确性、完整性、清晰度
- **特点**: 简单高效，适合快速评估

#### 2. **混合异步评价器** (HybridAsyncEvaluator) 
- **模型**: 嵌入模型 + 聊天模型
- **指标**: 嵌入模型计算语义相似度，聊天模型评估质量维度
- **特点**: 理论更科学，但配置复杂

#### 3. **Ragas评价器** (RagasOllamaEvaluator) 
- **状态**: 🚧 **临时禁用** - 兼容性问题待解决
- **模型**: Ragas框架 + OpenRouter + Ollama
- **指标**: faithfulness, answer_relevancy, context_recall等
- **计划**: 后续版本将重新启用

### 🔄 **评价器选择策略**
- **默认优先级**: HybridAsync > Academic > Ragas
- **异步支持**: 所有评价器都支持异步调用
- **容错机制**: 自动降级到可用评价器

## 🔧 **扩展性**

- 新增RAG系统只需实现`BaseRAGConnector`接口
- 新增评价器只需实现`BaseEvaluator`接口
- 配置化管理，支持多种环境

### 🔌 **RAG系统支持**
- **Dify** - 企业级RAG平台
- **RagFlow** - 开源RAG解决方案
- **通用连接器** - 支持OpenAI兼容的API

## 📋 **输出格式**

评价结果保存为CSV格式，包含：
- 原始问题和答案
- 多个评价器的评分
- 详细的指标分析

## 📁 **项目结构**
```
rag-eval/
├── main_multi_eval_async.py     # 主程序入口
├── config.py                   # 配置管理
├── connectors/                 # RAG连接器（策略模式）
│   ├── base.py                # 基础连接器接口
│   ├── factory.py             # 连接器工厂
│   ├── dify.py                # Dify连接器
│   ├── ragflow.py             # RagFlow连接器
│   └── universal.py           # 通用连接器
├── evaluators/                 # 评价器（策略模式）
│   ├── base.py                # 基础评价器接口
│   ├── async_base.py          # 异步评价器基类
│   ├── factory.py             # 评价器工厂
│   ├── async_factory.py       # 异步评价器工厂
│   ├── academic_evaluator.py  # 学术评价器
│   ├── async_academic_evaluator.py  # 异步学术评价器
│   ├── hybrid_async_evaluator.py   # 混合模型评价器
│   └── ragas_ollama.py        # Ragas评价器(临时禁用)
├── data/                      # 测试数据
│   └── test_cases_jp.json     # 日语测试用例
├── results/                   # 评价结果
├── test_system.py            # 系统测试脚本
└── requirements.txt           # 依赖包
```

## 📝 **添加新的评价问题**

### **1. 编辑测试数据文件**
在 `data/test_cases_jp.json` 中添加新的测试问题：

```json
[
  {
    "question": "新しい日本語学習アプリでユーザー認証をどのように実装すべきですか？",
    "ground_truth": "日本語学習アプリでは、OAuth 2.0とJWTトークンを使用したセキュアな認証を実装し、bcryptでパスワードハッシュ化を行い、過去のプロジェクト経験に基づいて多要素認証を実装してセキュリティを強化することを推奨します。"
  },
  {
    "question": "あなたの新しい質問をここに追加",
    "ground_truth": "対応する正解回答をここに追加"
  }
]
```

### **2. 数据格式说明**
- `question`: 评价的问题（日文）
- `ground_truth`: 标准答案（用于比较RAG系统的回答质量）

### **3. 运行评价**
添加新问题后，重新运行评价：
```bash
python3 main_multi_eval_async.py
```

### **4. 查看结果**
结果会保存在 `results/multi_evaluation_results.csv` 中，包含：
- 原始问题
- 标准答案  
- 各RAG系统的回答
- 各评价器的评分（关联性、正确性、完全性、明確性）

### **5. 注意事项**
- 问题应与您的RAG系统应用场景相关
- 标准答案应简洁、准确，便于比较
- 建议添加5-10个典型问题进行全面评价
- 支持日文、中文、英文等多种语言

## 📄 **许可证**

本项目采用MIT许可证。


