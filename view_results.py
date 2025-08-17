#!/usr/bin/env python3
# RAG评价结果查看器 - 精简版

import pandas as pd
import sys
from pathlib import Path

def format_score(score):
    """スコア表示をフォーマット"""
    if pd.isna(score) or score == "":
        return "❌ 未評価"
    try:
        score_float = float(score)
        if score_float >= 0.8:
            return f"🟢 {score_float:.3f}"
        elif score_float >= 0.6:
            return f"🟡 {score_float:.3f}"
        else:
            return f"🔴 {score_float:.3f}"
    except:
        return "❌ スコアエラー"

def clean_answer(answer):
    """回答表示をクリーンアップ"""
    if not answer or pd.isna(answer):
        return "❌ 回答なし"

    answer = str(answer)
    if len(answer) > 100:
        answer = answer[:100] + "..."
    return answer

def analyze_results(df):
    """評価結果を分析"""
    print("📊 評価結果分析")
    print("=" * 60)

    total_questions = len(df)
    print(f"総質問数: {total_questions}")

    # 各システムを分析
    systems = []
    for col in df.columns:
        if col.endswith('_answer'):
            system_name = col.replace('_answer', '')
            systems.append(system_name)

    for system in systems:
        answer_col = f"{system}_answer"
        relevancy_col = f"{system}_relevancy"
        correctness_col = f"{system}_correctness"

        answered = df[answer_col].notna().sum() if answer_col in df.columns else 0
        scored_relevancy = df[relevancy_col].notna().sum() if relevancy_col in df.columns else 0
        scored_correctness = df[correctness_col].notna().sum() if correctness_col in df.columns else 0

        print(f"\n🔵 {system.upper()}:")
        print(f"  回答質問数: {answered}/{total_questions}")
        print(f"  関連性評価数: {scored_relevancy}/{total_questions}")
        print(f"  正確性評価数: {scored_correctness}/{total_questions}")

        if scored_relevancy > 0:
            avg_relevancy = df[relevancy_col].dropna().mean()
            print(f"  平均関連性: {avg_relevancy:.3f}")

        if scored_correctness > 0:
            avg_correctness = df[correctness_col].dropna().mean()
            print(f"  平均正確性: {avg_correctness:.3f}")

def display_detailed_results(df):
    """詳細結果を表示"""
    print("\n📋 詳細評価結果")
    print("=" * 80)

    # システムリストを取得
    systems = []
    for col in df.columns:
        if col.endswith('_answer'):
            system_name = col.replace('_answer', '')
            systems.append(system_name)

    for idx, row in df.iterrows():
        print(f"\n❓ 質問 {idx + 1}:")
        print(f"   {row['question']}")
        print(f"\n📚 標準回答:")
        print(f"   {clean_answer(row['ground_truth'])}")

        for system in systems:
            answer_col = f"{system}_answer"
            relevancy_col = f"{system}_relevancy"
            correctness_col = f"{system}_correctness"

            print(f"\n🔵 {system.upper()} 回答:")
            answer = clean_answer(row.get(answer_col, ''))
            if answer == "❌ 回答なし":
                print(f"   {answer}")
            else:
                # 長い回答を行分割して表示し、可読性を向上
                lines = answer.split('\n')
                for line in lines:
                    if line.strip():
                        print(f"   {line}")

            print(f"   📊 関連性スコア: {format_score(row.get(relevancy_col, ''))}")
            print(f"   📊 正確性スコア: {format_score(row.get(correctness_col, ''))}")

        print("-" * 80)

def main():
    """メイン関数"""
    if len(sys.argv) < 2:
        results_file = "results/evaluation_results.csv"
    else:
        results_file = sys.argv[1]
    
    if not Path(results_file).exists():
        print(f"❌ 結果ファイルが存在しません: {results_file}")
        print("まず評価を実行してください: python main.py")
        sys.exit(1)
    
    try:
        df = pd.read_csv(results_file)
        print(f"📁 評価結果を読み込み: {results_file}")
        print(f"📊 データ形状: {df.shape}")

        # 結果を分析
        analyze_results(df)

        # 詳細結果の表示を確認
        show_details = input("\n❓ 詳細結果を表示しますか? (y/N): ").lower().strip()
        if show_details in ['y', 'yes']:
            display_detailed_results(df)

        print("\n✅ 結果確認完了！")

    except Exception as e:
        print(f"❌ 結果ファイルの読み取りに失敗しました: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
