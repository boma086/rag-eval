#!/usr/bin/env python3
# 直观评分查看器 - 提供清晰的评分总结

import pandas as pd
import sys
from pathlib import Path

def calculate_overall_score(scores):
    """计算总体评分"""
    valid_scores = [s for s in scores if s is not None and pd.notna(s)]
    if not valid_scores:
        return None
    return sum(valid_scores) / len(valid_scores)

def get_score_grade(score):
    """获取评分等级"""
    if score is None:
        return "❌ 未评价"
    elif score >= 0.9:
        return "🏆 优秀"
    elif score >= 0.8:
        return "🥇 良好"
    elif score >= 0.7:
        return "🥈 中等"
    elif score >= 0.6:
        return "🥉 及格"
    else:
        return "❌ 需改进"

def view_scores(csv_file):
    """查看评分结果"""
    if not Path(csv_file).exists():
        print(f"❌ 文件不存在: {csv_file}")
        return
    
    df = pd.read_csv(csv_file)
    
    print("🎯 RAG系统评价结果总览")
    print("=" * 60)
    
    # 识别RAG系统
    rag_systems = []
    for col in df.columns:
        if col.endswith('_answer'):
            system_name = col.replace('_answer', '')
            rag_systems.append(system_name)
    
    # 识别评价器
    evaluators = set()
    for col in df.columns:
        for system in rag_systems:
            if col.startswith(f"{system}_") and not col.endswith('_answer'):
                parts = col.replace(f"{system}_", "").split('_')
                if len(parts) >= 2:
                    evaluator = parts[0]
                    evaluators.add(evaluator)
    
    evaluators = sorted(list(evaluators))
    
    print(f"📊 RAG系统: {', '.join(rag_systems)}")
    print(f"🔍 评价器: {', '.join(evaluators)}")
    print(f"❓ 测试问题数: {len(df)}")
    print()
    
    # 为每个RAG系统显示评分
    for system in rag_systems:
        print(f"🔵 {system.upper()} 系统评价")
        print("-" * 40)
        
        system_scores = {}
        
        # 收集该系统的所有评分
        for evaluator in evaluators:
            evaluator_scores = {}
            
            for col in df.columns:
                if col.startswith(f"{system}_{evaluator}_"):
                    metric = col.replace(f"{system}_{evaluator}_", "")
                    scores = df[col].tolist()
                    avg_score = calculate_overall_score(scores)
                    evaluator_scores[metric] = avg_score
            
            if evaluator_scores:
                system_scores[evaluator] = evaluator_scores
        
        # 显示评分
        for evaluator, metrics in system_scores.items():
            print(f"  📊 {evaluator}评价器:")
            
            total_scores = []
            for metric, score in metrics.items():
                grade = get_score_grade(score)
                if score is not None:
                    print(f"    {metric}: {score:.3f} {grade}")
                    total_scores.append(score)
                else:
                    print(f"    {metric}: {grade}")
            
            # 计算该评价器的总体评分
            if total_scores:
                overall = sum(total_scores) / len(total_scores)
                overall_grade = get_score_grade(overall)
                print(f"    📈 总体评分: {overall:.3f} {overall_grade}")
            
            print()
        
        # 计算系统总体评分
        all_system_scores = []
        for evaluator_metrics in system_scores.values():
            for score in evaluator_metrics.values():
                if score is not None:
                    all_system_scores.append(score)
        
        if all_system_scores:
            system_overall = sum(all_system_scores) / len(all_system_scores)
            system_grade = get_score_grade(system_overall)
            print(f"  🎯 {system}系统总评分: {system_overall:.3f} {system_grade}")
        else:
            print(f"  🎯 {system}系统总评分: ❌ 无有效评分")
        
        print()
    
    # 评价器对比
    print("📊 评价器对比")
    print("-" * 40)
    
    for evaluator in evaluators:
        evaluator_all_scores = []
        
        for system in rag_systems:
            for col in df.columns:
                if col.startswith(f"{system}_{evaluator}_"):
                    scores = df[col].tolist()
                    valid_scores = [s for s in scores if s is not None and pd.notna(s)]
                    evaluator_all_scores.extend(valid_scores)
        
        if evaluator_all_scores:
            avg_score = sum(evaluator_all_scores) / len(evaluator_all_scores)
            grade = get_score_grade(avg_score)
            print(f"  {evaluator}: {avg_score:.3f} {grade} (基于{len(evaluator_all_scores)}个评分)")
        else:
            print(f"  {evaluator}: ❌ 无有效评分")
    
    print()
    print("📋 评分说明:")
    print("  🏆 优秀 (0.9+)  🥇 良好 (0.8+)  🥈 中等 (0.7+)")
    print("  🥉 及格 (0.6+)  ❌ 需改进 (<0.6)")

def main():
    """主函数"""
    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
    else:
        csv_file = "results/multi_evaluation_results.csv"
    
    view_scores(csv_file)

if __name__ == "__main__":
    main()
