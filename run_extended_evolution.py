#!/usr/bin/env python3
"""
NEXUS Phase 3 Extended - Main Entry Point
Run: python run_extended_evolution.py
"""
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from nexus_agents.phase3.extended_evolution_loop import ExtendedEvolutionLoop

def main():
    print("\n" + "="*70)
    print("🚀 NEXUS PHASE 3 EXTENDED - EVOLUTION SYSTEM")
    print("="*70)

    loop = ExtendedEvolutionLoop(".")
    results = loop.run_extended_continuous(max_cycles=5)

    print("\n✅ ЭВОЛЮЦИЯ ЗАВЕРШЕНА!")
    print(f"   Циклов: {len(results)}")
    print(f"   Финальный φ: {results[-1]['phi_after'] if results else 'N/A'}")

    return results

if __name__ == "__main__":
    main()

