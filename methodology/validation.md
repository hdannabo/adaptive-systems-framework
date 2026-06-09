# ASF Validation Framework

## How Would ASF Be Proven Correct?

This document defines the validation methodology — what evidence would confirm or refute ASF's core claims.

---

## Claim 1 — The six dimensions are the primary drivers of adaptation failure

**What this claims:** Observation Latency, Decision Latency, Execution Latency, Feedback Delay, Learning Velocity, and Dependency Index collectively explain why transformation programs miss targets.

**How to test it:**
1. Select 50 organizations that missed a stated transformation target in 2022–2023
2. Have two independent analysts score each organization on all six dimensions using only information available before the miss
3. Measure: does the highest-scoring dimension (worst bottleneck) match the primary reason the organization self-reported as the cause of the miss?
4. Target: >70% match would support the claim; <50% would refute it

**Current status:** Not yet formally tested. The 100-case dataset provides supporting evidence but was constructed by one analyst and has not been independently replicated.

---

## Claim 2 — The weights (0.15, 0.25, 0.30, 0.15, 0.15, -0.10) are correct

**What this claims:** Execution Latency (0.30) has the greatest impact on whether a program succeeds or fails. Decision Latency (0.25) is second most important.

**How to test it:**
1. Take 100 organizations with known outcome data (succeeded or missed target)
2. Run ASF scoring on each
3. Run logistic regression: which dimension scores best predict outcome?
4. Compare regression coefficients to ASF weights
5. Recalibrate weights if significantly different

**Current status:** Weights derived from qualitative analysis of 100-case dataset. No regression analysis completed. This is the most important gap in the current methodology.

---

## Claim 3 — CRT correctly estimates time to close the gap

**What this claims:** An organization with an ALS of 4.0 and governance/execution friction of 0.70 will take approximately 20 months to close a 3.5-point capability gap.

**How to test it:**
1. Select 20 organizations that have successfully closed a defined capability gap
2. Apply CRT formula retroactively using data from the start of their program
3. Compare CRT estimate to actual time taken
4. Target: actual time within ±30% of CRT estimate for >60% of cases
5. Identify systematic biases (does CRT consistently underestimate or overestimate for certain domains?)

**Current status:** Not yet tested against outcome data. Domain calibration (base_months_per_point) is estimated, not empirically derived.

---

## Claim 4 — Recommendations reduce adaptation latency

**What this claims:** Implementing the P0 recommendation reduces ALS and accelerates target achievement.

**How to test it:**
1. Track 10 organizations that implement ASF P0 recommendations
2. Re-score them 90 days later
3. Measure: does the bottleneck dimension score improve? Does ALS decrease?
4. Measure: does the program trajectory improve toward hitting the target?

**Current status:** No tracking mechanism exists yet. This requires a customer relationship and follow-up measurement capability.

---

## Confidence Score Generation

Current confidence scoring is subjective (analyst assigns H/M/L). The following criteria formalize it:

### High confidence (requires ALL of):
- Quantitative primary data (financial filings, operational metrics)
- Data from within the last 12 months
- No conflicting signals from other public sources
- Multiple independent sources corroborate

### Medium confidence (requires MOST of):
- Qualitative disclosure in official document (annual report, earnings call)
- Data from within the last 24 months
- No major conflicting signals
- At least two sources available

### Low confidence (any of):
- Inference from indirect signals
- Data older than 24 months
- Conflicting signals present
- Single source only
- Significant disclosure selectivity evident

---

## Inter-Rater Reliability Protocol

**Goal:** Determine whether two analysts reading the same document produce similar ASF scores.

**Protocol:**
1. Select 10 organizations with substantial public disclosure
2. Provide each analyst with the same documents and the ASF dimension definitions
3. Score independently, no communication
4. Calculate Cohen's Kappa for each dimension
5. Target: κ > 0.60 (moderate agreement) for the methodology to be defensible

**Acceptable variation:** ±1 point on the 1–5 scale
**Unacceptable variation:** >1 point on the 1–5 scale, or different primary bottleneck identified

**Current status:** Not yet conducted. This is Priority 2 after outcome validation.

---

## The Minimum Credible Evidence Package

For ASF to be credible to a skeptical CTO or strategy consultant, it requires:

1. **Outcome correlation study** — ASF High Risk scores from 2023 should predict missed targets in 2024–2025 at >60% accuracy
2. **Inter-rater agreement** — Two independent analysts score the same 10 companies; Kappa > 0.60
3. **CRT calibration** — 10 organizations retroactively tested; actual time within ±30% of estimate for >60%
4. **At least one published case study** with named client permission showing ASF bottleneck identification led to measurable intervention

None of these require large budgets. The first three can be done with existing public data.

---

## What ASF Can Claim Right Now

ASF can defensibly claim:

✅ The six dimensions are grounded in established theory (MAPE-K, OODA, Senge)
✅ The scoring model produces consistent outputs for the same inputs
✅ The 100-case dataset shows execution friction as the dominant bottleneck across domains
✅ The CRT formula produces mathematically reasonable estimates
✅ The company analyses cite publicly available evidence for every score

ASF cannot yet claim:
❌ The weights are empirically validated against outcome data
❌ CRT estimates are statistically accurate
❌ Recommendations demonstrably reduce adaptation latency
❌ The methodology is independently replicable with high agreement
