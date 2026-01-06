#!/usr/bin/env python3
"""
ResonantAnalyzerAgent - AI Resonator Architecture
Multiple internal perspectives for enhanced analysis quality
"""

import os
import json
import subprocess
import ast
import re
from datetime import datetime
from typing import Dict, List, Any
from dataclasses import dataclass
from enum import Enum

class Perspective(Enum):
    SYNTAX = "syntax"
    SEMANTIC = "semantic"
    SECURITY = "security"
    PERFORMANCE = "performance"
    ARCHITECTURE = "architecture"
    EVOLUTION = "evolution"

@dataclass
class ResonanceSignal:
    perspective: Perspective
    confidence: float
    findings: List[Dict[str, Any]]
    phi_impact: float

@dataclass
class ResonanceResult:
    amplified_signals: List[ResonanceSignal]
    consensus_issues: List[Dict[str, Any]]
    total_phi_delta: float
    resonance_strength: float

class ResonatorTools:
    def __init__(self, project_root="."):
        self.project_root = project_root

    def find_python_files(self, max_files=50):
        files = []
        for root, dirs, filenames in os.walk(self.project_root):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
            for f in filenames:
                if f.endswith('.py'):
                    files.append(os.path.join(root, f))
                    if len(files) >= max_files:
                        return files
        return files

    def git_diff(self, base="HEAD~1"):
        try:
            result = subprocess.run(['git', 'diff', base, '--name-only'],
                capture_output=True, text=True, cwd=self.project_root)
            return result.stdout
        except:
            return ""

    def git_log(self, n=10):
        try:
            result = subprocess.run(['git', 'log', f'-{n}', '--oneline'],
                capture_output=True, text=True, cwd=self.project_root)
            return result.stdout
        except:
            return ""

    def shell_exec(self, cmd, timeout=30):
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, 
                text=True, cwd=self.project_root, timeout=timeout)
            return result.stdout + result.stderr
        except:
            return ""

    def search_code(self, pattern):
        try:
            result = subprocess.run(['grep', '-rn', pattern, '--include=*.py', '.'],
                capture_output=True, text=True, cwd=self.project_root)
            matches = []
            for line in result.stdout.strip().split(chr(10)):
                if ':' in line:
                    parts = line.split(':', 2)
                    if len(parts) >= 3:
                        matches.append({"file": parts[0], "line": parts[1], "content": parts[2]})
            return matches[:50]
        except:
            return []

