# Cricket Anthropometric Research

## Getting Started with Claude Code

### Step 1: Set Up the Project

Open Claude Code and navigate to this folder:
```bash
cd /path/to/cricket-research
```

Claude Code will automatically read `CLAUDE.md` for project context.

### Step 2: Enable Auto-Accept Mode

Press `Shift+Tab` to enable auto-accept for a zero-prompts workflow.

### Step 3: Start Data Collection

Use these prompts to collect data tournament by tournament:

---

## Example Prompts for Data Collection

### Collect a Single Tournament

```
Create the raw data JSON for the 2023 ODI World Cup.
For each of the 8 nations (AUS, ENG, IND, PAK, WI, NZL, SL, RSA), identify the most 
representative Playing XI and collect:
- Player name and ID
- Category: WK, BAT, FAST, or SPIN
- Date of birth
- Height in cm
- Set height_verified=true only if confirmed from ESPN + secondary source
- Add flag and notes for any data quality issues

Save to data/raw/odi-2023.json

Don't ask questions, make reasonable choices.
```

### Collect Multiple Tournaments

```
Create raw data JSONs for all T20 World Cups from 2021-2024:
- t20-2021.json
- t20-2022.json  
- t20-2024.json

For each tournament, collect Playing XI for all 8 nations with full 
player details including heights, DOBs, categories, and verification flags.

Save to data/raw/

Don't ask questions, make reasonable choices.
```

### Validate Collected Data

```
Run validation on all collected tournament data:
1. Check all required fields are present
2. Verify height values are in range 155-220 cm
3. Flag any missing DOBs
4. Report verification rate (% with height_verified=true)
5. List all players with flags

Output a validation report.
```

---

## Example Prompts for Analysis

### Descriptive Statistics

```
Load all tournament data and create a summary table showing:
- Player count by category (WK, BAT, FAST, SPIN)
- Mean height ± SD for each category
- Height range (min-max) for each category
- % with verified heights
```

### Visualizations

```
Create a violin plot showing height distribution by category (WK, BAT, FAST, SPIN).
Use colorblind-friendly colors.
Save to figures/height_by_category.png at 300 DPI.
```

```
Create a line plot showing mean BAT height trend from 1975-2024 with:
- Points for each tournament
- Linear regression line
- 95% confidence band
- Annotation showing slope and p-value

Save to figures/bat_temporal_trend.png
```

```
Create a 4-panel publication figure showing:
A) Height distribution by category (violin)
B) Temporal trend for BAT and FAST
C) Country comparison (bar chart)
D) ODI vs T20 comparison (2007-2024)

Save to figures/main_figure.png at 300 DPI.
```

### Statistical Analysis

```
Run the population-adjusted regression analysis:
1. Load all player data with population height matched
2. Fit model: Height ~ Year + PopHeight for BAT category
3. Report unadjusted and adjusted slopes with 95% CI
4. Calculate attenuation ratio
5. Test for 2007 breakpoint using Chow test

Output results as a formatted table.
```

```
Run ANOVA: Height ~ Category + Era + Category×Era
Report F-statistics, p-values, and partial eta-squared.
Create a forest plot of effect sizes.
```

### Country Analysis

```
For each of the 8 countries, calculate:
1. Mean height by category
2. Temporal slope (unadjusted)
3. Population-adjusted slope
4. Excess over 48 years

Create a summary table ranked by adjusted slope.
Highlight which countries show significant selection effects.
```

---

## Example Prompts for Paper Updates

### Update a Section

```
Update Section 3.4 (Country-Wise Analysis) with the actual data collected.
Replace placeholder statistics with real values.
Ensure all 95% CIs are reported.
Maintain consistent decimal places (2 for coefficients, 3 for p-values).
```

### Generate a Table

```
Create a formatted markdown table for Table 5 (Country-Wise Height Trends)
with columns: Nation, Mean Height, Unadjusted β, Adjusted β, p-value, 48-year Excess

Use the actual data from the analysis.
```

### Create Figure Captions

```
Write publication-quality captions for all figures in the figures/ folder.
Include sample sizes, statistical tests, and interpretation hints.
```

---

## Project Structure

```
cricket-research/
├── CLAUDE.md                 # Main project context (read by Claude Code)
├── README.md                 # This file
├── data/
│   ├── raw/                  # Tournament JSONs (one per tournament)
│   │   ├── odi-1975.json
│   │   ├── ...
│   │   └── t20-2026.json
│   ├── processed/            # Merged datasets
│   │   ├── all_players.csv
│   │   └── all_players.parquet
│   └── external/
│       └── population_heights.csv
├── scripts/
│   ├── validate_data.py
│   ├── merge_tournaments.py
│   ├── run_analysis.py
│   └── generate_figures.py
├── figures/                  # Generated visualizations
├── paper/
│   └── cricket_paper.md
└── docs/
    ├── SAMPLING_METHODOLOGY_v3.md
    ├── POWER_HITTING_HYPOTHESIS.md
    ├── TOURNAMENT_INDEX.md
    └── VISUALIZATION_CATALOG.md
```

---

## Player Categories

| Category | Code | Description | Expected Height |
|----------|------|-------------|-----------------|
| Wicketkeeper | `WK` | Primary keeper | Medium |
| Top-Order Batsman | `BAT` | Batting positions 1-6 | Medium-Tall |
| Fast Bowler | `FAST` | Pace bowlers (positions 7-11) | Tall |
| Spin Bowler | `SPIN` | Spin bowlers (positions 7-11) | Variable |

---

## Data Quality Flags

| Flag | When to Use | Notes Required? |
|------|-------------|-----------------|
| `HEIGHT_ESTIMATED` | Height from photos only | Yes - explain method |
| `HEIGHT_CONFLICTING` | Sources disagree | Yes - list values |
| `DOB_ESTIMATED` | Birth year guessed | Yes - explain |
| `DOB_UNKNOWN` | No DOB available | Yes - use tournament-27 |
| `CATEGORY_AMBIGUOUS` | All-rounder edge case | Yes - explain choice |
| `LIMITED_APPEARANCES` | <3 tournament matches | Optional |

---

## Key Commands

```bash
# Validate all data
python scripts/validate_data.py data/raw/*.json

# Merge tournaments
python scripts/merge_tournaments.py

# Run full analysis
python scripts/run_analysis.py

# Generate all figures
python scripts/generate_figures.py
```

---

## Dependencies

```bash
pip install pandas numpy scipy statsmodels matplotlib seaborn pingouin pyarrow
```

---

*Last Updated: 2025-02-15*
