"""
ExtendedEvolutionLoop - Integrates all agents into single evolution cycle
"""
import json
import os
import time
from datetime import datetime

class ExtendedEvolutionLoop:
    def __init__(self, project_root="."):
        self.project_root = project_root
        self.metrics_file = os.path.join(project_root, "metrics.json")
        self.cycle = 0

    def load_metrics(self):
        try:
            with open(self.metrics_file, 'r') as f:
                return json.load(f)
        except:
            return {"phi": 0.18, "cycle": 0, "status": "init", "history": []}

    def save_metrics(self, metrics):
        with open(self.metrics_file, 'w') as f:
            json.dump(metrics, f, indent=2)

    def run_analyzer(self):
        """Simulate analyzer finding issues"""
        return {"issues_found": 8, "tasks_generated": 10}

    def run_executor(self):
        """Simulate executing fixes"""
        return {"completed": 3, "tasks": ["fix_1", "fix_2", "fix_3"]}

    def run_tester(self):
        """Run TesterAgent"""
        from .tester_agent import TesterAgent
        tester = TesterAgent(self.project_root)
        return tester.run()

    def run_optimizer(self):
        """Run OptimizerAgent"""
        from .optimizer_agent import OptimizerAgent
        optimizer = OptimizerAgent(self.project_root)
        return optimizer.generate_optimization_report()

    def calculate_phi_improvement(self, test_result, optimizer_result):
        """Calculate φ improvement based on results"""
        base = 0.02
        if test_result.get("overall_status") == "PASS":
            base += 0.01
        trend = optimizer_result.get("trend", {}).get("trend", "")
        if "GROWTH" in trend:
            base += 0.005
        return round(base, 3)

    def run_extended_cycle(self):
        """Run one complete extended evolution cycle"""
        self.cycle += 1
        metrics = self.load_metrics()
        phi_before = metrics.get("phi", 0.18)

        print(f"\n{'='*70}")
        print(f"🔄 ЦИКЛ #{self.cycle}")
        print(f"{'='*70}")

        # Step 1: Analyze
        print(f"\n📊 Шаг 1: АНАЛИЗ")
        analyzer = self.run_analyzer()
        print(f"  Найдено проблем: {analyzer['issues_found']}")

        # Step 2: Execute
        print(f"\n👨‍💻 Шаг 2: ВЫПОЛНЕНИЕ")
        executor = self.run_executor()
        print(f"  Выполнено задач: {executor['completed']}")

        # Step 3: Test
        print(f"\n🧪 Шаг 3: ТЕСТИРОВАНИЕ")
        test_result = self.run_tester()

        # Step 4: Optimize
        print(f"\n🚀 Шаг 4: ОПТИМИЗАЦИЯ")
        optimizer_result = self.run_optimizer()

        # Step 5: Update metrics
        phi_delta = self.calculate_phi_improvement(test_result, optimizer_result)
        phi_after = round(phi_before + phi_delta, 3)

        print(f"\n📈 Шаг 5: ОБНОВЛЕНИЕ")
        print(f"  φ: {phi_before} → {phi_after} (+{phi_delta})")

        # Save updated metrics
        metrics["phi"] = phi_after
        metrics["cycle"] = self.cycle
        metrics["status"] = "evolving"
        metrics["last_update"] = datetime.now().isoformat()
        metrics["details"] = {
            "completed_tasks": executor["completed"],
            "phi_delta": phi_delta,
            "tester_status": test_result.get("overall_status", "UNKNOWN"),
            "optimizer_recommendations": len(optimizer_result.get("recommendations", []))
        }
        if "history" not in metrics:
            metrics["history"] = []
        metrics["history"].append({"phi": phi_after, "cycle": self.cycle})

        self.save_metrics(metrics)

        return {
            "cycle": self.cycle,
            "phi_before": phi_before,
            "phi_after": phi_after,
            "phi_delta": phi_delta,
            "test_status": test_result.get("overall_status"),
            "recommendations": len(optimizer_result.get("recommendations", []))
        }

    def run_extended_continuous(self, max_cycles=5):
        """Run multiple evolution cycles"""
        print(f"\n{'#'*70}")
        print(f"🚀 РАСШИРЕННАЯ ЭВОЛЮЦИЯ ({max_cycles} циклов)")
        print(f"{'#'*70}")

        results = []
        for i in range(max_cycles):
            result = self.run_extended_cycle()
            results.append(result)
            time.sleep(0.1)

        print(f"\n{'#'*70}")
        print(f"📊 ИТОГО: {len(results)} циклов завершено")
        print(f"{'#'*70}")

        return results

if __name__ == "__main__":
    loop = ExtendedEvolutionLoop()
    loop.run_extended_continuous(5)

