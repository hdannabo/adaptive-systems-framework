# ASF Annual Validation Report — [YEAR]

**Report period:** [START_DATE] to [END_DATE]  
**Compiled by:** [ANALYST]  
**Date published:** [DATE]  
**Repository:** https://github.com/hdannabo/adaptive-systems-framework

---

## Executive Summary

[3–5 sentences summarizing: total predictions tracked, accuracy achieved,
key confirmed predictions, key refuted predictions, framework improvements made]

---

## Prediction Accuracy

| Metric | Target | Result | Status |
|---|---|---|---|
| Overall prediction accuracy | ≥ 70% | [X]% | [PASS/FAIL] |
| High confidence accuracy | ≥ 80% | [X]% | [PASS/FAIL] |
| False positive rate | ≤ 20% | [X]% | [PASS/FAIL] |
| Average lead time | ≥ 6 months | [X] months | [PASS/FAIL] |

---

## Predictions Resolved This Period

[For each resolved prediction:]

### [P_ID] — [COMPANY] — [OUTCOME]

**Prediction:** [exact text from register]  
**Assessment date:** [date]  
**Outcome date:** [date]  
**Lead time:** [months]  
**Evidence:** [what was observed in the public disclosure]  
**Analysis:** [why ASF was right/wrong — which dimension drove the prediction and whether that dimension's evidence was accurate]

---

## Confidence Calibration

[Table showing: for each confidence level, what % of predictions were confirmed]

| Confidence level | Predictions | Confirmed | Accuracy |
|---|---|---|---|
| High | [n] | [n] | [%] |
| Medium | [n] | [n] | [%] |
| Low | [n] | [n] | [%] |

[Assessment: is High confidence producing higher accuracy than Medium? If not, what does this indicate about the confidence assignment rubric?]

---

## Missed Predictions — Root Cause Analysis

[For each refuted prediction:]

### [P_ID] — [COMPANY] — Why ASF was wrong

**Prediction:** [exact text]  
**What happened instead:** [description]  
**Root cause:**
- [ ] Incorrect evidence interpretation at scoring time
- [ ] Correct scoring but wrong directional logic
- [ ] External shock not visible in public data at scoring time
- [ ] Dimension interdependency not captured by additive model
- [ ] T_base calibration error (CRT miss)

**Framework improvement:** [specific rubric or methodology change made in response]

---

## Lead Time Analysis

[For confirmed predictions: how far in advance did ASF identify the constraint?]

| ID | Company | Assessment date | Outcome date | Lead time | Confidence |
|---|---|---|---|---|---|
| [P_ID] | [co] | [date] | [date] | [months] | [High/Med/Low] |

**Key finding:** [Was ASF identifying constraints with ≥6 months lead time? What was the range?]

---

## Framework Reliability Update

[Summary of any inter-rater reliability study results from this period]

Current κ: [value]  
Bottleneck agreement rate: [%]  
Companies scored by external analysts: [list]

---

## CRT Accuracy Update

[How many CRT predictions (from P009, P006) have resolved? Are they on track?]

| Company | CRT prediction | Horizon | Status |
|---|---|---|---|
| Boeing | 38 planes/month not reached by 2028 | Q4 2028 earnings | [Pending/Confirmed/Refuted] |
| AT&T | $4B savings not achieved by 2028 | 2028 annual report | [Pending/Confirmed/Refuted] |

---

## Predictions Still Pending

| ID | Company | Horizon | Confidence | Months pending |
|---|---|---|---|---|
[auto-generated from register]

---

## Framework Improvements Made This Year

[List any changes to rubric, confidence criteria, or T_base values made in response to outcomes]

1. [Improvement] — [Reason] — [Prediction that motivated it]

---

## Appendix: Full Prediction Register Extract

[Include complete prediction register as of report date]
