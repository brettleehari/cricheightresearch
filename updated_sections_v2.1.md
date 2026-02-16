# Cricket Paper v2.1 - Updated Sections

## Changes Applied

1. ✅ Section 1.3: Reframed hypothesis around format trends (Test→ODI→T20) and power hitting
2. ✅ Section 1.4: Added objective (6) for country-specific trends
3. ✅ Section 2.1: 11-player snapshot methodology
4. ✅ Section 2.3: Birth year as explicit data field
5. ✅ Section 2.5: Python-based analysis

---

## SECTION 1.3 (REVISED)

### 1.3 Theoretical Framework: Format Evolution and Physical Selection

Cricket's evolution across formats provides a natural experiment for testing selection pressure hypotheses. The progression from Test cricket (unlimited overs, played over 5 days) to ODI cricket (50 overs, single day) to T20 cricket (20 overs, ~3 hours) has progressively intensified the premium on scoring rate and boundary-hitting capability. This format evolution generates testable predictions about anthropometric selection.

**The Power-Hitting Hypothesis**

We propose that cricket's format evolution has created increasing selection pressure for taller, more powerful batsmen:

1. **Test Cricket (Traditional):** Success depends primarily on technique, concentration, and ability to bat for extended periods. Height provides limited advantage; shorter batsmen with superior technique (Tendulkar, Gavaskar, Bradman) have historically excelled.

2. **ODI Cricket (Transitional):** The 50-over format introduced time pressure, rewarding batsmen who can score quickly while building innings. The introduction of powerplays (2003) created specific phases where boundary-hitting is incentivized.

3. **T20 Cricket (Power Era):** The 20-over format places maximum premium on strike rate and boundary percentage. Biomechanically, taller batsmen possess longer lever arms, generating greater bat-head speed and enabling reach advantages for power shots. Six-hitting—the signature T20 skill—rewards the force generation that height facilitates.

**Hypothesis 1 (Format Gradient):** Height selection pressure follows the format gradient:
```
T20 > ODI > Test (predicted selection pressure intensity)
```

**Hypothesis 2 (Temporal Acceleration):** Height selection pressure should accelerate after format introduction milestones:
- Post-1975: ODI World Cup era begins
- Post-2003: Powerplay introduction in ODIs
- Post-2007: T20 World Cup era begins
- Post-2008: IPL professionalization

**Hypothesis 3 (Predictive):** If power-hitting creates genuine selection pressure, cricket height trends should:
- **Exceed** birth-cohort population increases in respective national teams
- Show **format-specific** effects (T20 squads taller than contemporary ODI squads)
- Demonstrate **position-specific** patterns (batsmen showing T20-era acceleration; spinners showing no trend)

**Competing Null Hypothesis**

The alternative explanation remains that observed height increases simply reflect:
- General population growth due to improved nutrition/healthcare
- No sport-specific selection beyond demographic effects
- Height-independent success factors (technique, decision-making, fitness)

Under this null hypothesis, cricket heights should track population trends with no statistically significant excess, and no format-specific differentiation should emerge.

---

## SECTION 1.4 (REVISED)

### 1.4 Research Objectives

This study aims to:

1. **Document temporal evolution** of batsman and bowler heights across 48 years of ICC World Cup cricket, spanning both ODI (1975-2023) and T20 (2007-2024) formats.

2. **Compare cricket trajectories against birth-cohort-matched population norms** using WHO and NCD-RisC data, with player birth years explicitly recorded to enable precise cohort matching.

3. **Quantify excess height increase** attributable to sport-specific selection pressure, distinguishing genuine selection from demographic artifacts.

4. **Test format-specific effects** by comparing T20 World Cup squads against ODI World Cup squads in overlapping years (2007-2023).

5. **Identify structural breakpoints** where selection dynamics shifted, testing whether format introductions (powerplays, T20) created measurable inflections.

