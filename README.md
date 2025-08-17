# RAG Multi-Evaluator System

A professional evaluation framework for RAG (Retrieval-Augmented Generation) systems, supporting comprehensive assessment with multiple evaluators and RAG systems.

## 🌐 **Language / 言語**

- **English** (This document)
- [中文文档](README_CN.md)
- [日本語ドキュメント](README_JP.md)

## 🎯 **Key Features**

### 1. 创建配置
```bash
python generate_config.py --interactive
```

### 2. 运行评价
```bash
python main.py
```

### 3. 查看结果
```bash
python view_results.py
```

## ✨ 特性

- 🎯 **模板化配置** - 支持Dify、RagFlow等主流RAG系统
- 📁 **多配置文件** - 灵活管理不同环境和系统
- 🔄 **自动合并** - 智能合并所有配置文件
- 📊 **专业评价** - 基于相关性和正确性的科学评分
- 🛠️ **用户友好** - 交互式配置向导

## 📋 支持的RAG系统

| 系统 | 描述 | 状态 |
|------|------|------|
| Dify | Dify RAG平台 | ✅ 完全支持 |
| RagFlow | 开源RAG系统 | ✅ 完全支持 |
| OpenAI兼容 | 标准OpenAI API | ✅ 完全支持 |

## 📖 详细文档

查看 [用户手册](MANUAL.md) 获取完整使用指南。

## 🔧 配置示例

### 创建Dify配置
```bash
python generate_config.py --generate dify --name production
```

### 创建多系统配置
```bash
python generate_config.py --generate dify ragflow --name comparison
```

### 查看所有配置
```bash
python generate_config.py --configs
```

## 📊 评价指标

- **相关性** (Answer Relevancy) - 回答与问题的相关程度
- **正确性** (Answer Correctness) - 回答与标准答案的匹配度

## 🛠️ 高级功能

- 多环境配置管理
- 自定义评价参数
- 批量系统对比
- 详细结果分析

## 📚 示例工作流

```bash
# 1. 创建生产环境配置
python generate_config.py --interactive
# 选择: 1 (Dify)
# 配置名称: production

# 2. 创建测试环境配置
python generate_config.py --generate ragflow --name testing

# 3. 查看配置
python generate_config.py --configs

# 4. 运行评价
python main.py

# 5. 查看结果
python view_results.py
```

## 🆘 获取帮助

```bash
# 查看支持的系统
python generate_config.py --list

# 查看系统详情
python generate_config.py --info dify

# 查看帮助
python generate_config.py --help
```

## 📝 许可证

MIT License

---

**开始您的RAG评价之旅！** 🎉
