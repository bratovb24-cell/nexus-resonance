#!/usr/bin/env python3
"""
NEXUS EvoAgentX Core - Self-Evolving Agent Framework
Inspired by EvoAgentX architecture for autonomous code evolution
"""

import os
import json
import requests
import base64
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from abc import ABC, abstractmethod

# ═══════════════════════════════════════════════════════════════
# CORE: Agent Memory & State Management
# ═══════════════════════════════════════════════════════════════

@dataclass
class AgentMemory:
    """Persistent agent memory"""
    agent_id: str
    observations: List[Dict] = field(default_factory=list)
    actions: List[Dict] = field(default_factory=list)
    phi_history: List[float] = field(default_factory=list)

    def observe(self, data: Dict):
        self.observations.append({
            "timestamp": datetime.now().isoformat(),
            "data": data
        })
        if len(self.observations) > 100:
            self.observations = self.observations[-100:]

    def act(self, action: Dict):
        self.actions.append({
            "timestamp": datetime.now().isoformat(),
            "action": action
        })

    def get_recent_phi(self, n: int = 10) -> List[float]:
        return self.phi_history[-n:]


# ═══════════════════════════════════════════════════════════════
# CORE: Base Agent Class
# ═══════════════════════════════════════════════════════════════

class EvoAgent(ABC):
    """Base class for all evolution agents"""

    def __init__(self, agent_id: str, role: str):
        self.agent_id = agent_id
        self.role = role
        self.memory = AgentMemory(agent_id=agent_id)
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.repo = "bratovb24-cell/nexus-resonance"
        self.headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }

    @abstractmethod
    def perceive(self) -> Dict:
        pass

    @abstractmethod
    def think(self, perception: Dict) -> Dict:
        pass

    @abstractmethod
    def act(self, decision: Dict) -> Dict:
        pass

    def run_cycle(self) -> Dict:
        print(f"\n[{self.role}] Agent {self.agent_id} starting cycle...")

        perception = self.perceive()
        self.memory.observe(perception)
        print(f"  Perceived: {list(perception.keys())}")

        decision = self.think(perception)
        print(f"  Decision: {decision.get('action', 'none')}")

        result = self.act(decision)
        self.memory.act({"decision": decision, "result": result})
        print(f"  Result: {result.get('status', 'unknown')}")

        return {
            "agent_id": self.agent_id,
            "role": self.role,
            "perception": perception,
            "decision": decision,
            "result": result
        }


# ═══════════════════════════════════════════════════════════════
# ANALYZER AGENT
# ═══════════════════════════════════════════════════════════════