6. **Analyze country-specific trends** to determine whether selection pressure operates uniformly across cricket's diverse geographical landscape, or whether nations differ systematically in their anthropometric selection patterns.

7. **Examine position-specific selection** across batting positions (openers, middle order, wicketkeepers), bowling types (fast bowlers, spinners), and all-rounders.

**Predictive Objective:** Beyond describing historical patterns, this study aims to generate falsifiable predictions. If the power-hitting hypothesis is correct, we predict that:
- Future T20 squads will continue to exceed population height trends
- The height gap between T20 specialists and population norms will widen
- Nations that prioritize power-hitting (Australia, England) will show stronger selection effects than technique-focused traditions (India, Sri Lanka)

---

## SECTION 2.1 (REVISED)

### 2.1 Study Design

This study employs a repeated cross-sectional design with **structured position-based sampling**. Rather than analyzing all squad members, we select a **standardized 11-player snapshot** from each nation for each ICC World Cup tournament, enabling consistent cross-temporal and cross-national comparison.

**Tournament Coverage**

- **ODI World Cups:** All 13 tournaments (1975, 1979, 1983, 1987, 1992, 1996, 1999, 2003, 2007, 2011, 2015, 2019, 2023)
- **T20 World Cups:** All 9 tournaments (2007, 2009, 2010, 2012, 2014, 2016, 2021, 2022, 2024)
- **Future (optional):** 2026 T20 World Cup for validation

**11-Player Snapshot Structure**

For each nation in each tournament, we select players filling these position slots:

| Slot | Position Category | Count | Selection Criteria |
|------|-------------------|-------|-------------------|
| 1-2 | Opening Batsmen | 2 | Batted at #1 or #2 in ≥50% of tournament matches |
| 3-4 | Middle Order Batsmen | 2 | Batted at #3-5 in ≥50% of matches; highest tournament average |
| 5 | Wicketkeeper-Batsman | 1 | Primary keeper (most dismissals in tournament) |
| 6 | Batting All-rounder | 1 | Batting avg > bowling avg; bats in top 7 |
| 7 | Bowling All-rounder | 1 | Bowling avg < batting avg; regular bowler |
| 8-9 | Fast Bowlers | 2 | Pace bowlers; top 2 by wickets taken |
| 10 | Spin Bowler | 1 | Primary spinner; highest wickets among spinners |
| 11 | Support Bowler | 1 | Third-choice pace or second spinner |

**Rationale for Structured Sampling**

This approach offers several advantages over all-squad analysis:

1. **Consistency:** Every nation-tournament observation has exactly 11 players, enabling direct comparison.
2. **Position control:** Analysis can examine position-specific trends (e.g., "Do openers show stronger selection pressure than spinners?").
3. **Reduced noise:** Excludes fringe squad members who may not represent selection priorities.
4. **Replicability:** Clear inclusion rules enable independent verification.

**Tie-Breaking Rules**

When multiple players qualify for a slot:
1. Most matches played in tournament
2. If tied: higher batting/bowling average in tournament
3. If still tied: alphabetical by surname

---

## SECTION 2.3 (REVISED)

### 2.3 Data Sources

**2.3.1 Anthropometric Data**

Player heights were extracted from ESPN Cricinfo player profiles (accessed November-December 2024). Heights were recorded in centimeters; imperial measurements were converted using the standard factor (1 inch = 2.54 cm). Heights were cross-validated against ICC official match records and Wisden Cricketers' Almanack entries.

A four-level verification system was applied:
- **Level 1 (ICC_official):** Height from official ICC tournament records
- **Level 2 (ESPN_verified):** ESPN Cricinfo with corroborating secondary source
- **Level 3 (single_source):** Single reliable source only
- **Level 4 (estimated):** Estimated from photographs; flagged for sensitivity analysis

**2.3.2 Population Height Data**

Birth-cohort-matched population height norms were obtained from:

