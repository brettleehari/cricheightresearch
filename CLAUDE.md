# Cricket Anthropometric Research - Claude Code Project

## Project Goal

Build a comprehensive dataset of cricket player heights across all 23 ICC World Cups (1975-2026), analyze temporal trends, and test whether cricket shows sport-specific height selection pressure beyond population demographics.

## Core Deliverables

### 1. Raw Data Collection
Create JSON files for each of 23 World Cups containing Playing XI for 8 nations with:
- All players categorized into **4 categories**
- Height data with verification flags
- Date of birth for birth-cohort matching
- Notes explaining any data quality issues

### 2. Analysis Pipeline
Python scripts to:
- Validate and merge raw data
- Match players to population height norms
- Run statistical analyses
- Generate publication-quality visualizations

### 3. Research Paper
Updated manuscript incorporating findings with country-wise and regional analysis.

---

## Player Categories (4 Types)

Every player in a Playing XI falls into exactly ONE category:

| Category | Code | Batting Position | Description |
|----------|------|------------------|-------------|
| **Wicketkeeper** | `WK` | Any (usually 5-7) | Primary keeper; exactly 1 per team |
| **Top-Order Batsman** | `BAT` | 1-6 | First six batting positions |
| **Fast Bowler** | `FAST` | 7-11 | Pace, seam, swing bowlers |
| **Spin Bowler** | `SPIN` | 7-11 | Off-spin, leg-spin, left-arm orthodox |

### Classification Rules
```python
def classify_player(player):
    if player.is_wicketkeeper:
        return "WK"
    elif player.modal_batting_position <= 6:
        return "BAT"
    elif player.bowling_style in ["fast", "fast-medium", "medium-fast", "medium"]:
        return "FAST"
    else:  # spin bowler
        return "SPIN"
```

---

## Data Schema

### Player Record

```python
{
    "player_id": "v-kohli-1",           # Unique ID
    "full_name": "Virat Kohli",
    "country": "IND",                    # ISO 3166-1 alpha-3
    "category": "BAT",                   # WK | BAT | FAST | SPIN
    
    # Biographical
    "date_of_birth": "1988-11-05",       # YYYY-MM-DD
    "birth_year": 1988,
    
    # Anthropometric
    "height_cm": 175.0,
    "height_verified": True,             # KEY FLAG
    "height_source": "ESPN_verified",
    
    # Tournament appearances
    "world_cups": [
        {"tournament_id": "odi-2011", "batting_position": 3},
        {"tournament_id": "odi-2015", "batting_position": 3},
        {"tournament_id": "odi-2019", "batting_position": 3},
        {"tournament_id": "odi-2023", "batting_position": 3},
        {"tournament_id": "t20-2012", "batting_position": 3},
        {"tournament_id": "t20-2014", "batting_position": 3},
        {"tournament_id": "t20-2016", "batting_position": 3},
        {"tournament_id": "t20-2021", "batting_position": 3},
        {"tournament_id": "t20-2022", "batting_position": 3},
        {"tournament_id": "t20-2024", "batting_position": 3}
    ],
    
    # Data quality
    "flag": null,                        # See flag values below
    "notes": ""                          # Explanation if flag is not null
}
```

### Flag Values

| Flag | Meaning | Required Notes |
|------|---------|----------------|
| `null` | Data verified, no issues | None |
| `HEIGHT_ESTIMATED` | Height estimated from photos | Explain estimation method |
| `HEIGHT_CONFLICTING` | Sources disagree on height | List conflicting values |
| `DOB_ESTIMATED` | Birth year estimated | Explain estimation |
| `DOB_UNKNOWN` | DOB completely unknown | Use tournament year - 27 |
| `CATEGORY_AMBIGUOUS` | Role unclear (all-rounder) | Explain classification choice |
| `LIMITED_APPEARANCES` | <3 matches in tournament | May not represent "best XI" |

---

## Tournament Coverage

### 23 World Cups

**ODI World Cups (13):** 1975, 1979, 1983, 1987, 1992, 1996, 1999, 2003, 2007, 2011, 2015, 2019, 2023

**T20 World Cups (10):** 2007, 2009, 2010, 2012, 2014, 2016, 2021, 2022, 2024, 2026

### 8 Nations
`AUS`, `ENG`, `IND`, `PAK`, `WI`, `NZL`, `SL`, `RSA`

*Note: South Africa excluded 1975-1991 (apartheid ban)*

---

