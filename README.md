# Cricket Height Research

**Statistical analysis of height selection pressure across 23 ICC World Cups (1975-2026)**

This research investigates whether international cricket teams systematically select taller players over time, and whether this trend exceeds natural population height increases across participating nations.

## Research Question

Do cricket teams exhibit "height selection pressure" — a measurable bias toward selecting taller players that goes beyond general population height trends?

## Methodology

**Data:** Tournament-by-tournament player data across 23 ICC World Cups, organised by four functional categories:
- Wicketkeepers (WK)
- Batsmen (BAT)
- Fast Bowlers (FAST)
- Spin Bowlers (SPIN)

**Variables:** Height (cm), date of birth, player category, nation, tournament year, verification status

**Statistical Techniques:**
- ANOVA with interaction terms (category x era)
- Population-adjusted regression analysis
- Breakpoint testing (2007 T20 era hypothesis)
- Temporal trend analysis with confidence bands
- Data quality validation (height range checks 155-220cm, verification flags)

## Data Pipeline

Raw JSON (per tournament) --> CSV (cleaned) --> Parquet (analysis-ready)

## Tech Stack

| Purpose | Libraries |
|---------|-----------|
| **Data** | pandas, numpy |
| **Statistics** | scipy, statsmodels, pingouin |
| **Visualisation** | matplotlib, seaborn |
| **Pipeline** | Python scripts, JSON to CSV to Parquet |

## Visualisations

- Violin plots: height distributions by player category
- Temporal trend lines: mean height 1975-2026 with regression bands
- 4-panel publication figure: distributions, trends, country comparisons, ODI vs T20
- Forest plots for ANOVA effect sizes

## Setup

```bash
git clone https://github.com/brettleehari/cricheightresearch.git
cd cricheightresearch
pip install -r requirements.txt
python scripts/analyze.py
```

## Author

**Hariprasad Sudharshan** - [GitHub](https://github.com/brettleehari)
