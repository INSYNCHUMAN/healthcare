# 🏥 healthcare
*Primary seed for HealthRevolution2025*

---
## 🌱 Vision
“Empower every system in healthcare to pulse with real-time coherence, resilience, and compassion.”

---
## 🎯 Purpose
This repository is the **nervous system** of our HealthRevolution2025 initiative. It now ships with
an executable core that demonstrates how we ingest vitals, normalize them, and run lightweight
diagnostics so the rest of the ecosystem can iterate.

---
## 📚 What’s Here
1. **`insync_codex.yaml`**
   - Trigger-word → module map with somatic cues
2. **`modules/`**
   - `data_ingest/normalizer.py` → pure function to normalize raw vitals without mutating inputs
   - `diagnostics/risk.py` → derives a cardio-risk score from normalized vitals
   - `rituals/check_in.md` → team practice to reconnect data work with embodied reality
3. **`docs/architecture.md`**
   - Overview of how ingest ↔ diagnostics ↔ rituals feedback loop works
4. **`tests/`**
   - Pytest suite that guards against regressions (e.g., accidental mutation of incoming data)

---
## ⚙️ Getting Started
1. **Clone & Install**
   ```bash
   git clone git@github.com:INSYNCHUMAN/healthcare.git
   cd healthcare
   python -m venv .venv && source .venv/bin/activate
   pip install -r <(python - <<'PY'
import tomllib, sys
with open('pyproject.toml', 'rb') as fh:
    cfg = tomllib.load(fh)
requires = cfg.get('project', {}).get('dependencies', []) or []
print('\n'.join(requires))
PY
   )
   ```
   *(The project currently has no runtime dependencies, so this just ensures Python ≥ 3.10.)*
2. **Run Tests**
   ```bash
   pytest
   ```

---
## 🧠 Architecture Notes
- **Normalizer bugfix**: the first iteration mutated the caller’s dictionary after normalizing
  vitals, which corrupted raw telemetry for downstream services. The current implementation
  clones the payload and validates metric bounds up front.
- **Cardio risk scoring**: a light-weight heuristic demonstrates how diagnostics can subscribe to
  normalized data.

---
## 🤝 Contributing
1. Write a failing test that captures the bug or behavior shift.
2. Implement the change in a small, well-named module.
3. Run `pytest` and ensure the suite passes.
4. Open a PR that references the somatic cue(s) you tended to.
