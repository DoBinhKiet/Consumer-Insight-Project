# Digital Payment Adoption in Vietnam — Consumer Insight Project

A consumer research project I built as part of my application to Decision Lab's Market Research Consultant Programme (May 2026). The goal was to demonstrate the full consulting capability chain: structure a business problem → design research → analyse data → produce a commercial recommendation.

The hypothetical client is **Techcombank**, one of Vietnam's leading private commercial banks. The research question: who are the next-wave adopters of Techcombank's digital banking platform, what stops them from converting, and what should Techcombank do about it?

---

## What's in this repo

```
├── data/
│   └── Findex_Microdata_2025_updateViet_Nam.csv   # World Bank Global Findex 2021, Vietnam module
├── scripts/
│   ├── phase3_step1_explore.py      # data loading, SQLite setup, SQL-based demographic analysis
│   ├── phase3_step2_regression.py   # logistic regression, marginal effects, decision tree, segment profiling
│   └── phase3_step3_excel.py        # styled Excel workbook output
├── outputs/
│   ├── Techcombank_Digital_Adoption_Report.html    # the main client-facing report
│   └── Techcombank_Digital_Adoption_Analysis.xlsx  # analytical workbook (3 sheets)
└── README.md
```

---

## Data sources

**World Bank Global Findex 2021 — Vietnam module**
- 1,000 nationally representative Vietnamese adults (998 usable after cleaning)
- Individual-level survey: account ownership, digital payment use, saving, borrowing, demographics
- Free download from microdata.worldbank.org (catalog 5861), requires registration
- This is the main analytical dataset

**Decision Lab Connected Consumer Q4 2025**
- Quarterly tracker of Vietnamese digital platform usage, n = 1,427
- Used for market context — platform penetration trends, generational breakdowns
- Free PDF from decisionlab.co/library

**Decision Lab AI and the New Financial Decision Journey (Dec 2025)**
- Consumer financial decision journey research, n = 894
- Used for trust barrier evidence and journey-stage analysis
- Free PDF from decisionlab.co/library

**Decision Lab State of Consumer AI in Vietnam (Aug 2025)**
- AI adoption and barrier research, n = 600
- Used to corroborate age and education patterns found in Findex
- Free PDF from decisionlab.co/library

---

## How to run

You need Python 3.x with the following libraries:

```
pip install pandas numpy statsmodels scikit-learn openpyxl
```

Put the Findex CSV in the same directory as the scripts and run them in order:

```bash
python phase3_step1_explore.py   # creates findex_vietnam.db + prints demographic tables
python phase3_step2_regression.py  # runs the regression, decision tree, segment profiles
python phase3_step3_excel.py     # generates the Excel workbook
```

Script 1 needs to run first because it creates the SQLite database that scripts 2 and 3 load from.

---

## What the analysis actually found

Three findings that matter commercially for Techcombank:

**1. The access paradox.** The next-wave adopter segment — banked Vietnamese adults who haven't gone digital yet — has 90.8% internet access. The barrier isn't infrastructure. It's behavioural inertia. Internet access raises adoption probability by 23.5 percentage points in the regression (the single biggest predictor), but the next-wave segment already clears that bar. The problem is the absence of a compelling first-use trigger.

**2. The formal saver is the highest-value target.** Saving formally with an institution raises adoption probability by 12.8pp — statistically identical to moving up one full education level (also 12.8pp). 60.5% of the next-wave segment already saves formally. These are existing Techcombank customers who haven't been activated digitally. This is a retention and activation play, not cold acquisition.

**3. Age beats geography as a segmentation axis.** Rural consumers adopt at 68.1% vs urban at 57.5% — geography isn't the barrier and isn't statistically significant in the regression (p = 0.47). Age is. Adoption peaks at 83.3% for 25-34 year olds then drops to 18.3% for 55+. The 45-54 cohort at 59.1% is the tractable swing segment — still above 50%, likely already in a Techcombank relationship, but not yet digitally active.

**Model performance:** logistic regression AUC = 0.93, pseudo R² = 0.37. Decision tree AUC = 0.90 for comparison.

---

## Report structure

The HTML report (open in any browser) has 6 sections:

1. Executive summary
2. Market context
3. Key insights (3 insight cards with behavioral science framing)
4. Commercial recommendations (4 prioritised recommendations)
5. Methodological note (causal identification, sample limitations)
6. What this analysis cannot answer (research design reflection)

---

## Skills demonstrated

This was intentionally designed to show specific skills for a market research consulting role:

- **SQL** — all demographic breakdowns run as SQL queries via SQLite before touching pandas
- **Python** — pandas, statsmodels, scikit-learn, openpyxl throughout
- **Excel** — styled 3-sheet workbook with conditional formatting, generated programmatically
- **Causal inference** — logistic regression with average marginal effects; explicit discussion of endogeneity and identification limits in the methodological note
- **Research fundamentals** — multi-source data strategy, gap analysis, primary research proposal
- **Machine learning** — decision tree classifier with feature importance, AUC comparison against logistic regression
- **Behavioral science** — status quo bias, trust transfer, loss aversion applied to each insight
- **Clear communication** — conclusions-first report structure, client-ready tone throughout

---

## About me

Final-year Economics major with Applied Mathematics minor at Fulbright University Vietnam. GPA 3.72. Graduating June 2026.

I'm interested in quantitative consumer research and the intersection of behavioral economics and commercial decision-making. This project was built independently over ~3 weeks using only publicly available data.

Contact: dobinhkiet2004@gmail.com
LinkedIn: linkedin.com/in/kietdobinh1622004
