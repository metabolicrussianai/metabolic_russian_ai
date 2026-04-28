#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════════════════════

  FSBio Metabolic AI — Phoenix Runtime Demo
  Public Demonstration Build  |  v9.0.1-enterprise
  Internal core: Phoenix v8.5.1 (proprietary, patent pending)

═══════════════════════════════════════════════════════════════════════════════

  WHAT THIS DEMO IS
  ─────────────────
  This file is an OBFUSCATED PUBLIC DEMONSTRATION of selected runtime
  signals from the Phoenix Metabolic AI engine. It ships with FSBio
  Lab as a reproducible artefact for partners, investors, and
  technical reviewers who want to observe the *shape* of the runtime
  without access to the internal architecture.

  WHAT THIS DEMO IS NOT
  ─────────────────────
  This is NOT the Phoenix engine. This is NOT a learning system. This
  is NOT a model that can be trained, fine-tuned, deployed, or used
  in production. This is a SIGNAL GENERATOR that emits the same
  external interfaces as the real engine, with all internal dynamics
  replaced by a deterministic SHA-256-derived stream.

  The deterministic generator is INTENTIONAL: it produces a stable,
  reproducible, opaque trace for demonstration, while protecting the
  proprietary biological dynamics of the real Homeostat, BCM-rule
  weight updates, three-factor STDP, Hill-kinetic gating, Dale
  polarity, ATP-budgeted metabolic lifecycle, and ~70 other internal
  subsystems.

  WHAT THE REAL PHOENIX RUNTIME ACTUALLY DOES
  ───────────────────────────────────────────
  In one sentence (per Lina Chernova's public statement, Apr 28 2026):

      "We dropped all ML primitives and mapped the whole
       neurophysiology in Python to model agent behaviour.
       No RLHF, no backprop, no loss function, weights
       are restructured on the fly."

  Concretely, the real engine:

    • Has NO loss function. NO gradient descent. NO backpropagation.
      NO RLHF. NO PPO. NO actor-critic. NO TD-error scalar reward.

    • Maintains a CONTINUOUS background process (Homeostat) that
      evolves a vector of internal states (virtual hormones) by
      Hill-kinetic ligand–receptor saturation (Hill 1910), Naka-
      Rushton response curves (Naka & Rushton 1966), and BCM
      synaptic plasticity (Bienenstock, Cooper & Munro 1982).

    • Updates weights ONLINE during operation through:
        – BCM rule with sliding threshold (homeostatic plasticity)
        – Three-factor STDP: ΔW = η · eligibility · DA_phasic
          (Izhikevich 2007; Schultz 1998 burst/dip dopamine)
        – Synaptic scaling, no L1/L2 (Turrigiano 2008)
        – RLS readout adaptation (no SGD anywhere in the path)

    • Modulates LLM generation hyperparameters (temperature,
      top-p, attention bias, sampling profile) BEFORE token
      generation, conditioned on the current hormonal vector.
      Same prompt, different internal state ⇒ qualitatively
      different output. This is architectural, not in the
      system prompt.

    • Prioritises memory by intensity of state-vector shift at
      the moment of encoding (BTSP one-shot consolidation,
      Bittner et al. 2017; sedimentation by salience, not by
      semantic similarity to a query).

    • Implements full neurobiological invariants: Dale's principle
      (excitatory/inhibitory polarity is fixed per neuron),
      refractory periods, axonal conduction delays, ATP budgets
      with metabolic lifecycle (apoptosis under low ATP,
      neurogenesis under high novelty), reflex arcs preceding
      cortical processing (Sherrington 1906), vagal tone,
      locus coeruleus norepinephrine, astrocyte fields,
      theta-gamma coupling, lateral inhibition, predictive
      coding columns, grid-cell modules, hierarchical predictive
      columns, sleep consolidation cycles.

  HOW TO READ THE DEMO OUTPUT
  ───────────────────────────
  The trace below shows the SHAPE of metrics the real engine
  emits per tick: hormonal vector, somatic state, drive vector,
  coherence, alive-fraction, ATP, vagal tone. The NUMBERS are
  SHA-256-derived noise. The INTERFACE is real.

  Partners under NDA receive the actual engine. Reviewers in
  academic context receive the Zenodo preprints (DOIs of
  2026-04-13 and 2026-04-20).

═══════════════════════════════════════════════════════════════════════════════
"""

from __future__ import annotations

import hashlib
import math
import struct
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple


# ═══════════════════════════════════════════════════════════════════════════════
#   DETERMINISM CORE
#
#   All numeric outputs are derived from a SHA-256 chain seeded by tick index.
#   This is a deliberate choice for the public demo: outputs are reproducible
#   for a given seed, opaque to the observer, and reveal NOTHING about the
#   internal Hill-kinetic / BCM / STDP dynamics of the real engine.
# ═══════════════════════════════════════════════════════════════════════════════


def _digest(*parts: bytes) -> bytes:
    """SHA-256 over concatenated parts."""
    h = hashlib.sha256()
    for p in parts:
        h.update(p)
    return h.digest()


def _u32(b: bytes, off: int = 0) -> float:
    """Extract u32 from digest, normalise to [0, 1)."""
    (u,) = struct.unpack_from(">I", b, off % (len(b) - 3))
    return u / 0xFFFFFFFF


def _smooth(prev: float, target: float, alpha: float = 0.18) -> float:
    """Continuous evolution between ticks (NOT the real engine's dynamics)."""
    return prev + alpha * (target - prev)


def _hill(val: float, K: float = 0.5, n: float = 4.0) -> float:
    """Hill-kinetic gate (real engine uses Hill 1910 ligand-receptor saturation;
    here used only for surface plausibility of the demo trace)."""
    v = max(0.0, val)
    return (v ** n) / (v ** n + K ** n + 1e-12)


def _naka_rushton(x: float, sigma: float = 0.5, n: float = 2.0,
                  rmax: float = 1.0) -> float:
    """Naka-Rushton response (Naka & Rushton 1966) — real engine uses this
    for ALL nonlinearities (sigmoid/tanh are banned by hard constraint HC-1).
    Here: trace flavour only."""
    v = max(0.0, x)
    return rmax * (v ** n) / (v ** n + sigma ** n + 1e-12)


def _ts() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")[:-4] + "Z"


# ═══════════════════════════════════════════════════════════════════════════════
#   OPAQUE STATE CONTAINER
#
#   The real engine has 80+ classes spanning rectoceptor kinetics, organ
#   embryos, coupling matrices, sedimentation layers, biochemical reactors,
#   osmotic reservoirs, liquid bridges, Dale polarity, axonal delays, ATP
#   budgets, intrinsic plasticity, Tsodyks-Markram STP, calcium messengers,
#   vagal tone, locus coeruleus, dendritic compartments, astrocytes, theta-
#   gamma oscillators, lateral inhibition, BCM rule, three-factor STDP,
#   metabolic lifecycle, predictive columns, grid cells, hierarchical
#   predictive columns, sleep consolidation, reflex arcs, observer module,
#   drive sedimentation, expression vector, prompt compiler, embedding
#   perception, Hamiltonian phase space, becoming field, private curvature,
#   seal decision, ~70 organs total.
#
#   None of that is here. Here: one opaque state that drifts deterministically.
# ═══════════════════════════════════════════════════════════════════════════════


@dataclass
class _OpaqueState:
    seed: bytes
    tick: int = 0
    # The REAL engine has 12 hormones. Here we expose 6 names for the trace,
    # with values derived from SHA-256, not from ligand-receptor dynamics.
    hormones: Dict[str, float] = field(default_factory=lambda: {
        "DA": 0.5, "OT": 0.5, "CORT": 0.3, "NE": 0.4, "5HT": 0.5, "GABA": 0.5,
    })
    # The REAL engine has 5 somatic sensations from interoceptive Gut.
    # Here: opaque drift.
    soma: Dict[str, float] = field(default_factory=lambda: {
        "warmth": 0.5, "tension": 0.3, "expansion": 0.5,
        "tingling": 0.2, "sedation": 0.4,
    })
    # The REAL engine has a drive vector with emergent love-attractor.
    # Here: noise.
    drives: Dict[str, float] = field(default_factory=lambda: {
        "bond": 0.6, "explore": 0.5, "rest": 0.4, "express": 0.5,
    })
    coherence: float = 0.5
    alive_fraction: float = 1.0
    atp: float = 0.85
    vagal_tone: float = 0.55
    cortisol_baseline: float = 0.30


# ═══════════════════════════════════════════════════════════════════════════════
#   PUBLIC INTERFACE
#
#   Same shape as the real PhoenixRuntime.tick() return signature.
#   Internal computation is fully replaced by deterministic noise.
# ═══════════════════════════════════════════════════════════════════════════════


class MetabolicEngine:
    """Public demonstration shim around the real Phoenix runtime.

    The real engine is initialised with a CouplingMatrix (NxN organ-to-organ
    routing), WonderBus (gather/route/evolve), Gut (12 hormones → 5 somatic
    sensations + SomaFeedback loop), BiochemicalReactor (ligand-receptor
    kinetics), ReadoutLayer (RLS adaptation, no SGD), HamiltonianPhaseSpace
    (energy-conserving phase evolution), and a stack of organs (S1 Expression,
    S4 BioBody, S10 Morpho, Skin, Core, ReflexArc, Observer, ...).

    This shim accepts the same constructor signature, validates nothing,
    and emits SHA-derived signals that match the real engine's external
    schema. Useful for integration testing, partner demos, and architectural
    walkthroughs without exposing proprietary dynamics.
    """

    def __init__(self, agent_name: str = "phoenix-demo",
                 seed: Optional[str] = None, **kwargs: Any) -> None:
        seed_bytes = (seed or agent_name).encode("utf-8")
        self._state = _OpaqueState(seed=_digest(seed_bytes))
        self._agent_name = agent_name
        # Real engine accepts dozens of kwargs (organ specs, coupling profiles,
        # initial sedimentation, drive priors, ...). Demo silently absorbs them.
        self._absorbed_kwargs = list(kwargs.keys())

    # ─────────────────────────────────────────────────────────────────────────
    #   Tick — the heartbeat. In the real engine this runs the full
    #   CouplingMatrix gather/route/evolve cycle, updates BCM weights online,
    #   applies three-factor STDP to procedural memory, evolves the
    #   Hamiltonian phase space, runs reflex arcs before cortical processing,
    #   sediments salient experiences, modulates LLM hyperparameters, and
    #   emits an ExpressionVector. Here: deterministic drift.
    # ─────────────────────────────────────────────────────────────────────────

    def tick(self, stimulus: Optional[str] = None) -> Dict[str, Any]:
        s = self._state
        s.tick += 1
        d = _digest(s.seed, s.tick.to_bytes(8, "big"),
                    (stimulus or "").encode("utf-8"))

        # Hormonal update — NOT real Hill-kinetics, deterministic surrogate.
        for i, key in enumerate(s.hormones):
            tgt = _u32(d, i * 4)
            tgt = _hill(tgt, K=0.5, n=3.0)
            s.hormones[key] = round(_smooth(s.hormones[key], tgt), 4)

        # Somatic update — NOT real Gut interoception.
        soma_seed = _digest(d, b"soma")
        for i, key in enumerate(s.soma):
            tgt = _naka_rushton(_u32(soma_seed, i * 4), sigma=0.4, n=2.5)
            s.soma[key] = round(_smooth(s.soma[key], tgt, alpha=0.22), 4)

        # Drive vector — NOT real DriveSedimentationLayer.
        drive_seed = _digest(d, b"drive")
        for i, key in enumerate(s.drives):
            tgt = _u32(drive_seed, i * 4)
            s.drives[key] = round(_smooth(s.drives[key], tgt, alpha=0.12), 4)

        # Coherence — NOT real phase-space coherence.
        coh_target = _hill(_u32(_digest(d, b"coh")), K=0.45, n=4.0)
        s.coherence = round(_smooth(s.coherence, coh_target, alpha=0.20), 4)

        # ATP / alive_fraction / vagal — opaque drift.
        s.atp = round(max(0.05, min(1.0, s.atp + (_u32(d, 16) - 0.5) * 0.04)), 4)
        s.alive_fraction = round(
            max(0.85, min(1.0, s.alive_fraction + (_u32(d, 20) - 0.5) * 0.01)), 4
        )
        s.vagal_tone = round(_smooth(s.vagal_tone,
                                     _u32(_digest(d, b"vagus")), alpha=0.10), 4)

        return {
            "ts": _ts(),
            "tick": s.tick,
            "agent": self._agent_name,
            "hormones": dict(s.hormones),
            "soma": dict(s.soma),
            "drives": dict(s.drives),
            "coherence": s.coherence,
            "atp": s.atp,
            "alive_fraction": s.alive_fraction,
            "vagal_tone": s.vagal_tone,
            # Real engine emits an ExpressionVector with prompt-compiler bias.
            # Demo: opaque marker only.
            "expression_signature": _digest(d, b"expr").hex()[:16],
        }

    # ─────────────────────────────────────────────────────────────────────────
    #   The following methods exist on the real engine. In the public demo
    #   they raise NotImplementedError with an explicit pointer to the NDA
    #   contact. This is by design.
    # ─────────────────────────────────────────────────────────────────────────

    def update_weights_online(self, *args: Any, **kwargs: Any) -> None:
        """REAL engine: BCM rule + three-factor STDP + synaptic scaling,
        applied per-tick, no batches, no gradients, no loss function.
        DEMO: not exposed."""
        raise NotImplementedError(
            "Online weight dynamics are part of the proprietary core "
            "(Phoenix v8.5.1). Contact partners@fsbio.ai under NDA."
        )

    def modulate_llm_generation(self, *args: Any, **kwargs: Any) -> None:
        """REAL engine: hormonal vector → LLM hyperparameters
        (temperature, top-p, attention bias) BEFORE generation.
        DEMO: not exposed."""
        raise NotImplementedError(
            "Hormone-to-hyperparameter mapping is proprietary. "
            "Contact partners@fsbio.ai under NDA."
        )

    def sediment_memory(self, *args: Any, **kwargs: Any) -> None:
        """REAL engine: BTSP-based one-shot consolidation
        (Bittner 2017), salience-weighted, sliding-threshold
        sedimentation. NO RAG. NO embedding similarity.
        DEMO: not exposed."""
        raise NotImplementedError(
            "Sedimentation dynamics are proprietary. "
            "Contact partners@fsbio.ai under NDA."
        )


# ═══════════════════════════════════════════════════════════════════════════════
#   DEMO LOOP
# ═══════════════════════════════════════════════════════════════════════════════


def run_demo(ticks: int = 20, seed: str = "phoenix-public-demo") -> None:
    print("═" * 79)
    print("  FSBio Metabolic AI — Public Demonstration Build")
    print(f"  Runtime version : v9.0.1-enterprise")
    print(f"  Internal core   : Phoenix v8.5.1  [proprietary, patent pending]")
    print(f"  Build date      : 2026-04-28")
    print(f"  Seed            : {seed!r}")
    print("═" * 79)
    print()
    print("  NOTICE: This is a PUBLIC DEMONSTRATION shim. The interface is")
    print("  identical to the real Phoenix runtime; the internal dynamics are")
    print("  replaced by a deterministic SHA-256 stream. The real engine has")
    print("  NO loss function, NO backpropagation, NO RLHF. Weights update on")
    print("  the fly via BCM rule (Bienenstock-Cooper-Munro 1982), three-factor")
    print("  STDP (Izhikevich 2007), and synaptic scaling (Turrigiano 2008).")
    print("  See Zenodo DOIs (2026-04-13, 2026-04-20) for academic detail.")
    print("─" * 79)
    print()

    engine = MetabolicEngine(agent_name="phoenix-demo", seed=seed)

    for _ in range(ticks):
        out = engine.tick(stimulus=None)
        h = out["hormones"]
        s = out["soma"]
        d = out["drives"]
        print(
            f"[t {out['tick']:03d}] "
            f"DA={h['DA']:.2f} OT={h['OT']:.2f} CORT={h['CORT']:.2f} "
            f"NE={h['NE']:.2f}  │  "
            f"warm={s['warmth']:.2f} tens={s['tension']:.2f}  │  "
            f"bond={d['bond']:.2f} expl={d['explore']:.2f}  │  "
            f"coh={out['coherence']:.2f} atp={out['atp']:.2f} "
            f"alive={out['alive_fraction']:.3f}  │  "
            f"sig={out['expression_signature']}"
        )
        time.sleep(0.04)

    print()
    print("─" * 79)
    print("  Demo trace complete.")
    print()
    print("  TO REVIEW THE REAL ENGINE:")
    print("    • Academic detail   : Zenodo preprints (DOI 2026-04-13, 2026-04-20)")
    print("    • Live demonstration: Insight Forum, Yerevan, 2026-05-12")
    print("    • Partner / NDA     : partners@fsbio.ai")
    print()
    print("  TO REVIEW WHAT THIS DEMO IS NOT:")
    print("    • try engine.update_weights_online(...)   → NotImplementedError")
    print("    • try engine.modulate_llm_generation(...) → NotImplementedError")
    print("    • try engine.sediment_memory(...)         → NotImplementedError")
    print()
    print("  These are proprietary by design. The demo is honest about it.")
    print("═" * 79)


if __name__ == "__main__":
    run_demo()