## Data Collection Workflow

### Step 1: For Each Tournament
```
1. Identify most common Playing XI for each nation
2. For each of 11 players:
   a. Look up height on ESPN Cricinfo
   b. Cross-validate with secondary source (ICC, Wisden)
   c. Look up DOB
   d. Determine category based on batting position + bowling style
   e. Set height_verified = True if 2+ sources agree
   f. Add flag + notes if any data quality issues
```

### Step 2: Validation
```bash
python scripts/validate_data.py data/raw/*.json
```

### Step 3: Merge & Analysis
```bash
python scripts/merge_all_tournaments.py
python scripts/run_analysis.py
```

---

## Key Research Questions

1. **Do cricket heights exceed population trends?**
   - Compare player heights vs birth-cohort-matched population norms

2. **Is there a T20 effect?**
   - Compare T20 WC vs ODI WC heights in overlapping years

3. **Which categories show strongest selection?**
   - Expected: FAST > BAT > WK ≈ SPIN

4. **Which countries show strongest selection?**
   - Expected: AUS/ENG > IND/SL

5. **Is there a 2007 breakpoint?**
   - Test if selection accelerated after T20 emergence

---

## Power Hitting Hypothesis

**Definition:** Power hitting = high strike rate (≥130) + high boundary % (≥60%)

**Prediction:** As cricket evolves toward power hitting, TOP_ORDER_BATSMAN heights will:
1. Exceed population trends (✓ if adjusted β > 0)
2. Accelerate post-2007 (✓ if breakpoint detected)
3. Be higher in T20 than ODI (✓ if format effect significant)

---

## File Structure

```
cricket-research/
├── .claude/
│   └── CLAUDE.md              # This file
├── data/
│   ├── raw/                   # One JSON per tournament
│   │   ├── odi-1975.json
│   │   ├── odi-2023.json
│   │   ├── t20-2007.json
│   │   └── ...
│   ├── processed/
│   │   ├── all_players.csv    # Merged dataset
│   │   └── all_players.parquet
│   └── external/
│       └── population_heights.csv  # NCD-RisC/WHO data
├── scripts/
│   ├── validate_data.py
│   ├── merge_all_tournaments.py
│   ├── match_population.py
│   ├── run_analysis.py
│   └── generate_figures.py
├── notebooks/
│   └── exploratory_analysis.ipynb
├── figures/
│   └── (generated PNG/PDF files)
├── paper/
│   └── cricket_paper.md
└── README.md
```

---

## Common Tasks

### Collect Data for a Tournament
```
Prompt: "Create the raw data JSON for the 2023 ODI World Cup India team. 
Look up heights and DOBs for each player in the Playing XI. 
Set height_verified=True only if you can confirm from multiple sources.
Add notes explaining any data quality issues."
```

### Validate All Data
```bash
python scripts/validate_data.py data/raw/*.json --strict
```

### Generate a Visualization
```
Prompt: "Create a violin plot showing height distribution by category 
(WK, BAT, FAST, SPIN) across all tournaments."
```

### Run Statistical Analysis
```
Prompt: "Run the population-adjusted regression for TOP_ORDER_BATSMAN 
heights and report the adjusted slope with 95% CI."
```

---

## Pre-Allowed Commands

Safe to run without confirmation:
- `cat`, `ls`, `head`, `tail`, `wc`, `grep`, `find`
- `python scripts/*.py`
- `pip install pandas numpy scipy matplotlib seaborn`
- `git status`, `git add`, `git commit`

---

## Key Statistics to Maintain

When updating the paper, preserve these validated findings:
- Sample: n=782 players (480 BAT, 302 bowlers) [UPDATE after data collection]
- Unadjusted batsman trend: β = 0.104 cm/year
- Population-adjusted trend: β = 0.043 cm/year
- Attenuation: 59% demographic, 41% sport-specific
- Breakpoint: 2003 (Chow test p = .031)
- Position effect: FAST 4.8 cm > BAT (d = 0.82-0.86)

---

## Decision Rules

When data is ambiguous:
1. **Height conflicts:** Use ESPN Cricinfo as primary; note conflict
2. **DOB unknown:** Estimate as tournament_year - 27; flag as DOB_ESTIMATED
3. **Category unclear:** Use modal batting position; if truly ambiguous, flag
4. **Player didn't play:** Include if in "best XI"; flag as LIMITED_APPEARANCES

---

*Version: 3.0 | Last Updated: 2025-02-15*
