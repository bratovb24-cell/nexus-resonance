#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
from datetime import datetime

# Fix encoding for Windows/Linux/Mac compatibility
if sys.version_info >= (3, 7):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class EvolutionMetrics:
    """Safe metrics handler with fallback values"""

    def __init__(self, filepath='metrics.json'):
        self.filepath = filepath
        self.data = self._load_safe()

    def _load_safe(self):
        """Load metrics with error handling"""
        default = {
            'timestamp': datetime.utcnow().isoformat(),
            'phi': 0.18,
            'status': 'initialized',
            'phase': 3,
            'cycles': 0,
            'version': '4.0'
        }

        try:
            if os.path.exists(self.filepath):
                with open(self.filepath, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    if isinstance(loaded.get('phi'), (int, float)):
                        return loaded
        except Exception as e:
            print(f"⚠️  Load error: {e}, using defaults")

        return default

    def save(self):
        """Save metrics safely"""
        try:
            self.data['timestamp'] = datetime.utcnow().isoformat()
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"❌ Save error: {e}")
            return False

    def get_phi(self):
        """Get φ metric safely"""
        phi = self.data.get('phi', 0.18)

        if isinstance(phi, str):
            try:
                phi = float(phi.replace(',', '.'))
            except ValueError:
                phi = 0.18

        return max(0.1, min(0.9, float(phi)))

    def set_phi(self, value):
        """Set φ metric safely"""
        try:
            phi = float(value)
            phi = max(0.1, min(0.9, phi))
            self.data['phi'] = phi
            return phi
        except (ValueError, TypeError):
            print(f"❌ Invalid φ value: {value}")
            return self.get_phi()

    def increment_cycles(self):
        """Increment evolution cycle counter"""
        self.data['cycles'] = self.data.get('cycles', 0) + 1
        self.data['status'] = 'running'


class EvolutionEngine:
    """Standalone evolution engine"""

    def __init__(self):
        self.metrics = EvolutionMetrics('metrics.json')
        self.current_phi = self.metrics.get_phi()

    def log(self, message):
        """Log with timestamp"""
        ts = datetime.utcnow().isoformat()
        print(f"[{ts}] {message}")

    def run_cycle(self):
        """Execute one evolution cycle"""
        self.log("="*70)
        self.log("🚀 NEXUS Evolution Pipeline v4 - Starting cycle")
        self.log("="*70)

        self.log(f"Current φ: {self.current_phi:.2f}")

        if self.current_phi < 0.1:
            self.log("⚠️  φ below minimum, resetting to 0.18")
            self.current_phi = 0.18
        elif self.current_phi > 0.8:
            self.log("⚠️  φ above threshold, high instability!")

        old_phi = self.current_phi

        if self.current_phi < 0.5:
            delta = 0.01
            self.current_phi += delta
            self.log(f"📈 Improvement phase: +{delta}")
        else:
            delta = -0.005
            self.current_phi += delta
            self.log(f"📉 Optimization phase: {delta}")

        self.current_phi = max(0.1, min(0.9, self.current_phi))

        self.log(f"Evolution: {old_phi:.2f} → {self.current_phi:.2f}")

        self.metrics.set_phi(self.current_phi)
        self.metrics.increment_cycles()

        if self.metrics.save():
            self.log("✅ Metrics saved successfully")
        else:
            self.log("❌ Failed to save metrics")

        self.log("="*70)
        self.log("✅ Cycle completed")
        self.log("="*70)

        return True


def main():
    try:
        engine = EvolutionEngine()
        success = engine.run_cycle()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Fatal error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