1. **NCD Risk Factor Collaboration (NCD-RisC, 2016):** Modeled estimates of mean adult male height by country and birth year for 1950-2000.
2. **WHO Global Health Observatory (2023):** Age-sex-standardized height estimates by nation.

**2.3.3 Birth Year Data (Explicit Collection)**

Unlike previous studies that estimated birth years from tournament year minus median age, this study **explicitly collects date of birth** for each player:

| Field | Description | Source |
|-------|-------------|--------|
| `date_of_birth` | Full DOB (YYYY-MM-DD) | ESPN Cricinfo, ICC records |
| `birth_year` | Extracted year | Derived from DOB |
| `age_at_tournament` | Age in years at tournament start | Calculated |

For players with unknown DOB (primarily early tournaments), birth year was estimated as:
```
birth_year_estimated = tournament_year - 27 (median career age)
```
These cases are flagged with `birth_year_known = False` and excluded in sensitivity analysis.

**Birth Cohort Matching Process**

For each player, population height is matched as follows:

```python
def match_population_height(player_birth_year, player_nation):
    """
    Match player to birth-cohort population norm.
    
    Returns WHO/NCD-RisC mean height for:
    - Males
    - Born in player_birth_year
    - From player_nation
    """
    return ncd_risc_data.query(
        f"country == '{player_nation}' and birth_year == {player_birth_year}"
    )['mean_height_cm'].values[0]
```

This explicit birth-year matching enables precise population control rather than aggregate estimates.

---

## SECTION 2.5 (REVISED)

### 2.5 Statistical Analysis

All analyses were conducted in **Python 3.11** using the following packages:

**Core Dependencies**
```python
pandas>=2.0.0        # Data manipulation
numpy>=1.24.0        # Numerical computing
scipy>=1.10.0        # Statistical tests
statsmodels>=0.14.0  # Regression modeling
pingouin>=0.5.3      # Effect sizes, ANOVA
```

**Visualization**
```python
matplotlib>=3.7.0    # Base plotting
seaborn>=0.12.0      # Statistical visualization
```

**Advanced Modeling**
```python
scikit-learn>=1.3.0  # Machine learning utilities
pymer4>=0.8.0        # Mixed-effects models (R lme4 wrapper)
```

**2.5.1 Descriptive Statistics**

```python
import pandas as pd
import pingouin as pg

# Summary statistics by position, era, nation
descriptives = df.groupby(['position_category', 'era', 'nation']).agg({
    'height_cm': ['count', 'mean', 'std', 'min', 'max'],
    'age_at_tournament': 'mean'
}).reset_index()

# 95% confidence intervals
ci = pg.compute_bootci(df['height_cm'], func='mean', n_boot=10000)
```

**2.5.2 Temporal Trend Analysis**

```python
import statsmodels.api as sm

# Model 1: Unadjusted (Height ~ Year)
X = sm.add_constant(df['tournament_year'])
model1 = sm.OLS(df['height_cm'], X).fit()

# Model 2: Population-adjusted (Height ~ Year + PopHeight)
X_adj = sm.add_constant(df[['tournament_year', 'pop_height_birth_cohort']])
model2 = sm.OLS(df['height_cm'], X_adj).fit()

# Attenuation ratio
attenuation = model2.params['tournament_year'] / model1.params['tournament_year']
```

**2.5.3 Segmented Regression (Breakpoint Detection)**

```python
import numpy as np
from scipy.optimize import minimize

def segmented_regression(X, y, breakpoint):
    """Piecewise linear regression with single breakpoint."""
    X1 = X.copy()
    X2 = np.maximum(0, X - breakpoint)
    design = np.column_stack([np.ones_like(X), X1, X2])
    betas, residuals, _, _ = np.linalg.lstsq(design, y, rcond=None)
    return betas, residuals.sum()

# Grid search for optimal breakpoint
breakpoints = df['tournament_year'].unique()
results = {bp: segmented_regression(df['tournament_year'], df['height_cm'], bp) 
           for bp in breakpoints}
optimal_breakpoint = min(results, key=lambda x: results[x][1])

# Chow test for structural break
from scipy.stats import f as f_dist
# ... implementation
```