class ResonantAnalyzerAgent:
    def __init__(self, project_root="."):
        self.project_root = project_root
        self.perspectives = list(Perspective)
        self.tools = ResonatorTools(project_root)

    def analyze_from_perspective(self, perspective, files):
        findings = []
        confidence = 0.8
        phi_impact = 0.02

        if perspective == Perspective.SYNTAX:
            for filepath in files:
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        ast.parse(f.read())
                except SyntaxError as e:
                    findings.append({"type": "syntax_error", "file": filepath, 
                        "line": e.lineno, "message": str(e), "severity": "HIGH"})
            confidence = 0.95 if not findings else 0.7

        elif perspective == Perspective.SEMANTIC:
            patterns = [
                (r'except:\s*pass', 'silent_exception', 'Silent exception'),
                (r'# TODO', 'todo_found', 'TODO comment'),
                (r'eval\s*\(', 'dangerous_eval', 'Using eval()'),
            ]
            for filepath in files:
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    for pattern, issue_type, desc in patterns:
                        if re.search(pattern, content):
                            findings.append({"type": issue_type, "file": filepath,
                                "message": desc, "severity": "MEDIUM"})
                except:
                    pass

        elif perspective == Perspective.SECURITY:
            patterns = [
                (r'password\s*=\s*["\'\x27]', 'hardcoded_password', 'Hardcoded password'),
                (r'api_key\s*=\s*["\'\x27]', 'hardcoded_key', 'Hardcoded API key'),
                (r'shell\s*=\s*True', 'shell_injection', 'Potential shell injection'),
            ]
            for filepath in files:
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    for pattern, issue_type, desc in patterns:
                        if re.search(pattern, content, re.IGNORECASE):
                            findings.append({"type": issue_type, "file": filepath,
                                "message": desc, "severity": "CRITICAL"})
                except:
                    pass
            confidence = 0.85
            phi_impact = 0.04

        elif perspective == Perspective.PERFORMANCE:
            for filepath in files:
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    if re.search(r'range\s*\(\s*len\s*\(', content):
                        findings.append({"type": "inefficient_loop", "file": filepath,
                            "message": "Inefficient range(len())", "severity": "LOW"})
                except:
                    pass
            confidence = 0.75

        elif perspective == Perspective.ARCHITECTURE:
            for filepath in files:
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        lines = len(f.readlines())
                    if lines > 500:
                        findings.append({"type": "large_file", "file": filepath,
                            "message": f"File too large ({lines} lines)", "severity": "MEDIUM"})
                except:
                    pass
            confidence = 0.7

        elif perspective == Perspective.EVOLUTION:
            has_tests = any('test' in f.lower() for f in files)
            if not has_tests:
                findings.append({"type": "missing_tests", "file": "project",
                    "message": "No tests found", "severity": "MEDIUM"})
            confidence = 0.6

        return ResonanceSignal(perspective=perspective, confidence=confidence,
            findings=findings, phi_impact=phi_impact if findings else phi_impact * 0.5)

    def resonate(self, signals):
        file_issues = {}
        for signal in signals:
            for finding in signal.findings:
                file_key = finding.get('file', 'unknown')
                if file_key not in file_issues:
                    file_issues[file_key] = []
                file_issues[file_key].append({
                    **finding,
                    'perspective': signal.perspective.value,
                    'confidence': signal.confidence
                })

        consensus_issues = []
        for file_key, issues in file_issues.items():
            issue_types = [i['type'] for i in issues]
            for issue in issues:
                score = issue['confidence']
                similar_count = sum(1 for t in issue_types if t == issue['type'])
                if similar_count > 1:
                    score *= (1 + 0.2 * similar_count)
                issue['resonance_score'] = min(score, 1.0)
                consensus_issues.append(issue)

        consensus_issues.sort(key=lambda x: x.get('resonance_score', 0), reverse=True)
        confidences = [s.confidence for s in signals]
        resonance_strength = sum(confidences) / len(confidences) if confidences else 0
        total_phi_delta = sum(s.phi_impact for s in signals) / len(signals) if signals else 0

        return ResonanceResult(amplified_signals=signals, consensus_issues=consensus_issues[:20],
            total_phi_delta=total_phi_delta, resonance_strength=resonance_strength)

    def run_full_analysis(self):
        print("")
        print("=" * 70)
        print("RESONANT ANALYZER - AI Resonator Architecture")
        print("=" * 70)

        files = self.tools.find_python_files()
        print(f"Files found: {len(files)}")

        print("Multi-perspective analysis:")
        signals = []
        for perspective in self.perspectives:
            signal = self.analyze_from_perspective(perspective, files)
            signals.append(signal)
            status = "OK" if signal.confidence > 0.7 else "WARN"
            print(f"  [{status}] {perspective.value}: conf={signal.confidence:.2f}, findings={len(signal.findings)}")

        print("Signal resonance...")
        result = self.resonate(signals)

        print(f"  Resonance strength: {result.resonance_strength:.2f}")
        print(f"  Consensus issues: {len(result.consensus_issues)}")
        print(f"  Phi delta potential: +{result.total_phi_delta:.3f}")

        if result.consensus_issues:
            print("TOP ISSUES:")
            for issue in result.consensus_issues[:5]:
                score = issue.get('resonance_score', 0)
                print(f"  [{issue.get('severity')}] {issue.get('type')}: {issue.get('message')} (score={score:.2f})")

        return {
            "files_analyzed": len(files),
            "perspectives_used": len(self.perspectives),
            "resonance_strength": result.resonance_strength,
            "consensus_issues": len(result.consensus_issues),
            "phi_delta": result.total_phi_delta,
            "top_issues": result.consensus_issues[:10],
            "timestamp": datetime.now().isoformat()
        }

if __name__ == "__main__":
    analyzer = ResonantAnalyzerAgent(".")
    result = analyzer.run_full_analysis()
    print("=" * 70)
    print(f"Analysis complete. Resonance: {result['resonance_strength']:.2f}")
