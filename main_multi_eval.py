#!/usr/bin/env python3
# RAG評価システム - 多評価器対応版

import argparse
import sys
import json
import pandas as pd
from pathlib import Path
from config import EVALUATOR_CONFIG, get_enabled_rag_systems, validate_config
from connectors.universal import UniversalRAGConnector
from evaluators.factory import EvaluatorManager

class MultiEvaluatorRAGSystem:
    """多評価器対応RAG評価システム"""
    
    def __init__(self):
        """システムを初期化"""
        # 設定を検証
        config_errors = validate_config()
        if config_errors:
            raise ValueError(f"設定エラー: {config_errors}")
        
        # RAG連接器を初期化
        self.connectors = {}
        enabled_systems = get_enabled_rag_systems()
        
        for system_name, config in enabled_systems.items():
            try:
                connector = UniversalRAGConnector(system_name, config)
                if connector.test_connection():
                    self.connectors[system_name] = connector
                    print(f"✅ {system_name} RAGシステム接続成功")
                else:
                    print(f"❌ {system_name} RAGシステム接続失敗")
            except Exception as e:
                print(f"❌ {system_name} RAGシステム初期化エラー: {e}")
        
        if not self.connectors:
            raise ValueError("評価可能なRAGシステムがありません")
        
        # 評価器マネージャーを初期化（Factory Pattern使用）
        self.evaluator_manager = EvaluatorManager(EVALUATOR_CONFIG)

    def load_test_cases(self, file_path: str) -> list:
        """テストケースを読み込み"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            raise ValueError(f"テストケース読み込み失敗 {file_path}: {e}")

    def query_all_systems(self, questions: list) -> dict:
        """全RAGシステムに質問"""
        import time
        
        results = {system: [] for system in self.connectors.keys()}
        
        for i, question in enumerate(questions):
            print(f"質問 {i+1}/{len(questions)}: {question[:50]}...")
            
            for system_name, connector in self.connectors.items():
                try:
                    result = connector.query(question)
                    answer = result.get("answer", "")
                    if result.get("error"):
                        print(f"  {system_name} エラー: {result['error']}")
                        answer = ""
                    else:
                        print(f"  {system_name} ✅ 成功")
                    results[system_name].append(answer)
                    
                    # リクエスト間隔を追加
                    time.sleep(2)
                    
                except Exception as e:
                    print(f"  {system_name} 例外: {e}")
                    results[system_name].append("")
        
        return results

    def evaluate_with_all_evaluators(self, questions: list, ground_truths: list,
                                   system_answers: dict) -> dict:
        """全評価器で評価（Factory Pattern使用）"""
        all_results = {}

        for system_name, answers in system_answers.items():
            print(f"\n📊 {system_name}システムを評価中...")

            # 評価器マネージャーを使用して全評価器で評価
            system_results = self.evaluator_manager.evaluate_all(
                questions, answers, ground_truths
            )

            # 結果を再構成（システム別→評価器別の構造に変換）
            for evaluator_name, metrics in system_results.items():
                if evaluator_name not in all_results:
                    all_results[evaluator_name] = {}
                all_results[evaluator_name][system_name] = metrics

        return all_results

    def save_results(self, questions: list, ground_truths: list, system_answers: dict, 
                    evaluation_results: dict, output_dir: str) -> str:
        """結果を保存"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # 結果DataFrameを構築
        results_data = {
            "question": questions,
            "ground_truth": ground_truths
        }
        
        # RAGシステムの回答を追加
        for system_name in self.connectors.keys():
            results_data[f"{system_name}_answer"] = system_answers[system_name]
        
        # 各評価器の結果を追加
        for evaluator_name, eval_results in evaluation_results.items():
            for system_name in self.connectors.keys():
                if system_name in eval_results:
                    metrics = eval_results[system_name]
                    for metric_name, scores in metrics.items():
                        col_name = f"{system_name}_{evaluator_name}_{metric_name}"
                        results_data[col_name] = scores
        
        df = pd.DataFrame(results_data)
        csv_path = output_path / "multi_evaluation_results.csv"
        df.to_csv(csv_path, index=False, encoding='utf-8-sig')
        
        return str(csv_path)

    def run_evaluation(self, test_cases_file: str, output_dir: str = "results") -> str:
        """完全な評価フローを実行"""
        print("🚀 多評価器RAG評価開始...")
        
        # 1. テストケースを読み込み
        test_cases = self.load_test_cases(test_cases_file)
        questions = [case["question"] for case in test_cases]
        ground_truths = [case["ground_truth"] for case in test_cases]
        
        print(f"📋 {len(test_cases)}個のテストケースを読み込み")
        print(f"🔌 RAGシステム: {list(self.connectors.keys())}")
        print(f"📊 評価器: {list(self.evaluator_manager.evaluators.keys())}")
        
        # 2. 全RAGシステムに質問
        system_answers = self.query_all_systems(questions)
        
        # 3. 全評価器で評価
        evaluation_results = self.evaluate_with_all_evaluators(questions, ground_truths, system_answers)
        
        # 4. 結果を保存
        result_file = self.save_results(questions, ground_truths, system_answers, 
                                      evaluation_results, output_dir)
        
        print(f"\n✅ 結果を保存: {result_file}")
        return result_file

def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(description="多評価器RAGシステム評価ツール")
    parser.add_argument(
        "--test-cases", 
        default="data/test_cases_jp.json",
        help="テストケースファイルパス (デフォルト: data/test_cases_jp.json)"
    )
    parser.add_argument(
        "--output", 
        default="results",
        help="結果出力ディレクトリ (デフォルト: results)"
    )
    
    args = parser.parse_args()
    
    # テストケースファイルを確認
    if not Path(args.test_cases).exists():
        print(f"❌ テストケースファイルが存在しません: {args.test_cases}")
        sys.exit(1)
    
    try:
        # 評価システムを初期化
        eval_system = MultiEvaluatorRAGSystem()
        
        # 評価を実行
        result_file = eval_system.run_evaluation(args.test_cases, args.output)
        
        print(f"\n🎉 多評価器評価完了！")
        print(f"📊 結果確認: python view_results.py {result_file}")
        
    except Exception as e:
        print(f"❌ 評価失敗: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
