# RAG多評価器システム

RAG（Retrieval-Augmented Generation）システムの専門的評価フレームワーク。複数の評価器とRAGシステムの総合評価をサポート。

## 🎯 **コア機能**

### 📊 **多評価器アーキテクチャ**
- **Ragas評価器** - 真のRagasフレームワーク（OpenRouter Chat + Ollama Embeddings）
- **Ragas代替評価器** - LLM直接評価でRagas基準を模倣
- **シンプル評価器** - 基本的な関連性・正確性評価
- **学術的評価器** - 4次元専門評価（関連性・正確性・完全性・明確性）

### 🔌 **RAGシステム対応**
- **Dify** - エンタープライズRAGプラットフォーム
- **RagFlow** - オープンソースRAGソリューション
- **汎用コネクター** - OpenAI互換API対応

### 🏗️ **デザインパターン**
- **ファクトリーパターン** - 評価器の統一作成・管理
- **ストラテジーパターン** - 柔軟な評価戦略選択
- **アダプターパターン** - 統一RAGシステムインターフェース

## 🚀 **クイックスタート**

### 1. 環境準備

```bash
# 仮想環境作成
python -m venv venv
source venv/bin/activate  # Linux/Mac
# または venv\Scripts\activate  # Windows

# 依存関係インストール
pip install -r requirements.txt
```

### 2. 設定

設定ファイルを作成：

**`.env.local.evaluator`** (評価器設定):
```env
# 評価器設定 (スコアリング用LLM)
OPENROUTER_API_KEY=your_openrouter_api_key
EVALUATOR_BASE_URL=https://openrouter.ai/api/v1
EVALUATOR_MODEL=deepseek/deepseek-r1-distill-llama-70b:free

# Ollama Embeddings設定
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_EMBEDDING_MODEL=nomic-embed-text:latest
```

**`.env.local.dify`** (Dify RAGシステム):
```env
DIFY_ENABLED=true
DIFY_API_KEY=your_dify_api_key
DIFY_BASE_URL=https://api.dify.ai/v1
DIFY_USER_ID=your_user_id
```

### 3. Ollamaサービス起動

```bash
# Ollamaインストール・起動
ollama serve

# 埋め込みモデル取得
ollama pull nomic-embed-text:latest
```

### 4. 評価実行

```bash
# 多評価器評価実行
python main_multi_eval.py

# 結果確認
python view_results.py results/multi_evaluation_results.csv
```

## 📋 **設定要件詳細**

### 🔧 **評価器設定**

| 設定項目 | 説明 | 例 |
|---------|------|-----|
| `EVALUATOR_MODEL` | Chatモデル（プレフィックス必須） | `deepseek/deepseek-r1-distill-llama-70b:free` |
| `OLLAMA_EMBEDDING_MODEL` | 埋め込みモデル | `nomic-embed-text:latest` |

⚠️ **重要**: 
- OpenRouterモデルはプレフィックス必須（例：`openai/gpt-4`, `deepseek/deepseek-r1`）
- 埋め込みモデルをChatモデルとして使用不可
- RagasにはChatモデルとEmbeddingモデル両方が必要

### 🎯 **評価器タイプ**

1. **ragas** - 真のRagasフレームワーク
   - OpenRouter Chatモデルで評価生成
   - Ollama Embeddingsで類似度計算
   - answer_relevancy、answer_correctness指標対応

2. **ragas_alt** - Ragas代替案
   - 純粋LLM評価でRagas基準を模倣
   - relevancy、correctness、faithfulness指標対応

3. **simple** - シンプル評価器
   - 基本的な関連性・正確性評価
   - 高速評価に適用

4. **academic** - 学術的評価器
   - 4次元評価：関連性・正確性・完全性・明確性
   - 詳細分析に適用

## 🏗️ **プロジェクト構造**

