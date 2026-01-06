#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
        self.api_base = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json",
            "Content-Type": "application/json"
        }

    def get_phi_from_metrics(self) -> float:
        """Получает φ-метрику из metrics.json"""
        try:
            if os.path.exists('metrics.json'):
                with open('metrics.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    phi = data.get('phi', 0.18)
                    if isinstance(phi, str):
                        phi = float(phi.replace(',', '.'))
                    return max(0.1, min(0.9, float(phi)))
        except Exception as e:
            self.log(f"⚠️ Error reading metrics: {e}")
        return 0.18

    def analyze(self) -> Optional[Dict]:
        """Анализирует текущее состояние φ и определяет нужны ли улучшения"""
        phi = self.get_phi_from_metrics()

        self.log(f"Agent-{self.agent_id} analyzing φ={phi:.2f}")

        analysis = {
            'agent_id': self.agent_id,
            'phi': phi,
            'timestamp': datetime.utcnow().isoformat(),
            'issues_found': [],
            'status': 'ok'
        }

        # Определяем нужны ли улучшения
        if phi < 0.15:
            analysis['status'] = 'critical'
            analysis['issues_found'].append({
                'title': 'Critical: φ below threshold',
                'priority': 'high',
                'label': 'critical'
            })
        elif phi > 0.65:
            analysis['status'] = 'warning'
            analysis['issues_found'].append({
                'title': 'Warning: φ instability detected',
                'priority': 'medium',
                'label': 'stability'
            })

        return analysis

    def create_issue(self, analysis: Dict) -> bool:
        """Создает Issue на GitHub для найденных проблем"""
        if not analysis['issues_found']:
            return True

        try:
            for issue_data in analysis['issues_found']:
                url = f"{self.api_base}/repos/{self.repo}/issues"
                payload = {
                    "title": issue_data['title'],
                    "body": f"""Agent-{self.agent_id} Analysis Report
- φ-metric: {analysis['phi']:.2f}
- Priority: {issue_data['priority']}
- Timestamp: {analysis['timestamp']}
- Status: {analysis['status']}
""",
                    "labels": ["auto-fix", issue_data['label'], "phase-3"]
                }

                response = requests.post(url, headers=self.headers, json=payload, timeout=10)
                if response.status_code == 201:
                    self.log(f"✅ Issue created: {issue_data['title']}")
                else:
                    self.log(f"⚠️ Failed to create issue: {response.status_code}")

        except Exception as e:
            self.log(f"❌ Error creating issue: {e}")
            return False

        return True

    def log(self, message: str):
        """Логирует сообщение с timestamp"""
        ts = datetime.utcnow().isoformat()
        print(f"[{ts}] {message}")


class AnalyzerPool:
    """Координирует несколько analyzer agents"""

    def __init__(self, num_agents: int = 8):
        self.num_agents = num_agents
        self.agents = [AnalyzerAgent(i) for i in range(num_agents)]

    def run_analysis(self):
        """Запускает анализ с несколькими agents параллельно"""
        print(f"🧬 Starting {self.num_agents} Analyzer Agents...")

        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.num_agents) as executor:
            futures = {
                executor.submit(agent.analyze): agent 
                for agent in self.agents
            }

            for future in concurrent.futures.as_completed(futures):
                try:
                    result = future.result()
                    agent = futures[future]
                    agent.create_issue(result)
                    results.append(result)
                except Exception as e:
                    print(f"❌ Agent error: {e}")

        print(f"✅ Analysis complete: {len(results)} agents finished")

        return results


def main():
    """Точка входа в программу"""
    try:
        num_agents = int(os.getenv('NUM_AGENTS', '8'))
    except ValueError:
        num_agents = 8

    pool = AnalyzerPool(num_agents=num_agents)
    results = pool.run_analysis()

    print(f"\n📊 Summary: Analyzed by {len(results)} agents")
    print(f"✅ All analyses completed successfully")


if __name__ == '__main__':
    main()
