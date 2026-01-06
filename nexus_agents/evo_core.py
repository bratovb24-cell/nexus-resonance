#!/usr/bin/env python3
"""
NEXUS EvoAgentX Core - Self-Evolving Agent Framework
Inspired by EvoAgentX architecture for autonomous code evolution
"""

import os
import json
import requests
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import concurrent.futures

# ═══════════════════════════════════════════════════════════════
# CORE: Agent Memory & State Management
# ═══════════════════════════════════════════════════════════════

@dataclass
class AgentMemory:
    """Персистентная память агента"""
    agent_id: str
    observations: List[Dict] = field(default_factory=list)
    actions: List[Dict] = field(default_factory=list)
    phi_history: List[float] = field(default_factory=list)

    def observe(self, data: Dict):
        """Записать наблюдение"""
        self.observations.append({
            "timestamp": datetime.now().isoformat(),
            "data": data
        })
        # Ограничиваем память
        if len(self.observations) > 100:
            self.observations = self.observations[-100:]

    def act(self, action: Dict):
        """Записать действие"""
        self.actions.append({
            "timestamp": datetime.now().isoformat(),
            "action": action
        })

    def get_recent_phi(self, n: int = 10) -> List[float]:
        """Получить последние значения φ"""
        return self.phi_history[-n:]

    def to_dict(self) -> Dict:
        return {
            "agent_id": self.agent_id,
            "observations_count": len(self.observations),
            "actions_count": len(self.actions),
            "phi_history": self.phi_history[-10:]
        }


# ═══════════════════════════════════════════════════════════════
# CORE: Base Agent Class (EvoAgentX-style)
# ═══════════════════════════════════════════════════════════════

class EvoAgent(ABC):
    """Базовый класс для всех эволюционных агентов"""

    def __init__(self, agent_id: str, role: str):
        self.agent_id = agent_id
        self.role = role
        self.memory = AgentMemory(agent_id=agent_id)
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.repo = "bratovb24-cell/nexus-resonance"
        self.headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }

    @abstractmethod
    def perceive(self) -> Dict:
        """Воспринять окружение"""
        pass

    @abstractmethod
    def think(self, perception: Dict) -> Dict:
        """Обработать восприятие и принять решение"""
        pass

    @abstractmethod
    def act(self, decision: Dict) -> Dict:
        """Выполнить действие"""
        pass

    def run_cycle(self) -> Dict:
        """Выполнить один цикл: perceive → think → act"""
        print(f"\n🔄 {self.role} Agent [{self.agent_id}] starting cycle...")

        # 1. Perceive
        perception = self.perceive()
        self.memory.observe(perception)
        print(f"   👁️ Perceived: {list(perception.keys())}")

        # 2. Think
        decision = self.think(perception)
        print(f"   🧠 Decision: {decision.get('action', 'none')}")

        # 3. Act
        result = self.act(decision)
        self.memory.act({"decision": decision, "result": result})
        print(f"   ⚡ Result: {result.get('status', 'unknown')}")

        return {
            "agent_id": self.agent_id,
            "role": self.role,
            "perception": perception,
            "decision": decision,
            "result": result
        }


# ═══════════════════════════════════════════════════════════════
# ANALYZER AGENT: Анализирует код и находит проблемы
# ═══════════════════════════════════════════════════════════════

