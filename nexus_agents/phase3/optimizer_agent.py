"""
OptimizerAgent - Analyzes evolution history and generates recommendations
"""
import json
import os
from datetime import datetime

class OptimizerAgent:
    def __init__(self, project_root="."):
        self.project_root = project_root
        self.metrics_file = os.path.join(project_root, "metrics.json")
        self.history = []

    def analyze_phi_trend(self):
        """Analyze φ trend from history"""
        try:
            with open(self.metrics_file, 'r') as f:
                metrics = json.load(f)
            history = metrics.get("history", [])
            if len(history) < 2:
                return {"trend": "INSUFFICIENT_DATA", "delta": 0}

            recent = history[-5:] if len(history) >= 5 else history
            deltas = [recent[i+1].get("phi",0) - recent[i].get("phi",0) for i in range(len(recent)-1)]
            avg_delta = sum(deltas) / len(deltas) if deltas else 0

            if avg_delta > 0.07:
                trend = "STRONG_GROWTH"
            elif avg_delta > 0.03:
                trend = "GROWTH"
            elif avg_delta > 0:
                trend = "WEAK_GROWTH"
            elif avg_delta == 0:
                trend = "STAGNATION"
            else:
                trend = "DECLINE"

            return {"trend": trend, "avg_delta": round(avg_delta, 4)}
        except:
            return {"trend": "ERROR", "delta": 0}

    def identify_successful_patterns(self):
        """Identify patterns that led to improvements"""
        patterns = []
        try:
            with open(self.metrics_file, 'r') as f:
                metrics = json.load(f)
            details = metrics.get("details", {})
            if details.get("completed_tasks", 0) > 0:
                patterns.append("fix-задачи эффективнее")
        except:
            pass
        return patterns

    def generate_recommendations(self):
        """Generate improvement recommendations"""
        trend = self.analyze_phi_trend()
        recommendations = []

        if trend["trend"] in ["STRONG_GROWTH", "GROWTH"]:
            recommendations.append({
                "agent": "AnalyzerAgent",
                "priority": "HIGH",
                "recommendation": "Продолжить текущую стратегию",
                "implementation": "Стратегия работает эффективно"
            })

        recommendations.append({
            "agent": "AnalyzerAgent", 
            "priority": "HIGH",
            "recommendation": "Добавить performance checks",
            "implementation": "Расширить анализ на memory leaks, CPU usage"
        })

        recommendations.append({
            "agent": "TesterAgent",
            "priority": "MEDIUM", 
            "recommendation": "Расширить регрессионные тесты",
            "implementation": "Добавить coverage метрики"
        })

        return recommendations

    def generate_optimization_report(self):
        """Generate full optimization report"""
        print("\n📊 OptimizerAgent запущен")
        print("-" * 70)

        trend = self.analyze_phi_trend()
        print(f"  📈 Тренд: {trend['trend']} (Δ={trend.get('avg_delta', 0)})")

        patterns = self.identify_successful_patterns()
        for p in patterns:
            print(f"  🎯 Паттерн: {p}")

        recommendations = self.generate_recommendations()
        print(f"  💡 Рекомендаций: {len(recommendations)}")
        for r in recommendations:
            print(f"    [{r['priority']}] {r['recommendation']}")

        return {
            "trend": trend,
            "patterns": patterns,
            "recommendations": recommendations,
            "timestamp": datetime.now().isoformat()
        }

if __name__ == "__main__":
    optimizer = OptimizerAgent()
    result = optimizer.generate_optimization_report()
    print(json.dumps(result, indent=2))