**2.5.4 Two-Way ANOVA**

```python
import pingouin as pg

# Position × Era ANOVA
anova_results = pg.anova(
    data=df,
    dv='height_cm',
    between=['position_category', 'era'],
    detailed=True
)

# Effect sizes (partial eta-squared)
eta_squared = anova_results['np2']

# Post-hoc Tukey HSD
posthoc = pg.pairwise_tukey(data=df, dv='height_cm', between='era')
```

**2.5.5 Mixed-Effects Modeling**

```python
from pymer4.models import Lmer

# Height ~ Position + Era + PopHeight + (1|Nation)
model = Lmer(
    'height_cm ~ position_category + era + pop_height_birth_cohort + (1|nation)',
    data=df
)
results = model.fit()

# Intraclass correlation
icc = model.ranef_var / (model.ranef_var + model.residual_var)
```

**2.5.6 Format Comparison (ODI vs T20)**

```python
# Filter to overlapping years (2007-2023)
overlap_df = df[(df['tournament_year'] >= 2007) & (df['tournament_format'].isin(['ODI', 'T20I']))]

# T-test: T20 vs ODI heights
from scipy.stats import ttest_ind, cohen_d

t20_heights = overlap_df[overlap_df['tournament_format'] == 'T20I']['height_cm']
odi_heights = overlap_df[overlap_df['tournament_format'] == 'ODI']['height_cm']

t_stat, p_value = ttest_ind(t20_heights, odi_heights)
effect_size = pg.compute_effsize(t20_heights, odi_heights, eftype='cohen')
```

**2.5.7 Country-Specific Analysis**

```python
# Separate regressions by nation
country_results = {}
for nation in df['nation'].unique():
    nation_df = df[df['nation'] == nation]
    
    # Unadjusted model
    X = sm.add_constant(nation_df['tournament_year'])
    model_unadj = sm.OLS(nation_df['height_cm'], X).fit()
    
    # Adjusted model
    X_adj = sm.add_constant(nation_df[['tournament_year', 'pop_height_birth_cohort']])
    model_adj = sm.OLS(nation_df['height_cm'], X_adj).fit()
    
    country_results[nation] = {
        'n': len(nation_df),
        'mean_height': nation_df['height_cm'].mean(),
        'slope_unadjusted': model_unadj.params['tournament_year'],
        'slope_adjusted': model_adj.params['tournament_year'],
        'p_adjusted': model_adj.pvalues['tournament_year'],
        'excess_48y': model_adj.params['tournament_year'] * 48
    }
```

**2.5.8 Sensitivity Analyses**

Four pre-registered robustness checks:

1. **Verified heights only:** Exclude Level 3-4 heights
2. **Known birth years only:** Exclude estimated DOBs
3. **Alternative position classification:** Slot reassignment test
4. **Age-offset sensitivity:** ±3 years for cohort matching

---

## Summary of Changes

| Section | Original | Updated |
|---------|----------|---------|
| 1.3 Hypothesis | Generic selection pressure | Format-specific (Test→ODI→T20) with power-hitting mechanism |
| 1.3 Prediction | Observational only | Predictive: heights will exceed birth cohort trends |
| 1.4 Objectives | 5 objectives | 6 objectives (added country-specific) |
| 2.1 Design | All squad members | 11-player snapshot with position slots |
| 2.1 Coverage | ODI only | ODI + T20 World Cups (1975-2024) |
| 2.3 Birth data | Estimated from median age | Explicit DOB collection |
| 2.5 Software | R | Python 3.11 |

---

*Document Version: 2.1*
*Last Updated: 2025-02-15*