class AnalyzerAgent(EvoAgent):
    """Анализирует код и генерирует список проблем для улучшения φ"""

    def __init__(self, agent_id: str = "analyzer-1"):
        super().__init__(agent_id, "Analyzer")
        self.vps_api = "http://176.123.169.38:5000/vps"
        self.vps_key = "claude2025"

    def perceive(self) -> Dict:
        """Получить текущее состояние системы"""
        perception = {
            "phi_current": 0.18,
            "phi_threshold": 0.75,
            "system_status": "stable",
            "code_files": [],
            "issues_open": 0
        }

        # Получаем φ из VPS
        try:
            response = requests.post(
                self.vps_api,
                json={"key": self.vps_key, "cmd": "cat /opt/bridge/io/ai_context.json"},
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                context = json.loads(data.get('out', '{}'))
                agents = context.get('agents', [])
                if agents:
                    phi_values = [a.get('phi', 0.18) for a in agents if 'phi' in a]
                    perception['phi_current'] = max(phi_values) if phi_values else 0.18
        except Exception as e:
            print(f"   ⚠️ VPS error: {e}")

        # Получаем открытые issues
        try:
            url = f"https://api.github.com/repos/{self.repo}/issues?state=open"
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                perception['issues_open'] = len(response.json())
        except:
            pass

        self.memory.phi_history.append(perception['phi_current'])
        return perception

    def think(self, perception: Dict) -> Dict:
        """Анализировать и найти проблемы"""
        problems = []

        phi = perception['phi_current']
        phi_history = self.memory.get_recent_phi()

        # Анализ трендов
        if len(phi_history) >= 2:
            trend = phi_history[-1] - phi_history[0]
            if trend < -0.05:
                problems.append({
                    "type": "performance_degradation",
                    "severity": "high",
                    "description": f"φ declining: {phi_history[0]:.3f} → {phi_history[-1]:.3f}",
                    "suggestion": "Add caching and optimize hot paths"
                })

        # Проверка порога
        if phi > 0.5:
            problems.append({
                "type": "high_phi_warning",
                "severity": "medium",
                "description": f"φ approaching threshold: {phi:.3f}",
                "suggestion": "Review recent changes for instability"
            })

        # Если нет проблем - предложить улучшения
        if not problems:
            problems.append({
                "type": "optimization_opportunity",
                "severity": "low",
                "description": "System stable, opportunity for optimization",
                "suggestion": "Add more monitoring metrics"
            })

        return {
            "action": "create_tasks" if problems else "monitor",
            "problems": problems,
            "phi_current": phi
        }

    def act(self, decision: Dict) -> Dict:
        """Создать задачи для Developer Agent"""
        if decision['action'] != 'create_tasks':
            return {"status": "monitoring", "tasks_created": 0}

        tasks_created = 0

        for problem in decision['problems']:
            if problem['severity'] in ['high', 'medium']:
                # Создаем Issue
                title = f"🔧 [{problem['severity'].upper()}] {problem['type']}: {problem['description'][:50]}"
                body = f"""## Problem Analysis

**Type:** `{problem['type']}`
**Severity:** {problem['severity'].upper()}
**Current φ:** {decision['phi_current']:.4f}

### Description
{problem['description']}

### Suggested Fix
{problem['suggestion']}

### For Developer Agent
- [ ] Implement suggested fix
- [ ] Verify φ improvement
- [ ] Create PR

---
*Generated by Analyzer Agent [{self.agent_id}]*
"""

                try:
                    url = f"https://api.github.com/repos/{self.repo}/issues"
                    response = requests.post(url, headers=self.headers, json={
                        "title": title,
                        "body": body,
                        "labels": ["auto-fix", "evo-agent", problem['severity']]
                    })
                    if response.status_code == 201:
                        tasks_created += 1
                        print(f"   📝 Created issue: {title[:40]}...")
                except Exception as e:
                    print(f"   ❌ Failed to create issue: {e}")

        return {"status": "tasks_created", "tasks_created": tasks_created}


# ═══════════════════════════════════════════════════════════════
# DEVELOPER AGENT: Пишет код для исправления проблем
# ═══════════════════════════════════════════════════════════════

class DeveloperAgent(EvoAgent):
    """Принимает задачи от Analyzer и пишет/изменяет код"""

    def __init__(self, agent_id: str = "developer-1"):
        super().__init__(agent_id, "Developer")
        self.fix_templates = self._load_fix_templates()

    def _load_fix_templates(self) -> Dict:
        """Загрузить шаблоны исправлений"""
        return {
            "performance_degradation": {
                "file": "nexus_agents/optimizations.py",
                "code": self._get_performance_fix()
            },
            "high_phi_warning": {
                "file": "nexus_agents/stabilizer.py", 
                "code": self._get_stabilizer_fix()
            },
            "optimization_opportunity": {
                "file": "nexus_agents/metrics.py",
                "code": self._get_metrics_fix()
            }
        }

    def _get_performance_fix(self) -> str:
        return Performance Optimizations - Auto-generated