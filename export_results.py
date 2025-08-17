#!/usr/bin/env python3
# RAG评价结果导出工具 - 生成中文友好的报告

import pandas as pd
import sys
from pathlib import Path
from datetime import datetime

def export_to_japanese_report(csv_file: str, output_file: str = None):
    """日本語フレンドリーな評価レポートを出力"""

    if not Path(csv_file).exists():
        print(f"❌ 結果ファイルが存在しません: {csv_file}")
        return

    # データを読み込み
    df = pd.read_csv(csv_file)

    # 出力ファイル名を生成
    if not output_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"results/評価レポート_{timestamp}.txt"
    
    # 获取系统列表
    systems = []
    for col in df.columns:
        if col.endswith('_answer'):
            system_name = col.replace('_answer', '')
            systems.append(system_name)
    
    # レポート内容を生成
    report_lines = []
    report_lines.append("RAGシステム評価レポート")
    report_lines.append("=" * 50)
    report_lines.append(f"生成時刻: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}")
    report_lines.append(f"テスト質問数: {len(df)}")
    report_lines.append(f"参加システム: {', '.join([s.upper() for s in systems])}")
    report_lines.append("")

    # システム概要
    report_lines.append("📊 システムパフォーマンス概要")
    report_lines.append("-" * 30)

    for system in systems:
        answer_col = f"{system}_answer"
        answered = df[answer_col].notna().sum()
        report_lines.append(f"{system.upper()}: {answered}/{len(df)} 問に回答")

    report_lines.append("")

    # 詳細な質疑応答
    report_lines.append("📋 詳細質疑応答記録")
    report_lines.append("-" * 30)
    
    for idx, row in df.iterrows():
        report_lines.append(f"\n質問 {idx + 1}:")
        report_lines.append(f"Q: {row['question']}")
        report_lines.append(f"\n標準回答:")
        report_lines.append(f"A: {row['ground_truth']}")

        for system in systems:
            answer_col = f"{system}_answer"
            answer = row.get(answer_col, "")

            report_lines.append(f"\n{system.upper()} 回答:")
            if pd.isna(answer) or answer == "":
                report_lines.append("A: [回答なし]")
            else:
                # 長い回答を処理し、適切な改行を追加
                lines = str(answer).split('\n')
                for line in lines:
                    if line.strip():
                        report_lines.append(f"A: {line}")

        report_lines.append("\n" + "=" * 50)
    
    # 写入文件
    Path(output_file).parent.mkdir(exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
    
    print(f"✅ 日本語レポートが生成されました: {output_file}")
    return output_file

def export_to_excel(csv_file: str, output_file: str = None):
    """Excel形式のレポートを出力"""

    if not Path(csv_file).exists():
        print(f"❌ 結果ファイルが存在しません: {csv_file}")
        return

    # データを読み込み
    df = pd.read_csv(csv_file)

    # 出力ファイル名を生成
    if not output_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"results/評価レポート_{timestamp}.xlsx"

    # 列名を日本語に変更
    column_mapping = {
        'question': '質問',
        'ground_truth': '標準回答'
    }
    
    # システムリストを取得し、名前を変更
    systems = []
    for col in df.columns:
        if col.endswith('_answer'):
            system_name = col.replace('_answer', '')
            systems.append(system_name)
            column_mapping[col] = f'{system_name.upper()}_回答'
            column_mapping[f'{system_name}_relevancy'] = f'{system_name.upper()}_関連性'
            column_mapping[f'{system_name}_correctness'] = f'{system_name.upper()}_正確性'

    # 列名を変更
    df_japanese = df.rename(columns=column_mapping)

    # Excelに書き込み
    Path(output_file).parent.mkdir(exist_ok=True)
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        df_japanese.to_excel(writer, sheet_name='評価結果', index=False)

    print(f"✅ Excelレポートが生成されました: {output_file}")
    return output_file

def main():
    """メイン関数"""
    if len(sys.argv) < 2:
        csv_file = "results/evaluation_results.csv"
    else:
        csv_file = sys.argv[1]

    if not Path(csv_file).exists():
        print(f"❌ 結果ファイルが存在しません: {csv_file}")
        print("まず評価を実行してください: python main.py")
        sys.exit(1)

    print("📊 RAG評価結果エクスポートツール")
    print("=" * 30)

    # 日本語テキストレポートを生成
    txt_file = export_to_japanese_report(csv_file)

    # Excelレポートの生成を試行
    try:
        excel_file = export_to_excel(csv_file)
        print(f"\n📁 生成されたファイル:")
        print(f"  テキストレポート: {txt_file}")
        print(f"  Excelレポート: {excel_file}")
    except ImportError:
        print(f"\n📁 生成されたファイル:")
        print(f"  テキストレポート: {txt_file}")
        print("💡 openpyxlをインストールするとExcelレポートが生成できます: pip install openpyxl")
    except Exception as e:
        print(f"⚠️  Excelエクスポートに失敗しました: {e}")
        print(f"📁 テキストレポート: {txt_file}")

if __name__ == "__main__":
    main()