class AnalyzerAgent(EvoAgent):
    """Analyzes phi-metric and finds problems"""

    def __init__(self, agent_id: str = "analyzer-1"):
        super().__init__(agent_id, "Analyzer")
        self.vps_api = "http://176.123.169.38:5000/vps"
        self.vps_key = "claude2025"

    def perceive(self) -> Dict:
        perception = {
            "phi_current": 0.18,
            "phi_threshold": 0.75,
            "system_status": "stable",
            "issues_open": 0
        }

        try:
            response = requests.post(
                self.vps_api,
                json={"key": self.vps_key, "cmd": "cat /opt/bridge/io/ai_context.json"},
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                context = json.loads(data.get("out", "{}"))
                agents = context.get("agents", [])
                if agents:
                    phi_values = [a.get("phi", 0.18) for a in agents if "phi" in a]
                    perception["phi_current"] = max(phi_values) if phi_values else 0.18
        except Exception as e:
            print(f"  VPS connection: {e}")

        try:
            url = f"https://api.github.com/repos/{self.repo}/issues?state=open"
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                perception["issues_open"] = len(response.json())
        except:
            pass

        self.memory.phi_history.append(perception["phi_current"])
        return perception

    def think(self, perception: Dict) -> Dict:
        problems = []
        phi = perception["phi_current"]

        if phi > 0.5:
            problems.append({
                "type": "high_phi_warning",
                "severity": "medium",
                "description": f"Phi approaching threshold: {phi:.3f}"
            })

        if not problems:
            problems.append({
                "type": "optimization_opportunity",
                "severity": "low",
                "description": "System stable, monitoring"
            })

        return {
            "action": "report" if problems else "monitor",
            "problems": problems,
            "phi_current": phi
        }

    def act(self, decision: Dict) -> Dict:
        print(f"  Phi: {decision['phi_current']:.4f}")
        print(f"  Problems found: {len(decision['problems'])}")

        for p in decision["problems"]:
            print(f"    - [{p['severity']}] {p['type']}: {p['description']}")

        return {"status": "analyzed", "problems_count": len(decision["problems"])}


# ═══════════════════════════════════════════════════════════════
# DEVELOPER AGENT
# ═══════════════════════════════════════════════════════════════

class DeveloperAgent(EvoAgent):
    """Creates fixes for problems"""

    def __init__(self, agent_id: str = "developer-1"):
        super().__init__(agent_id, "Developer")

    def perceive(self) -> Dict:
        perception = {"pending_issues": [], "open_prs": 0}

        try:
            url = f"https://api.github.com/repos/{self.repo}/issues"
            params = {"labels": "auto-fix", "state": "open"}
            response = requests.get(url, headers=self.headers, params=params)
            if response.status_code == 200:
                perception["pending_issues"] = response.json()
        except:
            pass

        return perception

    def think(self, perception: Dict) -> Dict:
        issues = perception["pending_issues"]

        if not issues:
            return {"action": "idle", "reason": "no tasks"}

        return {
            "action": "ready",
            "issues_count": len(issues)
        }

    def act(self, decision: Dict) -> Dict:
        if decision["action"] == "idle":
            print("  No auto-fix issues to process")
            return {"status": "idle"}

        print(f"  Found {decision['issues_count']} issues ready for auto-fix")
        return {"status": "ready", "issues": decision["issues_count"]}


# ═══════════════════════════════════════════════════════════════
# EVOLUTION PIPELINE
# ═══════════════════════════════════════════════════════════════

class EvolutionPipeline:
    """Orchestrates the evolution cycle"""

    def __init__(self):
        self.analyzer = AnalyzerAgent()
        self.developer = DeveloperAgent()
        self.cycle_count = 0

    def run_evolution_cycle(self) -> Dict:
        self.cycle_count += 1
        print(f"\n{'='*60}")
        print(f"EVOLUTION CYCLE #{self.cycle_count}")
        print(f"{'='*60}")

        results = {
            "cycle": self.cycle_count,
            "timestamp": datetime.now().isoformat(),
            "stages": {}
        }

        # Stage 1: Analysis
        print("\n[STAGE 1] ANALYSIS")
        print("-" * 40)
        analyzer_result = self.analyzer.run_cycle()
        results["stages"]["analyzer"] = analyzer_result

        # Stage 2: Development
        print("\n[STAGE 2] DEVELOPMENT")
        print("-" * 40)
        developer_result = self.developer.run_cycle()
        results["stages"]["developer"] = developer_result

        # Summary
        print(f"\n{'='*60}")
        print("CYCLE SUMMARY")
        print(f"{'='*60}")
        phi = analyzer_result["perception"].get("phi_current", "N/A")
        print(f"  Phi current: {phi}")
        print(f"  Problems: {analyzer_result['result'].get('problems_count', 0)}")
        print(f"  Status: OK")

        return results


def main():
    """Run evolution cycle"""
    print("NEXUS EvoAgentX Core v3.1")
    print("=" * 60)

    pipeline = EvolutionPipeline()
    result = pipeline.run_evolution_cycle()

    print(f"\nEvolution cycle completed successfully!")
    return result


if __name__ == "__main__":
    main()
