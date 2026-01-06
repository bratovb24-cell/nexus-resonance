#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NEXUS Analyzer Agents - Phase 3
Self-evolving φ-metric analysis system
"""

import os
import sys
import json
from datetime import datetime

def safe_log(msg):
    """Safe logging with timestamp"""
    ts = datetime.utcnow().isoformat()
    print(f"[{ts}] {msg}")
    sys.stdout.flush()

def get_phi():
    """Get φ from metrics.json safely"""
    try:
        if os.path.exists('metrics.json'):
            with open('metrics.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                phi = data.get('phi', 0.18)
                if isinstance(phi, str):
                    phi = float(phi.replace(',', '.'))
                return max(0.1, min(0.9, float(phi)))
    except Exception as e:
        safe_log(f"⚠️  Error reading metrics: {e}")
    return 0.18

def run_analysis():
    """Main analysis function"""
    safe_log("🧬 NEXUS Analyzer Agents starting...")
    safe_log("=" * 70)

    phi = get_phi()
    safe_log(f"Current φ: {phi:.2f}")

    # Check if analysis is needed
    if phi < 0.15:
        safe_log("⚠️  CRITICAL: φ below threshold")
    elif phi > 0.65:
        safe_log("⚠️  WARNING: φ instability detected")
    else:
        safe_log("✅ φ metric stable")

    safe_log("=" * 70)
    safe_log("✅ Analysis completed successfully")

    return 0

if __name__ == '__main__':
    try:
        exit_code = run_analysis()
        sys.exit(exit_code)
    except Exception as e:
        safe_log(f"❌ FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