```
ragas/
├── evaluators/                 # 評価器モジュール
│   ├── __init__.py             # モジュールエクスポート
│   ├── base.py                 # 基底評価器インターフェース
│   ├── factory.py              # ファクトリーパターン実装
│   ├── ragas_ollama.py         # Ragas+Ollama評価器
│   ├── ragas_alternative.py    # Ragas代替評価器
│   ├── simple_evaluator.py     # シンプル評価器
│   └── academic_evaluator.py   # 学術的評価器
├── connectors/                 # RAGシステムコネクター
│   ├── __init__.py
│   ├── base.py                 # 基底コネクターインターフェース
│   ├── universal.py            # 汎用RAGコネクター
│   ├── dify.py                 # Difyコネクター
│   └── ragflow.py              # RagFlowコネクター
├── data/                       # テストデータ
│   └── test_cases_jp.json      # 日本語テストケース
├── results/                    # 評価結果
├── config.py                   # 設定管理
├── main_multi_eval.py          # メインプログラム
├── view_results.py             # 結果ビューアー
└── requirements.txt            # 依存関係リスト
```

## 🔍 **使用例**

### プログラミングインターフェース

```python
from evaluators.factory import EvaluatorManager
from config import EVALUATOR_CONFIG

# 評価器マネージャー初期化
manager = EvaluatorManager(EVALUATOR_CONFIG)

# 評価データ準備
questions = ["ユーザー認証をどのように実装すべきですか？"]
answers = ["OAuth 2.0とJWTトークンを使用します。"]
ground_truths = ["OAuth 2.0とJWTでセキュアな認証を実装することを推奨します。"]

# 評価実行
results = manager.evaluate_all(questions, answers, ground_truths)
print(results)
```

### コマンドライン使用

```bash
# カスタムテストケース使用
python main_multi_eval.py --test-cases data/my_test_cases.json

# 出力ディレクトリ指定
python main_multi_eval.py --output my_results/
```

## 📊 **評価結果フォーマット**

評価結果はCSV形式で保存され、以下の列を含みます：

- `question` - テスト質問
- `ground_truth` - 標準回答
- `{system}_answer` - RAGシステム回答
- `{system}_{evaluator}_{metric}` - 評価スコア

例：
```csv
question,ground_truth,dify_answer,dify_ragas_relevancy,dify_ragas_correctness,...
認証実装方法は？,OAuth 2.0使用...,OAuth 2.0とJWT推奨...,0.85,0.92,...
```

## 🛠️ **トラブルシューティング**

### よくある問題

1. **405エラー** - モデルタイプエラー
   - Chatモデル使用確認（Embeddingモデルではない）
   - モデル名に正しいプレフィックス確認

2. **Embeddingsエラー** - `'str' object has no attribute 'data'`
   - OpenRouterはEmbeddings API未対応
   - OllamaでEmbeddingsサービス提供

3. **接続タイムアウト**
   - ネットワーク接続確認
   - タイムアウト時間設定増加

### デバッグモード

```bash
# 詳細ログ有効化
export PYTHONPATH=.
python -c "
from evaluators.factory import EvaluatorFactory
info = EvaluatorFactory.get_evaluator_info()
print(info)
"
```

## 🤝 **貢献ガイド**

1. プロジェクトをフォーク
2. 機能ブランチ作成 (`git checkout -b feature/AmazingFeature`)
3. 変更をコミット (`git commit -m 'Add some AmazingFeature'`)
4. ブランチにプッシュ (`git push origin feature/AmazingFeature`)
5. プルリクエスト開始

## 📄 **ライセンス**

このプロジェクトはMITライセンスの下で配布されています - 詳細は [LICENSE](LICENSE) ファイルを参照してください。

## 🙏 **謝辞**

- [Ragas](https://github.com/explodinggradients/ragas) - RAG評価フレームワーク
- [Ollama](https://ollama.ai/) - ローカルLLMサービス
- [OpenRouter](https://openrouter.ai/) - LLM APIサービス
