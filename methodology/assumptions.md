# ASF — Honest Assumptions and Limitations

This document states what ASF assumes, where those assumptions may not hold, and what evidence would be required to validate the framework further.

Intellectual honesty about limitations builds more credibility than hiding them.

---

## Assumption 1 — The six dimensions are the right ones

**What ASF assumes:** Adaptation speed is primarily determined by six factors: how fast you detect change, decide, execute, receive feedback, learn, and reduce manual dependencies.

**Where this might not hold:** In highly regulated environments, regulatory approval cycles may be the dominant constraint and cannot be compressed regardless of other dimensions. In early-stage organizations, leadership attention may be the binding constraint rather than any structural dimension.

**What would validate it:** A study comparing organizations with similar ASF scores to their actual transformation outcomes over 3-5 years. High correlation between ASF bottleneck identification and self-reported primary constraint would support the model.

---

## Assumption 2 — The weights are correct

**What ASF assumes:** Execution Latency is weighted 0.30 — the highest weight — because it was the most common bottleneck in the 100-case dataset. The other weights (Observation 0.15, Decision 0.25, Feedback 0.15, Dependency 0.15, Learning −0.10) follow from the same dataset.

**Where this might not hold:** The 100-case dataset was manually scored by one analyst. The weights reflect patterns in that dataset, not empirical outcomes. A different analyst might score differently. The weights have not been validated against objective organizational performance data.

**What would validate it:** Regression analysis comparing ASF dimension scores to time-to-target outcomes across 500+ organizations with independently verified performance data.

---

## Assumption 3 — The 1-5 scale is linear

**What ASF assumes:** A system that scores 4 on execution latency is twice as slow as one that scores 2.

**Where this might not hold:** The relationship may be non-linear. Moving from 4 to 3 may be much harder than moving from 2 to 1. Organizational friction often has threshold effects — a process with 5 approval gates is not necessarily five times slower than one with 1.

**What would validate it:** Empirical measurement of actual delay durations at each score level across a large dataset.

---

## Assumption 4 — The six dimensions are independent

**What ASF assumes:** Each dimension is scored separately and contributes independently to the total score.

**Where this might not hold:** In practice, high decision latency usually causes high execution latency. Governance friction affects multiple dimensions simultaneously. The model does not capture this correlation.

**What would validate it:** Factor analysis of dimension scores across a large dataset to measure actual interdependence.

---

## Assumption 5 — Public data is sufficient for company analysis

**What ASF assumes:** Annual reports, SEC filings, earnings calls, and press releases contain enough information to score the six dimensions reliably.

**Where this might not hold:** Companies control what they disclose. Internal execution problems are rarely disclosed with precision. The gap between reported performance and actual performance may be significant. A company describing their digital transformation in positive terms in an annual report may be slower internally than the public disclosure suggests.

**What ASF does about this:** Confidence levels (High / Medium / Low) are assigned to each analysis. Most company analyses are Medium confidence because they rely on public disclosure. Where specific quantitative data is available (AT&T's 58% adoption rate, Boeing's 18 planes/month), confidence is higher.

---

## Assumption 6 — Current velocity will continue

**What CRT assumes:** The rate at which an organization is currently closing the capability gap will continue at roughly the same pace until the target date.

**Where this might not hold:** Organizations can accelerate. Leadership changes, new investment, or successful interventions can significantly change velocity. The CRT estimate is a current-state projection, not a deterministic forecast.

**What ASF does about this:** CRT outputs a range (low-high confidence interval) rather than a single number. The range widens with lower evidence confidence.

---

## What ASF does not claim

- ASF does not claim to predict whether any specific company will achieve its goals
- ASF does not claim the scores are audited or independently verified
- ASF does not claim the methodology has been peer-reviewed or academically validated
- ASF does not provide investment, legal, or financial advice
- ASF does not claim complete coverage of all factors that affect organizational performance

---

## What would make ASF significantly more credible

1. **Automated scoring from documents** — LLM reads primary sources, assigns scores with evidence citations. This removes human judgment from score assignment.

2. **Outcome validation study** — Compare ASF scores from 2023 to actual 2025 organizational outcomes. If companies ASF scored as "High Risk" at the bottleneck dimension actually missed targets in that dimension more often than not, the model is predictive.

3. **Independent replication** — Have a second analyst score the same companies using the ASF methodology. Measure inter-rater reliability. If two analysts produce similar scores independently, the methodology is more defensible.

4. **Academic peer review** — Submit the methodology to a management science, information systems, or organizational behavior journal. Peer review will identify weaknesses the builder cannot see.

5. **Practitioner validation** — Have transformation executives at 10+ organizations evaluate whether ASF correctly identified their primary constraint. Their agreement or disagreement with the bottleneck identification is the most direct validation available.
