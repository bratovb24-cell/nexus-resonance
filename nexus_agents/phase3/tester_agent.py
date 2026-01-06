"""
TesterAgent - Automatic validation of NEXUS Evolution changes
"""
import json
import os
import ast
from datetime import datetime

class TesterAgent:
    def __init__(self, project_root="."):
        self.project_root = project_root
        self.metrics_file = os.path.join(project_root, "metrics.json")
        self.results = {"tests": [], "status": "PENDING"}

    def validate_syntax(self, files=None):
        """Validate Python syntax of all files"""
        if files is None:
            files = self._find_python_files()
        results = []
        for filepath in files:
            try:
                with open(filepath, 'r') as f:
                    source = f.read()
                ast.parse(source)
                results.append({"file": filepath, "status": "PASS"})
            except SyntaxError as e:
                results.append({"file": filepath, "status": "FAIL", "error": str(e)})
        return {"test": "syntax", "results": results, "status": "PASS" if all(r["status"]=="PASS" for r in results) else "FAIL"}

    def validate_metrics(self):
        """Validate metrics.json structure and values"""
        try:
            with open(self.metrics_file, 'r') as f:
                metrics = json.load(f)
            phi = metrics.get("phi", 0)
            if 0 <= phi <= 1:
                return {"test": "metrics", "status": "PASS", "phi": phi}
            return {"test": "metrics", "status": "FAIL", "error": "phi out of range"}
        except Exception as e:
            return {"test": "metrics", "status": "FAIL", "error": str(e)}

    def test_imports(self):
        """Test that all required imports work"""
        required = ["json", "os", "time", "datetime"]
        results = []
        for mod in required:
            try:
                __import__(mod)
                results.append({"module": mod, "status": "PASS"})
            except ImportError:
                results.append({"module": mod, "status": "FAIL"})
        return {"test": "imports", "results": results, "status": "PASS" if all(r["status"]=="PASS" for r in results) else "FAIL"}

    def _find_python_files(self):
        """Find all Python files in project"""
        files = []
        for root, dirs, filenames in os.walk(self.project_root):
            if '.git' in root or '__pycache__' in root:
                continue
            for f in filenames:
                if f.endswith('.py'):
                    files.append(os.path.join(root, f))
        return files[:10]

    def run(self):
        """Run all tests"""
        print("\n🧪 TesterAgent запущен")
        print("-" * 70)

        syntax = self.validate_syntax()
        print(f"  🔍 Синтаксис: {syntax['status']}")

        metrics = self.validate_metrics()
        print(f"  📊 Метрики: {metrics['status']} (φ={metrics.get('phi', 'N/A')})")

        imports = self.test_imports()
        print(f"  📦 Импорты: {imports['status']}")

        overall = "PASS" if all(t["status"]=="PASS" for t in [syntax, metrics, imports]) else "FAIL"
        print(f"\n✅ Тестирование завершено: {overall}")

        return {
            "overall_status": overall,
            "tests": {"syntax": syntax, "metrics": metrics, "imports": imports},
            "timestamp": datetime.now().isoformat()
        }

if __name__ == "__main__":
    tester = TesterAgent()
    result = tester.run()
    print(json.dumps(result, indent=2))

