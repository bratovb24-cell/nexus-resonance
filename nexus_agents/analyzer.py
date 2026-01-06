#!/usr/bin/env python3
"""
NEXUS Analyzer Agents - Phase 3
Self-evolving φ-metric analysis system
"""

import os
import json
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import statistics
import concurrent.futures

class AnalyzerAgent:
    """Анализирует φ-метрику и создает Issues для улучшения"""

    def __init__(self, agent_id: int):
        self.agent_id = agent_id
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.repo = "bratovb24-cell/nexus-resonance"
        self.vps_api = "http://176.123.169.38:5000/vps"
        self.vps_key = "claude2025"
        self.headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }

    def get_phi_from_vps(self) -> Optional[float]:
        """Получает текущую φ-метрику из VPS"""
        try:
            response = requests.post(
                self.vps_api,
                json={"key": self.vps_key, "cmd": "cat /opt/bridge/io/ai_context.json"},
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                context = json.loads(data.get('out', '{}'))
                # Извлекаем φ из контекста
                agents = context.get('agents', [])
                if agents:
                    phi_values = [a.get('phi', 0) for a in agents if 'phi' in a]
                    return max(phi_values) if phi_values else 0.18
            return 0.18
        except Exception as e:
            print(f"⚠️ Agent-{self.agent_id}: VPS error: {e}")
            return 0.18

    def get_phi_history(self, hours: int = 1) -> List[Dict]:
        """Получает историю φ-метрики"""
        # В реальности это из базы данных или artifacts
        current_phi = self.get_phi_from_vps()
        history = []
        for i in range(hours * 6):  # каждые 10 минут
            variation = 0.02 * (1 if i % 2 == 0 else -1)
            history.append({
                "timestamp": datetime.now() - timedelta(minutes=i*10),
                "phi": current_phi + variation
            })
        return history

    def analyze_trend(self) -> Dict:
        """Анализирует тренд φ"""
        history = self.get_phi_history(hours=1)

        if not history:
            return {"trend": "unknown", "severity": "low"}

        values = [h['phi'] for h in history]
        mean_val = statistics.mean(values)

        # Вычисляем тренд
        trend = values[0] - values[-1]  # последнее vs первое

        if trend < -0.1:
            severity = "high" if trend < -0.2 else "medium"
            return {
                "trend": "declining",
                "severity": severity,
                "rate": trend,
                "current": values[0],
                "previous": values[-1],
                "mean": mean_val
            }
        elif trend > 0.1:
            return {
                "trend": "improving",
                "severity": "low",
                "rate": trend,
                "current": values[0],
                "mean": mean_val
            }
        else:
            return {
                "trend": "stable",
                "severity": "low",
                "rate": trend,
                "current": values[0],
                "mean": mean_val
            }

    def detect_problem(self, trend: Dict) -> Dict:
        """Определяет тип проблемы на основе тренда"""
        problems = {
            "performance": {
                "type": "performance",
                "description": "System performance degradation detected",
                "severity": "medium",
                "solution": "Optimize critical execution paths and reduce latency"
            },
            "memory_leak": {
                "type": "memory_leak",
                "description": "Potential memory leak detected",
                "severity": "high",
                "solution": "Check long-lived objects and cyclic references"
            },
            "race_condition": {
                "type": "race_condition",
                "description": "Possible race condition in concurrent operations",
                "severity": "high",
                "solution": "Add synchronization to critical sections"
            },
            "resource_limit": {
                "type": "resource_limit",
                "description": "System approaching resource limits",
                "severity": "medium",
                "solution": "Increase limits or optimize resource usage"
            }
        }

        # Выбираем проблему на основе severity
        if trend.get('severity') == 'high':
            return problems['memory_leak']
        elif trend.get('rate', 0) < -0.15:
            return problems['race_condition']
        else:
            return problems['performance']

    def create_github_issue(self, problem: Dict, trend: Dict) -> Optional[Dict]:
        """Создает GitHub Issue с рекомендацией"""

        title = f"🔴 φ-Resonance Alert: {problem['description']}"

        body = f"""## 🧬 Auto-Analysis Report

**Agent ID:** Analyzer-{self.agent_id}  
**Timestamp:** {datetime.now().isoformat()}  
**Trend:** {trend['trend'].upper()}  

---

### 📊 Current Status

| Metric | Value |
|--------|-------|
| φ current | {trend.get('current', 'N/A'):.4f} |
| φ mean | {trend.get('mean', 'N/A'):.4f} |
| Change rate | {trend.get('rate', 0):.4f} |
| Severity | **{trend['severity'].upper()}** |

---

### ❌ Detected Problem

**Type:** `{problem['type']}`  
**Description:** {problem['description']}  
**Severity:** {problem['severity'].upper()}  

---

### ✅ Recommended Solution

{problem['solution']}

---

### 🎯 Acceptance Criteria

- [ ] φ-metric improved by at least 5%
- [ ] All existing tests passing
- [ ] No breaking changes introduced
- [ ] Code quality maintained (CodeQL passing)

---

### 🤖 Agent Instructions

This issue is marked for **auto-fix** by Developer Agents.

Expected flow:
1. Developer Agent picks up this issue
2. Generates fix code using AI
3. Creates Pull Request
4. Tester Agent validates
5. Optimizer Agent merges if criteria met

---

*Auto-generated by NEXUS Analyzer Agent #{self.agent_id}*  
*Phase 3: Self-Evolving Agent Ecosystem*
"""

        url = f"https://api.github.com/repos/{self.repo}/issues"
        data = {
            "title": title,
            "body": body,
            "labels": ["auto-fix", "agent-generated", "φ-metric", "evolution"]
        }

        try:
            response = requests.post(url, headers=self.headers, json=data)
            if response.status_code == 201:
                issue = response.json()
                print(f"✅ Agent-{self.agent_id}: Created Issue #{issue['number']}")
                return issue
            else:
                print(f"❌ Agent-{self.agent_id}: Failed - {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Agent-{self.agent_id}: Error - {e}")
            return None

    def run(self) -> Dict:
        """Главный цикл анализатора"""
        print(f"\n🔍 Analyzer Agent #{self.agent_id} starting...")

        # Анализируем тренд
        trend = self.analyze_trend()
        print(f"   📊 Trend: {trend['trend']} (severity: {trend['severity']})")

        result = {
            "agent_id": self.agent_id,
            "trend": trend,
            "issue_created": False
        }

        # Если есть проблема - создаем issue
        if trend['trend'] == 'declining' and trend['severity'] in ['high', 'medium']:
            problem = self.detect_problem(trend)
            issue = self.create_github_issue(problem, trend)
            result['issue_created'] = issue is not None
            result['issue'] = issue
        else:
            print(f"   ✅ Agent-{self.agent_id}: System healthy, no action needed")

        return result


def run_parallel_analyzers(num_agents: int = 8):
    """Запускает несколько анализаторов параллельно"""
    print("=" * 60)
    print("🧬 NEXUS Phase 3: Analyzer Agents Starting...")
    print("=" * 60)

    results = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_agents) as executor:
        futures = []

        for i in range(1, num_agents + 1):
            agent = AnalyzerAgent(agent_id=i)
            future = executor.submit(agent.run)
            futures.append(future)

        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                print(f"❌ Agent failed: {e}")

    # Summary
    print("\n" + "=" * 60)
    print("📊 ANALYSIS SUMMARY")
    print("=" * 60)

    issues_created = sum(1 for r in results if r.get('issue_created'))
    print(f"Total agents: {len(results)}")
    print(f"Issues created: {issues_created}")

    return results


if __name__ == "__main__":
    run_parallel_analyzers(num_agents=8)
