# Independent verification of OpenAI's preprint “The Quasi-Riemann Hypothesis: A Zero-Free Half-Plane Re s > 7/8”

This repository publishes the results of an independent verification of the paper announced by OpenAI on
30 September 2026 in its `openai/math` repository. The paper claims that the Riemann zeta function, every Dirichlet
*L*-function, and every finite-order Hecke *L*-function over **Q**(√−3) have no zeros in the half-plane Re *s* > 7/8.
If true, this resolves the *quasi-Riemann hypothesis*.

**Upstream sources (verified at commit [`adc7f1241b42`](https://github.com/openai/math/tree/adc7f1241b42e322a6451854ab7e4b4c146bf78a)):**

* Repository: https://github.com/openai/math
* Paper PDF: https://github.com/openai/math/blob/main/preprints/The-Quasi-Riemann-Hypothesis-September-30-2026/paper.pdf
* Contents (CONTENTS.md): https://github.com/openai/math/blob/main/CONTENTS.md

> This project is not affiliated with OpenAI. The paper itself is not redistributed here; please obtain it from the
> links above. This verification is not a substitute for expert peer review.

---

## Summary of findings

| Question | Verdict | Evidence |
|---|---|---|
| Is ζ(*s*) ≠ 0 for Re *s* > 7/8? | **Verified** | The accompanying Lean 4 formalization was rebuilt from source: 2,924 modules, 0 errors. The theorem depends only on the standard axioms `propext`, `Classical.choice`, `Quot.sound`. |
| Is *L*(*s*, χ) ≠ 0 for Re *s* > 7/8 for every Dirichlet character χ (principal pole at *s* = 1 excepted)? | **Verified** | Same build and axiom check. |
| Hecke *L*-functions over **Q**(√−3) | Correct within the paper's argument; the corresponding Lean challenge (which uses custom definitions) was **not** built | — |
| Is the paper's written proof correct? | No error found in any part checked | The core logic was checked line by line and 66 explicit identities and inequalities were checked in exact arithmetic. The heaviest technical sections were not re-read by hand (see *Scope*). |
| Can the same method prove the Riemann hypothesis (Re *s* > 1/2)? | **No** | Quantitative barrier analysis below. |

### 1. Formal verification (decisive evidence)

The upstream comparator challenge states, using only Mathlib definitions:

```lean
theorem riemannZeta_ne_zero_of_seven_eighths_lt_re
    {s : ℂ} (hs : (7 / 8 : ℝ) < s.re) : riemannZeta s ≠ 0
```

The solution module `OAI.NumberTheory.DirichletL.Nonvanishing` was built locally:

* Toolchain: Lean 4.34.1 (official release). Mathlib `d13f23b` from the official build cache. PrimeNumberTheoremAnd `c39a751` and rellich-kondrachov `70f85d4`, with the upstream compatibility patches applied.
* `lake build OAI.NumberTheory.DirichletL.Nonvanishing` finished 7,061 jobs, including local elaboration and kernel checking of all 2,924 `OAI` modules (about 490k lines), with **0 errors** and no `sorry` warnings. It took 252 minutes on 8 cores / 16 GB.
* [`lean/QRHCheck.lean`](lean/QRHCheck.lean) copies the challenge statement verbatim and proves it from the solution theorem, so the types match. Its `#print axioms` output ([`lean/print_axioms_output.txt`](lean/print_axioms_output.txt)) is:

```
'OAI.riemannZeta_ne_zero_of_seven_eighths_lt_re' depends on axioms: [propext, Classical.choice, Quot.sound]
'OAI.DirichletCharacter.LFunction_ne_zero_of_seven_eighths_lt_re' depends on axioms: [propext, Classical.choice, Quot.sound]
```

* A static scan of the 2,924-file closure found no `sorry`, `axiom`, `native_decide`, `implemented_by`, `extern`, `unsafe`, `opaque`, `run_cmd`, `elab`, `macro_rules`, `initialize`, `skipKernelTC`, or `addDecl`.
* An additional `leanchecker` replay completed without error for the two final modules. A replay of all 2,924 modules was stopped after about 60 minutes without having reported an error.

**Remaining trust base:** the Lean kernel, the official Mathlib build cache, and Mathlib's definitions of
`riemannZeta` and `DirichletCharacter.LFunction`.

Details: [`lean/lean_build_report.md`](lean/lean_build_report.md) (Japanese) and [`lean/lake_build_log.txt`](lean/lake_build_log.txt).

### 2. Review of the written argument

* **Barrier tests: all passed.**
  * The proof uses Euler products essentially, so Davenport–Heilbronn-type counterexamples do not apply. The script re-computes the Davenport–Heilbronn zero 0.808517 + 85.699348 i.
  * The target zero is never "excluded by a density estimate". It enters through the size of the Mellin signal of 1/*L*, and density-type counts are used only for the other twists.
  * All exponent margins are uniform in the target character.
  * The section dependency graph is acyclic.
* **Checked line by line:** the continuation criterion (Prop. 2.1), the Hecke→Dirichlet transfer (Prop. 11.3), and Corollary 1.2 (logic only).
* **Checked in exact arithmetic (66/66 pass, [`scripts/numerical_checks.py`](scripts/numerical_checks.py)):**
  * every rational constant and exponent identity of §20;
  * the completed-square certificate of Lemma 20.2. Its grid minimum of −E\* is 2.28·10⁻⁴, about twice the certified 49/440640.
* **One minor remark:** at TeX line 16141 the bound *R*\* + Δ/4 ≤ 139/96 is valid, but the exact maximum is 137/96.

![Lemma 20.2 certificate](figures/fig_endpoint_certificate.png)

### 3. Why the method cannot reach the Riemann hypothesis

The low estimate and the Mellin normalization fix the boundary exactly at

  σ₀ = 1 − h/6 + b/12  (Part I: h = 1/2, b = 0 → 11/12; Part II: h = 13/16, b = 1/8 → 7/8).

Here 1/6 comes from the pole of ζ_F(6z) produced by the sextic frequency structure *ua*⁶. Reconstructing the explicit
§20 constraints as functions of the geometry gives the following limits:

* **Low-side geometry.** Under the paper's normalization *M* + ℓ = 1, σ₀ ≥ 2/3 for every choice of geometry.
* **Density barrier.** Rows whose zeros lie near Re *s* = 1/2 cannot be counted with any saving. This forces σ₀ > 13/15 ≈ 0.8667, even with density-hypothesis-strength counts.
* **Bootstrap saturation.** Re-running the second stage with input 7/8 gives at most 0.87451. The iteration has a fixed point at about 0.8745.
* **Stated ranges.** Several lemmas are stated only down to 7/8: `lem:bin-contour-accounting` (σ₀ ∈ [7/8, 1)), `lem:local-euler` (Re *x* ≥ 7/8), and `lem:plain` (κ ≥ 3/4).

![Barrier analysis](figures/fig_barrier.png)

These limits are model computations that use the paper's exponent formulas outside their stated ranges, so they
are optimistic. They show that a substantially new idea, not further tuning, would be needed.
Details: [`reports/barrier_analysis.md`](reports/barrier_analysis.md), [`reports/improvement_exploration.md`](reports/improvement_exploration.md).

---

## Scope and limitations

* The Lean build certifies the **theorem**, not the paper's prose argument line by line. No mapping from the paper's numbered statements to Lean declarations is provided upstream.
* The following were not re-checked by hand; their correctness rests on the formalization:
  * Prop. 5.1 (cubic reflection) and Lemma 9.1 (sextic large sieve);
  * Props. 9.2 and 19.2 (row counts) and Lemma 7.x (local Euler identity);
  * the moment estimates of §§17–18.
* The Hecke challenge over **Q**(√−3), which uses custom definitions, was not built.
* A planned per-lemma independent second-opinion review could not be run.

## Repository layout

| Path | Content |
|---|---|
| [`reports/referee_report_en.pdf`](reports/referee_report_en.pdf) ([`.tex`](reports/referee_report_en.tex)) | Referee-style report (English) |
| [`reports/verification_report_ja.md`](reports/verification_report_ja.md) | Full verification report (Japanese) |
| [`reports/sanity_checks.md`](reports/sanity_checks.md) | Structural barrier tests T1–T7 (Japanese) |
| [`reports/proof_structure.md`](reports/proof_structure.md) | Proof skeleton, two-stage table, section index (Japanese) |
| [`reports/barrier_analysis.md`](reports/barrier_analysis.md) | Why the method cannot reach Re *s* > 1/2 (Japanese) |
| [`reports/improvement_exploration.md`](reports/improvement_exploration.md) | Scenarios for improving 7/8 (Japanese) |
| [`data/issue_log.csv`](data/issue_log.csv) | Per-item verdicts (24 items) |
| [`data/numerical_checks_results.json`](data/numerical_checks_results.json) | Output of the exact-arithmetic checks |
| [`data/provenance.json`](data/provenance.json) | Upstream commit, file hashes, retrieval time |
| [`lean/`](lean/) | Build report, `QRHCheck.lean`, axiom output, sanitized build log |
| [`scripts/numerical_checks.py`](scripts/numerical_checks.py) | Exact / numerical checks (sympy, mpmath) |
| [`scripts/lean_import_closure.py`](scripts/lean_import_closure.py) | Computes the Lean import closure of the solution module |
| [`figures/`](figures/) | Figures used above, plus the section dependency graph |

## Reproducing the formal check

```sh
git clone https://github.com/openai/math && cd math && git checkout adc7f1241b42
cd lean
lake update                     # fetches dependencies and applies upstream compatibility patches
lake exe cache get              # Mathlib build cache
lake build OAI.NumberTheory.DirichletL.Nonvanishing
cp /path/to/this/repo/lean/QRHCheck.lean .
lake env lean QRHCheck.lean     # statement match + #print axioms
```

Reproducing the arithmetic checks requires Python 3 with `sympy`, `mpmath`, and `numpy`:
`python scripts/numerical_checks.py`.

*Verification date: 7 October 2026.*
