# ASF Outcome Tracking Workflow

**Purpose:** Describe exactly how predictions are monitored and outcomes are recorded.  
**Principle:** No prediction is ever modified. Outcomes are appended, not edited.

---

## Priority Queue (Nearest checkpoints first)

| ID | Company | Checkpoint | Date | Action required |
|---|---|---|---|---|
| P001 | LTM | Q1FY27 earnings | ~July 22, 2026 | Read earnings release; check BFSI YoY growth |
| P003 | LTM | Any LTM event | Ongoing | Monitor for BlueVerse contract disclosure |
| P004 | AT&T | Q3 2026 earnings | ~October 2026 | Read earnings; check for mandatory adoption program announcement |
| P007 | Boeing | Q3/Q4 2026 earnings | Oct–Jan 2027 | Read earnings; check monthly production rate |
| P005 | AT&T | Q4 2026 earnings | ~January 2027 | Read earnings; check AI savings run-rate |
| P008 | Boeing | Annual report 2026 | ~February 2027 | Read 10-K; check management attribution of constraints |
| P002 | LTM | Q4FY27 earnings | ~April 2027 | Read earnings; check full-year revenue growth |
| P012 | Framework | Internal | Immediate | Re-run calibration with revised T_base values |
| P013 | Framework | Study completion | 6–8 weeks | External analyst study conclusion |

---

## Step-by-Step Outcome Resolution Process

### Step 1: Monitor the checkpoint source

Each prediction names a specific observable source (earnings release, annual report, press release).
Subscribe to investor relations alerts or set calendar reminders for each company's earnings calendar.

- Boeing IR: ir.boeing.com
- LTM IR: ltimindtree.com/investors  
- AT&T IR: ir.att.com

### Step 2: Read the source document

When the checkpoint document is published, read the relevant sections.
Do not rely on news coverage or analyst summaries — read the primary source.

For earnings releases: check the specific metric named in the confirming/refuting signal.
For annual reports: check the management commentary section for language matching the bottleneck.

### Step 3: Apply the confirming/refuting criteria

Each prediction has an explicit confirming signal and refuting signal.
Apply the criteria as written, not as interpreted.

If the outcome is ambiguous (neither clearly confirming nor clearly refuting), record "Partial"
with detailed notes explaining the ambiguity.

### Step 4: Record the outcome

Using `validation_metrics.py`:

```bash
# Confirmed example
python validation_metrics.py --update P001 Confirmed \
    "BFSI +2.1% YoY Q1FY27 earnings July 22 2026" \
    2026-07-22

# Refuted example
python validation_metrics.py --update P001 Refuted \
    "BFSI -1.8% YoY Q1FY27, decline continued" \
    2026-07-22

# Partial example
python validation_metrics.py --update P004 Partial \
    "AI champions program expanded but no mandatory program with specific targets announced" \
    2026-10-23
```

### Step 5: Commit and publish

Commit the updated `prediction_register.json` and regenerate `prediction_register.md`.
The Git commit hash serves as the immutable timestamp.

```bash
git add validation/prediction_register.json
git add validation/prediction_register.md
git commit -m "outcome(P001): LTM BFSI confirmed positive Q1FY27 — first ASF prediction confirmed"
git push
```

### Step 6: Root cause analysis on misses

When a prediction is refuted:

1. Identify which specific evidence led to the incorrect prediction
2. Determine whether the miss was due to:
   - Incorrect dimension scoring (evidence was misread)
   - Correct dimension scoring but wrong directional prediction
   - External shock not present in the evidence at scoring time
3. Document in `validation/missed_predictions/P00X_analysis.md`
4. Update methodology if systemic scoring error is identified

Refutations are not failures. They are information. A refuted prediction that identifies
a scoring rubric gap is more valuable than a confirmed prediction that reveals nothing new.

---

## Partial Outcome Handling

A prediction is "Partial" when:
- The directional prediction is correct but the magnitude is different
- The predicted event occurred but in a different form
- The confirming signal was met but the refuting signal was also partially met

Partial outcomes count as 0.5 in accuracy calculations.

---

## The P001 Resolution Protocol (Priority — July 22, 2026)

P001 is the first resolvable prediction and the highest-value validation checkpoint.

**On approximately July 22, 2026:**

1. Go to ltimindtree.com/investors
2. Download the Q1FY27 earnings release or press release
3. Find the vertical revenue breakdown
4. Check the BFSI segment YoY growth rate
5. Apply the criteria:
   - BFSI growth ≥ 0%: record P001 as **Confirmed** with exact figure
   - BFSI growth < 0%: record P001 as **Refuted** with exact figure
6. Commit immediately
7. If confirmed: publish a brief note in the repository and update validation/README.md

A confirmed P001 is ASF's first publicly timestamped prediction confirmation.
Document it clearly. This is the transition from "framework" to "tested framework."

---

## Annual Validation Report

Every June (anniversary of the first assessment), generate an annual validation report using:

```bash
python validation_metrics.py --report > validation/annual_report_2027.txt
```

The annual report covers:
- All predictions resolved in the past 12 months
- Accuracy against targets
- Confidence calibration (were High confidence predictions more accurate?)
- Lead time analysis
- Rubric improvements made based on misses
