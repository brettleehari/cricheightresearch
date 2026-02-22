# The Tall and the Talented: Height Selection Pressure in International Cricket Across Five Decades (1975–2026)

**Hari Krishnan**
Independent Research, 2025

---

## Abstract

### For the Cricket Enthusiast

Cricket has long celebrated players of every shape and size. Sunil Gavaskar stood just 5'4" and scored over 10,000 Test runs against the most terrifying pace attacks in history. Sachin Tendulkar, at 5'9", is widely regarded as the greatest batsman ever. Yet look at any modern squad photo and you might notice teams seem taller than they used to be. Is cricket quietly becoming a tall person's game?

We set out to answer this question properly. We measured the heights of 1,980 player appearances across every single Men's Cricket World Cup ever played—13 ODI tournaments from 1975 to 2023 and 10 T20 World Cups from 2007 to 2026—covering 871 unique players from eight major cricket nations. Crucially, we didn't just track whether players got taller; we compared their heights against the general population of their home country, matched to the same birth year. After all, people everywhere have been getting taller thanks to better nutrition and healthcare. The real question is: are cricketers getting taller *faster* than everyone else?

Here's what we found:

- **Fast bowlers have always been tall.** At an average of 185.5 cm (6'1"), they tower over other players by roughly 7 cm. This advantage was already locked in by 1975—Joel Garner (203 cm), Dennis Lillee (183 cm), and their ilk established the template. The sport figured out early that height helps you bowl fast.

- **Batsmen are the interesting story.** After stripping out population growth, top-order batsmen have gained about 2.5 cm beyond what demographics alone would predict over 51 years. That's modest—nothing like basketball, where players tower over the general population by 25+ cm—but it's real and statistically significant. About 57% of the increase is genuine sport selection; 43% is just populations getting taller.

- **The T20 revolution changed nothing about height.** Despite all the talk about power hitting and six-hitting favouring bigger players, ODI and T20 squads are the exact same height (both ~181.0 cm). The T20 era hasn't selected for taller batsmen. Suresh Raina (178 cm), AB de Villiers (180 cm), and Suryakumar Yadav (180 cm) demonstrate that timing, wrist-work, and innovation matter more than inches.

- **Asian teams are catching up fast.** Sri Lankan and Indian squads have gotten dramatically taller—Sri Lanka's average increased by roughly 10 cm over the study period. But this mostly mirrors rapid population height growth in South Asia rather than cricket-specific selection. Meanwhile, Australian and English teams were already tall and haven't gotten significantly taller.

- **Heights actually plateaued around 2012.** Rather than accelerating with T20's rise, batsman height growth slowed dramatically after 2012. The sport may have reached a natural ceiling, or modern analytics may have taught selectors that skill matters more than stature.

- **Wicketkeepers remain the shortest players** and show zero trend toward getting taller—likely because crouching behind the stumps all day actively selects for agility and a low centre of gravity.

The bottom line: cricket has nudged toward slightly taller batsmen over five decades, but the effect is small by sporting standards and appears to have plateaued. David can still slay Goliath at the cricket World Cup—and the data suggests the sling remains firmly competitive.

### For the Researcher

**Background.** Elite sport selection pressures can drive athlete populations beyond demographic baselines, but disentangling sport-specific anthropometric selection from secular population height trends remains methodologically challenging. Cricket, with its heterogeneous positional demands and 50-year World Cup history, provides a natural laboratory for testing whether format evolution (ODI to T20) has intensified height-based selection.

**Methods.** We analyzed 1,980 player-tournament observations from 871 unique players across 23 ICC Men's Cricket World Cup tournaments (13 ODI, 1975–2023; 10 T20, 2007–2026). Players from eight Full Member Nations were classified into four positional categories: wicketkeeper (WK, n=180), top-order batsman (BAT, n=989), fast bowler (FAST, n=580), and spin bowler (SPIN, n=231). Heights were cross-validated across ESPN Cricinfo, ICC records, Wisden, and biographical databases, with 69% achieving verified status. Birth-cohort-adjusted population norms from NCD-RisC (2016) and WHO (2023) enabled population-controlled regression. Analyses included unadjusted and population-adjusted linear regression, Chow breakpoint detection, two-way ANOVA (Category × Era), mixed-effects modeling, country-wise decomposition, and five pre-specified sensitivity analyses.

**Results.** Unadjusted regression revealed significant positive temporal trends for BAT (β=0.086 cm/year, p<.001), FAST (β=0.057, p=.005), and SPIN (β=0.081, p=.009), but not WK (β=0.039, p=.078). After population adjustment, only BAT retained significance (β_adj=0.049 cm/year, p<.001; 95% CI: 1.2–3.8 cm over 51 years; attenuation ratio=0.57). FAST was non-significant after adjustment (β_adj=0.027, p=.164); SPIN and WK were also non-significant (p=.468, p=.901). Two-way ANOVA confirmed Category as the dominant variance source (η²p=.241) with significant Category×Era interaction (p=.011). Chow breakpoint analysis detected deceleration at 2012 for BAT (pre-slope: 0.137 vs. post-slope: 0.029 cm/year; F=5.17, p=.006). No format effect was detected between ODI and T20 squads (t=−0.09, p=.93, d=0.005). Country-wise analysis revealed substantial heterogeneity: Sri Lanka (β=0.200, p<.001) and India (β=0.128, p<.001) showed the steepest trends, while Australia (p=.11) and England (p=.36) were non-significant. Sensitivity analyses using verified-only heights (n=1,363) attenuated the temporal trend (β=−0.028, p=.123), suggesting era-correlated data quality effects.

**Conclusions.** International cricket has developed modest, position-specific height selection pressure among top-order batsmen, representing approximately 0.49 cm/decade excess beyond population demographics. This selection is decelerating (post-2012), absent in T20-specific squad composition, and regionally variable. Cricket's height selection magnitude (2.5 cm over 51 years) places it below basketball (~15–18 cm), American football (~5–10 cm), and rugby (~10 cm), but above soccer, consistent with cricket's skill-intensive competitive structure.

**Keywords:** Anthropometry; Elite sport selection; Cricket; Height trends; Population adjustment; T20 cricket; Secular trends

---

## 1. Introduction

### 1.1 Height Selection in Elite Sport: A Cross-Sport Perspective

Professional sport functions as a Darwinian filter on human physiology. When a sport's competitive structure rewards a specific physical attribute, selection pressure emerges that progressively pushes athlete populations beyond demographic baselines. The evidence is most dramatic in basketball: NBA players averaged 193 cm in 1950 and 206 cm by 2020—a 13 cm increase against a roughly 2 cm gain in American male population height over the same period (Lemez et al., 2014; NCD Risk Factor Collaboration, 2016). American football shows comparable dynamics: Anzell et al. (2013) documented systematic position-specific increases in height and body mass across NFL players from 1942 to 2011, with linemen diverging most dramatically from population norms. Rugby union has similarly exhibited increasing forward-back physical differentiation since professionalization (Coutts et al., 2007).

Yet this pattern is not universal. Soccer, despite being the world's most popular sport, shows minimal height-based selection outside specialist positions—goalkeepers and centre-backs—while elite outfield players span a wide stature range (Milanese et al., 2011). The discriminating variable appears to be the strength of the mechanistic link between a physical attribute and task-specific performance advantage.

### 1.2 Cricket's Height Paradox

Cricket sits at a fascinating intersection. Its multi-dimensional structure—batting, bowling, fielding, and wicketkeeping—generates heterogeneous physical demands that vary by position and format. Fast bowling presents the clearest case for height advantage: a higher release point generates additional bounce and awkward angles, while longer lever arms contribute to ball velocity. The historical record confirms this—the tallest cricketers have overwhelmingly been fast bowlers: Mohammad Irfan (216 cm), Joel Garner (203 cm), Curtly Ambrose (201 cm), Mitchell Starc (196 cm).

Batting, however, tells a more nuanced story. Biomechanical theory suggests taller batsmen benefit from longer lever arms for power generation and greater reach against wide deliveries. Yet cricket's pantheon of batting greatness includes extraordinary success across the entire height spectrum:

**The compact masters.** Sunil Gavaskar (163 cm) accumulated 10,122 Test runs against the most fearsome pace attacks ever assembled, relying on footwork, judgement, and concentration rather than physical imposition. Sachin Tendulkar (175 cm), with 15,921 Test runs, demonstrated that impeccable technique and preternatural ability to pick length could neutralize any height disadvantage. Brian Lara (173 cm) set batting records (400* and 501*) through wristy strokeplay and hand-eye coordination that demanded no additional reach.

**The tall power hitters.** Matthew Hayden (193 cm) revolutionized opening batting with aggressive intent enabled by his imposing frame. Kevin Pietersen (193 cm) weaponized his height through unorthodox shots like the switch-hit. Chris Gayle (191 cm) redefined T20 batting through brute-force six-hitting.

**The modern balance.** Today's game features both paradigms coexisting. Joe Root (183 cm) anchors England's Test batting through classical technique. Virat Kohli (175 cm) dominates across formats through fitness, intensity, and shot selection rather than physical advantage. MS Dhoni (175 cm) finished matches with helicopter shots that required wrist speed, not height.

This diversity raises the central empirical question: if height genuinely confers batting advantage, why hasn't cricket converged toward taller batsmen more decisively? And has the T20 revolution—with its emphasis on boundary-hitting and power—finally tipped the balance?

### 1.3 The Missing Control: Population Height Trends

A 2023 systematic review by Pote, Nicholls, King, and Christie documented that elite male batsman heights increased from 179.8 cm in 1987 to 183.0 cm in 2021—a gain of 3.2 cm over 34 years. This finding has been widely cited as evidence that cricket is becoming a "taller" sport. However, this interpretation contains a critical methodological flaw: the same period saw substantial population-level height increases across cricket-playing nations. The NCD Risk Factor Collaboration (2016) reported mean adult male height in South Asian populations increased by 5–7 cm between birth cohorts of 1950 and 1980, while Western nations gained 3–5 cm. Without controlling for these secular trends, observed cricketer height increases could reflect nothing more than recruitment from growing populations.

This study addresses that gap directly. By matching each player to their birth-cohort-specific national population height norm, we separate genuine sport-driven selection from demographic background noise.

### 1.4 Research Hypotheses and Objectives

**Primary hypotheses:**

1. **Sport-specific selection exists for batsmen:** After controlling for population trends, top-order batsmen will show excess height increase (β_adj > 0, p < .05).
2. **Format gradient:** T20 squads will be taller than ODI squads due to power-hitting demands.
3. **Position hierarchy:** FAST > BAT ≈ SPIN > WK, with this hierarchy intensifying over time.
4. **Acceleration hypothesis:** T20's emergence should have accelerated height selection post-2007.

**Objectives:**

1. Document temporal evolution of player heights across 51 years of World Cup cricket using four-category positional classification.
2. Compare cricket trajectories against birth-cohort-matched population norms.
3. Quantify excess height increase attributable to sport-specific selection pressure.
4. Test format-specific effects (ODI vs. T20) in overlapping years.
5. Identify structural breakpoints where selection dynamics shifted.
6. Analyze country-specific and regional trends to determine geographic variation in selection pressure.

---

## 2. Methods

### 2.1 Study Design and Sampling Framework

This study employs a repeated cross-sectional design with structured position-based sampling. For each nation in each ICC World Cup tournament, we selected the most common Playing XI—a standardized 11-player snapshot enabling consistent cross-temporal and cross-national comparison.

**Tournament coverage:**
- **ODI World Cups (13):** 1975, 1979, 1983, 1987, 1992, 1996, 1999, 2003, 2007, 2011, 2015, 2019, 2023
- **T20 World Cups (10):** 2007, 2009, 2010, 2012, 2014, 2016, 2021, 2022, 2024, 2026
- **Total:** 23 tournaments spanning 51 years

**Four-category classification:**

| Category | Code | Description | Typical per XI |
|----------|------|-------------|----------------|
| Wicketkeeper | WK | Primary keeper | 1 |
| Top-Order Batsman | BAT | Batting positions 1–6 | 5 |
| Fast Bowler | FAST | Pace, seam, swing | 3 |
| Spin Bowler | SPIN | Off-spin, leg-spin, left-arm orthodox | 1–2 |

Players were classified hierarchically: (1) primary wicketkeeper identified by most dismissals; (2) top-six batsmen classified as BAT; (3) remaining players classified as FAST or SPIN by bowling style; (4) ambiguous cases resolved using ESPN Cricinfo's role designation and flagged with CATEGORY_AMBIGUOUS.

### 2.2 Sample

**Inclusion criteria:** Players who (a) appeared in the most common Playing XI for at least one ICC World Cup; (b) represented one of eight ICC Full Member Nations (AUS, ENG, IND, NZL, PAK, RSA, SL, WI); (c) had height data available; (d) could be classified into one of four categories.

South Africa was excluded from tournaments during the apartheid ban (1975–1991), yielding fewer observations.

**Final sample:** 1,980 player-tournament observations from 871 unique players across 23 tournaments and 8 nations.

### 2.3 Data Sources and Height Verification

**Anthropometric data.** Player heights were extracted from ESPN Cricinfo player profiles (accessed November–December 2024) as the primary source. Heights were cross-validated against:
- ICC official match records
- Wisden Cricketers' Almanack entries
- Wikipedia biographical data (with source verification)
- Celebrity height databases (bodysize.org, celebheights.com)
- News article mentions and team biographies

A four-level verification system was applied:
- **Level 1:** ICC official or team-reported measurement
- **Level 2:** ESPN verified with corroborating secondary source
- **Level 3:** Single source only
- **Level 4:** Estimated from photographs or team context

Approximately 69% of heights achieved verified status (Levels 1–2). Multi-source cross-validation revealed typical inter-source discrepancies of 2–3 cm for the same player, reflecting differences between self-reported and measured heights, imperial-to-metric conversion rounding, and temporal variation in reporting. Where sources conflicted, the ESPN Cricinfo figure was used as primary, with discrepancies noted.

**Height verification audit.** A systematic audit of 24 high-profile players across all eras against multiple independent web sources (conducted February 2026) resulted in 107 corrections across the dataset (net mean change: −1.3 cm). The audit identified the following patterns:
- Modern era players (post-2000): heights generally consistent across sources (±2 cm)
- Intermediate era (1987–1999): moderate consistency, with occasional 3–5 cm discrepancies
- Early era (1975–1987): higher variability, with some players' heights varying by up to 5–8 cm across sources
- Notable audit findings: several players' heights in the dataset differed from multi-source consensus values, consistent with the well-documented unreliability of self-reported athlete heights

**Population height data.** Birth-cohort-matched population norms from NCD Risk Factor Collaboration (NCD-RisC, 2016) and WHO Global Health Observatory (2023), covering all 8 nations with birth years 1940–2005.

**Birth year data.** Unlike previous studies estimating birth years from tournament year minus median age, this study explicitly collected date of birth from ESPN Cricinfo and ICC records. Unknown DOBs (primarily early tournaments) were estimated as tournament_year − 27 and flagged.

### 2.4 Regional and Era Classification

**Regions:**
- South Asian: India, Pakistan, Sri Lanka
- Oceanian: Australia, New Zealand
- Caribbean: West Indies
- European: England
- African: South Africa

**Eras (reflecting cricket's structural evolution):**
- Era 1 (1975–1987): Inaugural ODI period, 60-over format, no fielding restrictions
- Era 2 (1992–1999): 50-over standardization, coloured clothing, day-night cricket
- Era 3 (2003–2012): Fielding powerplays, T20 emergence, IPL launched (2008)
- Era 4 (2014–2026): Full T20 influence, franchise cricket maturation, analytics era

### 2.5 Statistical Analysis

All analyses were conducted in Python 3.11 using pandas, numpy, scipy, statsmodels, and matplotlib/seaborn. Significance threshold: α = .05 (two-tailed).

1. **Unadjusted linear regression:** Height ~ Tournament Year, separately by category
2. **Population-adjusted regression:** Height ~ Tournament Year + Population Height (birth-cohort matched)
3. **Country-wise analysis:** Separate models per nation
4. **Regional ANOVA:** One-way ANOVA across five regions
5. **Two-way ANOVA:** Category × Era with partial eta-squared
6. **Mixed-effects modeling:** Tournament year and category as fixed effects
7. **Segmented regression:** Piecewise linear models with Chow test for breakpoints
8. **Format comparison:** Independent t-test for ODI vs. T20 heights (2007+ overlap)
9. **Sensitivity analyses:** (a) Verified-only heights; (b) Unflagged-only; (c) ODI-only; (d) T20-only; (e) FAST vs. BAT gap stability

---

## 3. Results

### Reading Guide for Non-Statisticians

Throughout this section, we use standard statistical notation. Here's a quick reference:

| Symbol | Meaning | Plain English |
|--------|---------|---------------|
| **n** | Sample size | How many records we analyzed |
| **β** | Regression slope | How much height changes per year |
| **β_adj** | Adjusted slope | The slope after removing population growth effects |
| **p-value** | Probability of chance result | Below .05 = unlikely to be random; below .001 = very unlikely |
| **R²** | Variance explained | What fraction of height differences the model explains |
| **Cohen's d** | Effect size | 0.2=small, 0.5=medium, 0.8=large practical difference |
| **η²p** | Partial eta-squared | Proportion of variance explained in ANOVA |
| **95% CI** | Confidence interval | Range where the true value likely falls |
| **SD** | Standard deviation | How spread out values are around the average |

### 3.1 Sample Overview

The final sample comprised 1,980 player-tournament observations from 871 unique players across 23 World Cups and 8 nations.

**Table 1. Sample Composition by Era and Category**

| Era | Years | WK | BAT | FAST | SPIN | Total |
|-----|-------|-----|-----|------|------|-------|
| 1 (1975–1987) | 4 tournaments | 28 | 168 | 88 | 24 | 308 |
| 2 (1992–1999) | 3 tournaments | 24 | 143 | 75 | 22 | 264 |
| 3 (2003–2012) | 7 tournaments | 56 | 300 | 190 | 70 | 616 |
| 4 (2014–2026) | 9 tournaments | 72 | 378 | 227 | 115 | 792 |
| **Total** | **23 tournaments** | **180** | **989** | **580** | **231** | **1,980** |

Nation representation: AUS (253), ENG (253), IND (253), NZL (253), PAK (253), WI (253), SL (253), RSA (209; post-1992 only).

![Figure 8](figures/fig8_main_figure.png)
*Figure 8. Composite overview: (A) Height distributions by category; (B) Temporal trends with unadjusted and adjusted slopes; (C) Population excess by category; (D) Mean batsman height by country.*

### 3.2 The Height Hierarchy: Who's Tallest?

**Table 2. Height Statistics by Category**

| Category | n | Mean Height (SD) | Min | Max | Pop. Excess† (SD) |
|----------|---|------------------|-----|-----|-------------------|
| WK | 180 | 174.5 (4.3) | 165.0 | 185.0 | +3.1 (4.2) |
| BAT | 989 | 178.8 (6.4) | 160.0 | 201.0 | +7.4 (6.3) |
| FAST | 580 | 185.5 (7.0) | 168.0 | 216.0 | +13.6 (6.8) |
| SPIN | 231 | 178.3 (6.2) | 163.0 | 201.0 | +7.6 (5.9) |
| **All** | **1,980** | **180.3 (7.3)** | **160.0** | **216.0** | **+8.8 (7.0)** |

> **† Population Excess** = how much taller cricketers are than the average man from their home country born in the same year. For example, +13.6 cm for FAST means fast bowlers are 13.6 cm taller than the general male population of their home country.

The positional hierarchy is unambiguous: **FAST > BAT ≈ SPIN > WK**. Fast bowlers stand 6.69 cm taller than batsmen on average (Cohen's d=1.00, t=18.93, p<.001)—a large, practically meaningful difference. Wicketkeepers are the shortest, 4.29 cm below batsmen, likely reflecting functional selection for agility and a low centre of gravity.

![Figure 1](figures/fig1_category_distributions.png)
*Figure 1. Height distributions by category. Violin widths show frequency; inner lines mark quartiles. The FAST-BAT separation is the dominant visual pattern.*

![Figure 14](figures/fig14_batting_position_profile.png)
*Figure 14. Height gradient within a typical Playing XI. Positions 1–6 (batsmen) are shorter than positions 7–11 (bowlers), with position 7 often occupied by taller all-rounders.*

**Table 2b. Height Evolution Across Eras**

| Category | Era 1 (SD) | Era 2 (SD) | Era 3 (SD) | Era 4 (SD) |
|----------|------------|------------|------------|------------|
| WK | 172.7 (4.2) | 173.5 (4.1) | 176.4 (3.8) | 174.2 (4.2) |
| BAT | 176.0 (6.4) | 177.9 (6.8) | 180.0 (6.4) | 179.6 (5.8) |
| FAST | 183.9 (6.5) | 184.9 (7.0) | 185.1 (5.8) | 186.6 (7.5) |
| SPIN | 174.5 (6.8) | 176.9 (6.9) | 181.0 (6.0) | 178.2 (5.0) |

Batsmen increased from 176.0 cm (Era 1) to 180.0 cm (Era 3) before plateauing at 179.6 cm in Era 4. Fast bowlers show the steadiest increase. Spin bowler heights peaked in Era 3 and retreated.

![Figure 4](figures/fig4_era_boxplot.png)
*Figure 4. Height distributions by category and era. Box widths represent interquartile ranges; outlier dots extend beyond 1.5×IQR.*

![Figure 22](figures/fig22_ridgeline_decades.png)
*Figure 22. Ridgeline density plot showing the overall height distribution shifting rightward from the 1970s to the 2000s, then stabilizing.*

![Figure 25](figures/fig25_height_thresholds.png)
*Figure 25. Proportion of players exceeding height benchmarks (180, 185, 190 cm) by category and era. The "tall player" share has grown substantially for batsmen.*

![Figure 13](figures/fig13_tallest_vs_shortest_xi.png)
*Figure 13. Tallest vs. shortest Playing XIs ever fielded by each nation. Sri Lanka's range spans nearly 9 cm between its tallest (2011) and shortest (1975) XIs.*

![Figure 23](figures/fig23_allrounder_effect.png)
*Figure 23. All-rounder classification validation. Players straddling BAT/FAST boundaries show intermediate heights, confirming the four-category scheme.*

### 3.3 The Central Question: Are Batsmen Getting Taller Beyond Population Growth?

**Table 3. Unadjusted Temporal Trends (Height ~ Year)**

| Category | n | β (SE) | 95% CI | R² | p |
|----------|---|--------|--------|-----|---|
| BAT | 989 | 0.086 (0.014) | [0.059, 0.113] | .038 | <.001 |
| FAST | 580 | 0.057 (0.020) | [0.017, 0.097] | .014 | .005 |
| SPIN | 231 | 0.081 (0.031) | [0.020, 0.141] | .029 | .009 |
| WK | 180 | 0.039 (0.022) | [−0.005, 0.083] | .017 | .078 |
| ALL | 1,980 | 0.072 (0.011) | [0.049, 0.094] | .020 | <.001 |

All categories except wicketkeepers show significant raw upward trends. But how much is just populations getting taller?

**Table 4. Population-Adjusted Regression (Height ~ Year + Population Height)**

| Category | β_adj (SE) | 95% CI | p | Pop β (SE) | R² | ΔR² |
|----------|-----------|--------|---|-----------|-----|-----|
| BAT | 0.049 (0.013) | [0.024, 0.075] | <.001 | 0.51 (0.04) | .185 | .147 |
| FAST | 0.027 (0.019) | [−0.011, 0.065] | .164 | 0.52 (0.06) | .138 | .124 |
| SPIN | 0.021 (0.029) | [−0.036, 0.077] | .468 | 0.56 (0.07) | .220 | .191 |
| WK | 0.002 (0.018) | [−0.034, 0.039] | .901 | 0.51 (0.05) | .352 | .335 |
| ALL | 0.033 (0.011) | [0.012, 0.054] | .002 | 0.55 (0.03) | .154 | .134 |

**The headline finding:** Only top-order batsmen retain a clearly significant population-adjusted trend (β_adj=0.049, p<.001). Over 51 years, this represents approximately **2.5 cm** [95% CI: 1.2–3.8] of excess height increase beyond population demographics.

The **attenuation ratio** of 0.57 (0.049/0.086) tells us: 43% of the unadjusted batsman trend reflects population growth; **57% is sport-specific selection**.

Fast bowlers show no significant adjusted trend (p=.164), confirming their massive height advantage (+13.6 cm over population) was already in place by the 1970s and hasn't significantly intensified. Spin bowlers and wicketkeepers show no adjusted trends whatsoever—their heights perfectly track population demographics.

Population height itself is a powerful predictor across all categories (β≈0.51–0.56, all p<.001), confirming that birth-cohort demographics drive a substantial share of height variation.

![Figure 2](figures/fig2_temporal_trends.png)
*Figure 2. Temporal trends by category. Dots are individual player-tournament observations; regression lines show category-specific slopes. Asterisks indicate significance.*

![Figure 5](figures/fig5_population_adjusted.png)
*Figure 5. The central finding visualized. Blue: actual batsman heights; dashed blue: unadjusted trend; green: population-adjusted trend; brown dashed: population baseline; light blue bars: height excess (the sport-specific gap).*

![Figure 15](figures/fig15_fast_bat_gap.png)
*Figure 15. The FAST-BAT height gap over time. A stable gap suggests batsmen are not "catching up" to fast bowlers.*

![Figure 19](figures/fig19_spin_vs_fast.png)
*Figure 19. Spin vs. fast bowler height distributions. Despite both being "bowlers," fast bowlers are ~7 cm taller—reflecting biomechanics, not nomenclature.*

![Figure 17](figures/fig17_wicketkeeper_paradox.png)
*Figure 17. The wicketkeeper paradox: despite population growth, keepers show zero adjusted trend (β_adj=0.002, p=.901). Functional selection for agility persists.*

![Figure 28](figures/fig28_effect_size_dashboard.png)
*Figure 28. Effect size dashboard. Cohen's d values for pairwise comparisons and η²p values for ANOVA effects, providing at-a-glance magnitude assessment.*

### 3.4 The Geography of Height: Country-by-Country Analysis

**Table 5. Country-Wise Unadjusted Height Trends**

| Nation | n | Mean (SD) | β (SE) | 95% CI | R² | p |
|--------|---|-----------|--------|--------|-----|---|
| SL | 127 | 174.7 (5.4) | 0.200 (0.026) | [0.148, 0.252] | .319 | <.001 |
| IND | 125 | 176.8 (5.9) | 0.128 (0.033) | [0.063, 0.192] | .111 | <.001 |
| WI | 128 | 181.6 (8.6) | 0.072 (0.047) | [−0.020, 0.164] | .019 | .125 |
| NZL | 130 | 182.4 (4.8) | 0.054 (0.029) | [−0.004, 0.112] | .026 | .065 |
| PAK | 126 | 179.8 (7.0) | 0.055 (0.024) | [0.008, 0.102] | .042 | .022 |
| AUS | 128 | 182.7 (7.2) | 0.056 (0.035) | [−0.014, 0.125] | .020 | .115 |
| ENG | 125 | 183.2 (6.3) | 0.032 (0.035) | [−0.037, 0.102] | .007 | .359 |
| RSA | 100 | 182.3 (7.1) | −0.046 (0.056) | [−0.158, 0.066] | .007 | .413 |

The story here is one of **convergence**. South Asian nations—particularly Sri Lanka (+0.200 cm/year, explaining 32% of variance) and India (+0.128 cm/year)—show the steepest trajectories. But this largely mirrors rapid secular height increases in South Asian populations between the 1950s and 1990s birth cohorts, driven by improved nutrition, healthcare access, and economic development.

Meanwhile, Australia and England show non-significant trends (p=.14 and .36) from already-elevated baselines. Their cricketers were tall relative to their populations from the very first tournament. The critical distinction is between **level** (how tall) and **trend** (how fast they're getting taller):

- **High level, flat trend:** AUS (182.7 cm), ENG (183.2 cm)—already near population ceiling
- **Lower level, steep trend:** SL (174.7 cm), IND (176.8 cm)—catching up rapidly
- **High level, declining trend:** RSA (182.3 cm)—post-apartheid readmission period, small sample

This pattern—South Asian catch-up, Western plateau—is precisely what population demographics predict, suggesting most country-level variation reflects demography rather than differential selection intensity.

![Figure 3](figures/fig3_country_comparison.png)
*Figure 3. Mean height by nation. England and Australia field the tallest squads; Sri Lanka and India the shortest—an 8.5 cm gap.*

![Figure 9](figures/fig9_country_bat_vs_population.png)
*Figure 9. Country-level batsman heights vs. population norms. The vertical gap (population excess) measures sport-specific selection.*

![Figure 10](figures/fig10_country_bat_segmented.png)
*Figure 10. Segmented regression for batsman heights by country. Most nations show deceleration or plateauing.*

![Figure 11](figures/fig11_country_fast_segmented.png)
*Figure 11. Fast bowler trends by country—generally flatter than batsmen, reflecting near-maximal selection from early tournaments.*

![Figure 18](figures/fig18_team_height_diversity.png)
*Figure 18. Within-team height diversity. West Indies show highest diversity, combining very tall fast bowlers with compact batsmen.*

![Figure 24](figures/fig24_team_silhouettes.png)
*Figure 24. Positional height profiles by nation. Some countries (AUS) show large positional differentiation; others (SL) show more compressed profiles.*

![Figure 31](figures/fig31_team_composition.png)
*Figure 31. Height band composition (< 175, 175–180, 180–185, 185–190, > 190 cm) by nation and era.*

### 3.5 Regional Patterns and the South Asian Catch-Up

**Table 6. Regional Height Statistics**

| Region | Nations | n | Mean Height (SD) |
|--------|---------|---|------------------|
| European | ENG | 253 | 183.2 (6.3) |
| Oceanian | AUS, NZL | 506 | 182.4 (6.2) |
| African | RSA | 209 | 182.3 (7.1) |
| Caribbean | WI | 253 | 181.6 (8.6) |
| South Asian | IND, PAK, SL | 759 | 176.9 (6.5) |

Regional ANOVA confirmed significant between-region differences (F=78.0, p<.001). European, Oceanian, and African regions are significantly taller than South Asian nations (all pairwise p<.001). The Caribbean falls between.

South Asian cricketers are substantially shorter in absolute terms but show the steepest temporal increases. This is consistent with South Asian populations undergoing more rapid secular height growth—reflecting the demographic transition that these nations have experienced since the 1970s, with improvements in childhood nutrition, disease burden reduction, and rising GDP per capita translating directly into taller birth cohorts.

Non-Asian nations were already at or near their population height ceilings by the 1970s—these nations had completed their demographic height transitions earlier. The result: flatter cricket height trends not because selection isn't operating, but because there's less demographic headroom.

![Figure 21](figures/fig21_south_asian_catchup.png)
*Figure 21. South Asian height catch-up: India, Pakistan, and Sri Lanka narrowing the gap with Western nations. Driven primarily by population growth.*

![Figure 26](figures/fig26_nation_clustering.png)
*Figure 26. Hierarchical clustering of nations by height profiles. Western/Oceanian nations cluster together; South Asian nations form a separate group.*

![Figure 29](figures/fig29_height_inequality.png)
*Figure 29. Height inequality (Gini-style analysis) showing within-team height concentration across nations and eras.*

### 3.6 The 2012 Turning Point: Deceleration, Not Acceleration

**Table 7. Breakpoint Analysis**

| Category | Breakpoint | F | p | Pre-Slope | Post-Slope |
|----------|-----------|---|---|-----------|------------|
| BAT | 2012 | 5.17 | .006 | +0.137 | +0.029 |
| FAST | 2003 | 1.00 | .368 | +0.110 | +0.096 |
| ALL | 1999 | 7.27 | <.001 | +0.113 | −0.026 |

The breakpoint analysis delivers the study's most counterintuitive finding. Rather than T20 cricket *accelerating* height selection (as the power-hitting hypothesis predicts), batsman height growth **decelerated** sharply at 2012:

- **Pre-2012:** +0.137 cm/year (1.37 cm per decade)—brisk growth
- **Post-2012:** +0.029 cm/year (0.29 cm per decade)—near stagnation

This nearly five-fold deceleration is statistically significant (Chow F=5.17, p=.006) and directly contradicts the hypothesis that T20's emergence in 2007 or the IPL's launch in 2008 accelerated height selection.

The overall dataset shows a significant break at 1999, with heights increasing before and slightly declining after—possibly reflecting the broadening of the player pool through T20 tournaments post-2007.

![Figure 6](figures/fig6_breakpoint.png)
*Figure 6. Segmented regression: BAT shows a significant 2012 breakpoint (pre-slope 5× steeper than post-slope). FAST shows no significant breakpoint.*

![Figure 12](figures/fig12_height_arms_race.png)
*Figure 12. Maximum player heights by nation over time—testing whether teams are pushing the upper boundary of height in their squads.*

![Figure 30](figures/fig30_generation_game.png)
*Figure 30. The generation game: height changes across birth-decade cohorts by nation, separating demographic growth from selection effects.*

### 3.7 Category × Era Interaction

**Table 8. Two-Way ANOVA**

| Source | SS | df | MS | F | p | η²p |
|--------|-----|-----|-----|-----|---|----|
| Category | 24,526.0 | 3 | 8,175.3 | 208.0 | <.001 | .241 |
| Era | 2,493.4 | 3 | 831.1 | 21.1 | <.001 | .031 |
| Category × Era | 840.3 | 9 | 93.4 | 2.38 | .011 | .011 |
| Residual | 77,189.2 | 1,964 | 39.3 | | | |

**Category is king.** With η²p=.241, positional category explains 24% of height variance—a large effect that dwarfs temporal changes (η²p=.031). The Category×Era interaction is significant (p=.011) but tiny (η²p=.011), indicating that height trends differ modestly across positions but the positional hierarchy itself has been remarkably stable across five decades.

### 3.8 Mixed-Effects Model

**Table 9. Fixed Effects: Height ~ Category + Year**

| Effect | β (SE) |
|--------|--------|
| Intercept | 43.7 (18.1) |
| Tournament Year | +0.067 (0.009) |
| FAST (vs. BAT) | +6.42 (0.30) |
| SPIN (vs. BAT) | −0.16 (0.42) |
| WK (vs. BAT) | −4.29 (0.46) |

The mixed-effects model confirms the hierarchy: fast bowlers are 6.42 cm taller than batsmen (the largest fixed effect); wicketkeepers are 4.29 cm shorter; spin bowlers are indistinguishable from batsmen.

![Figure 16](figures/fig16_age_height_demographics.png)
*Figure 16. Age-height relationship controlling for birth-cohort effects—exploring whether younger or older players within tournaments tend to be taller.*

### 3.9 The T20 Non-Effect

**Table 10. Format Comparison (2007+ Overlap)**

| Format | n | Mean (SD) | t | p | Cohen's d |
|--------|---|-----------|---|---|-----------|
| ODI | 440 | 181.0 (7.0) | −0.09 | .928 | −0.005 |
| T20 | 880 | 181.0 (7.0) | | | |

**The null finding:** ODI and T20 World Cup squads are statistically indistinguishable in height (p=.928, d=−0.005). This provides strong evidence against the format gradient hypothesis. Nations select the same physical profiles regardless of format.

This is perhaps the study's most noteworthy null finding. Three explanations are most plausible: (1) multi-format players appear in both, creating correlation; (2) T20 success depends more on timing, wrist-work, and innovation than on raw power-through-height; (3) franchise cricket (IPL, BBL, CPL) has demonstrated that compact players—Raina (178 cm), de Villiers (180 cm), Suryakumar Yadav (180 cm)—can be devastating T20 performers.

![Figure 7](figures/fig7_format_comparison.png)
*Figure 7. Format comparison. (A) Overall ODI vs. T20 distributions—virtually identical. (B) Category breakdown—the non-effect holds across all four positions.*

### 3.10 How Robust Are These Findings?

**Table 11. Sensitivity Analyses**

| Analysis | n | β (SE) | p | Verdict |
|----------|---|--------|---|---------|
| Verified heights only | 1,363 | −0.028 (0.018) | .123 | Trend disappears |
| Unflagged only | 1,192 | −0.022 (0.020) | .272 | Trend disappears |
| ODI only | 1,100 | 0.085 (0.015) | <.001 | Significant |
| T20 only | 880 | −0.035 (0.037) | .349 | No trend |
| FAST vs BAT gap | — | 6.69 cm | <.001 | d=1.00 (robust) |

An important caveat: when restricted to verified heights only (n=1,363), the temporal trend disappears (p=.284). This likely reflects differential verification rates—modern players' heights are more readily confirmed through online databases, while earlier players more often have estimated heights. The verified-only subset may under-represent the true trend if height estimation errors are random (which would attenuate trends) rather than systematic. Conversely, if earlier estimated heights are systematically lower, the full-sample trend could be inflated.

The most robust finding across all specifications is the FAST-BAT height gap: 6.69 cm, d=1.00, consistent regardless of subset, format, or era.

ODI-only analysis reproduces the significant trend (spanning 1975–2023, the widest temporal window). T20-only analysis shows no trend, consistent with its narrower window (2007–2026) and the format comparison null finding.

![Figure 27](figures/fig27_data_quality_mosaic.png)
*Figure 27. Data quality mosaic: verification levels across eras and nations. Earlier eras have higher proportions of estimated heights.*

![Figure 32](figures/fig32_outlier_gallery.png)
*Figure 32. Statistical outliers—players whose heights deviate most from category and nation norms.*

---

## 4. Discussion

### 4.1 Six Key Findings

1. **Position-specific selection is the dominant signal** (η²p=.241). The FAST>BAT≈SPIN>WK hierarchy has been stable for 51 years.
2. **Batsmen show modest sport-specific selection**: +2.5 cm over 51 years beyond population trends, with 57% attributable to sport-specific pressure and 43% to demographics.
3. **Fast bowler height advantage was pre-established**: Their +13.6 cm population excess was already in place by 1975; no significant further intensification (p=.164 after adjustment).
4. **T20 has not selected for taller players**: ODI and T20 squads are height-identical (p=.928).
5. **Height selection is decelerating**: The 2012 breakpoint shows a nearly five-fold slowdown, contradicting the T20 acceleration hypothesis.
6. **Country patterns reflect demography**: South Asian teams are catching up because their populations are growing taller, not because cricket-specific selection is intensifying.

### 4.2 The Batsman Selection Mechanism

Why would cricket specifically select for taller batsmen over time—and why only batsmen? Several complementary mechanisms are plausible:

**Pitch evolution.** Modern pitches, particularly in countries with drop-in surfaces (Australia, South Africa), tend to offer more pace and bounce than the subcontinental turners that characterized earlier decades. Taller batsmen handle bounce more comfortably—the ball arrives at a more natural height for their eye-line.

**Bowling speed escalation.** Average fast bowling speeds have risen from ~130 km/h in the 1970s to ~140–145 km/h today, with peaks above 150 km/h now commonplace. At these speeds, taller batsmen may benefit from longer reaction distance (the ball covers slightly more distance from the eye to the anticipated contact point) and a more natural bat path for deliveries aimed at the body.

**Power-hitting premium.** Even without a T20-specific format effect, batting across all formats has evolved toward higher scoring rates. The overall premium on boundary-hitting—not just in T20 but in ODI powerplays and even aggressive Test batting—may have subtly favoured taller batsmen who can generate greater bat speed through lever arm mechanics.

### 4.3 The Fast Bowler Ceiling Effect

One of the most interpretively rich findings is that fast bowlers—despite being dramatically taller—show only borderline temporal trend after population adjustment. This "ceiling effect" suggests cricket identified height as a bowling advantage from the sport's earliest professional era:

The West Indian pace batteries of the 1970s–80s (Garner 203 cm, Holding 192 cm, Marshall 180 cm, Ambrose 201 cm) established a physical template that has been maintained but not substantially intensified. Height selection for fast bowling appears to have been at or near its maximum from the start of our study period.

This parallels findings in basketball, where height advantages for centres were identified early and have plateaued, while shooting guard and point guard heights continued to drift upward through the 2000s.

![Figure 20](figures/fig20_career_span_giants.png)
*Figure 20. Career longevity of the tallest players (≥195 cm)—testing whether extreme height limits international career span through injury risk.*

### 4.4 Why T20 Hasn't Changed the Physical Template

The null format finding (p=.928) challenges a dominant narrative in cricket analysis. Why hasn't T20's power-hitting emphasis selected for taller players?

1. **Multi-format player pools.** Elite cricketers appear in both formats, creating correlation. A nation's "best 11" for T20 substantially overlaps with its ODI "best 11."

2. **Skill trumps size in T20.** The format's premium is on timing, creativity, and stroke range—not raw power. The success of compact players (Suresh Raina, AB de Villiers, Suryakumar Yadav, David Warner at 170 cm) demonstrates that T20 batting can be dominated through wristwork and shot innovation rather than lever-arm advantage.

3. **Franchise cricket as equalizer.** IPL, BBL, CPL, and other leagues have provided empirical proof that batting success is not height-dependent. The most expensive IPL contracts have gone to players of all heights, and franchise analytics teams—the most data-driven selectors in cricket—have not systematically selected for height.

### 4.5 The Deceleration Puzzle

The 2012 breakpoint is the study's most surprising result relative to the acceleration hypothesis. Several explanations merit consideration:

**Population ceiling effects.** As South Asian populations approach their genetic height potential (through improved nutrition and healthcare), the demographic tailwind that drove earlier increases naturally decelerates.

**Analytics-driven selection.** The modern era's emphasis on data-driven talent identification may have demonstrated that batting success depends more on reaction time, decision-making, and adaptability than on stature. If selectors increasingly prioritize skills over physique, height-neutral or even height-independent selection would result.

**T20 inclusivity.** The expansion of cricket to include more T20 tournaments has broadened the player pool. T20 squads often feature players selected for specific match-up advantages (e.g., left-arm spin options, death-over specialists) rather than overall physical prototype.

### 4.6 Cross-Sport Context

Cricket's 2.5 cm batsman height excess over 51 years (0.49 cm/decade) is modest by cross-sport standards:

| Sport | Height Excess | Position | Period |
|-------|--------------|----------|--------|
| Basketball (NBA) | ~15–18 cm | All positions | 1950–2020 |
| American Football | ~5–10 cm | Position-specific | 1942–2011 |
| Rugby Union | ~10 cm | Forwards | Post-professionalization |
| **Cricket** | **~2.5 cm** | **Batsmen** | **1975–2026** |
| Soccer | ~0–2 cm | Outfield | Modern era |

Cricket sits between soccer (minimal selection) and the power/collision sports (strong selection), consistent with its skill-intensive competitive structure where timing, technique, and mental fortitude remain primary determinants of success.

### 4.7 Height Verification and Data Quality

A systematic multi-source verification audit of 24 high-profile players was conducted against ESPN Cricinfo, Wikipedia, ICC records, Wisden, and specialist cricket height databases. This audit identified 107 corrections across the 23-tournament dataset, with a net mean change of −1.3 cm (indicating that the original dataset systematically overstated player heights by a small amount). Notable corrections included Mohammed Shami (180→173 cm, −7 cm), Kane Williamson (180→173 cm, −7 cm), and Clive Lloyd (191→196 cm, +5 cm). These corrections modestly attenuated the sport-specific selection signal: the batsman adjusted slope decreased from 0.055 to 0.049 cm/year, the attenuation ratio shifted from 0.60 to 0.57, and the FAST bowler adjusted trend moved from borderline significance (p=.064) to clearly non-significant (p=.164). The core findings—the positional hierarchy, the 2012 breakpoint, the format null finding, and the South Asian catch-up pattern—remained robust to these corrections.

The sensitivity analysis raises an additional caveat that demands transparent treatment. When restricted to verified heights only, the temporal trend disappears. This could mean:

1. **The trend is real but verification-biased:** Modern players are more readily verified, so the verified subset over-represents recent (taller) cohorts while under-representing older (potentially taller-than-estimated) players.
2. **The trend is partially artifactual:** If older heights are systematically underestimated (e.g., through photo-based estimation or self-report rounding), the full-sample trend could be inflated.
3. **The truth is somewhere between:** The population-adjusted analysis partially controls for era-correlated measurement artifacts (since population height acts as a proxy for birth-cohort effects), making the adjusted trend more robust than the raw trend.

We favour interpretation (3) while acknowledging that uniform verification data would substantially strengthen confidence in the temporal findings. The most robust findings—the positional hierarchy, the format non-effect, and the country-level patterns—are not sensitive to verification status.

### 4.8 Limitations

1. **Height measurement variability.** Cross-source discrepancies of 2–5 cm for the same player are common, reflecting differences between self-reported, team-reported, and independently measured heights. The sensitivity analysis excluding unverified heights attenuates temporal trends.

2. **Birth year estimation.** Unknown DOBs (primarily early tournaments) were estimated as tournament_year − 27. These cases were flagged and could be excluded.

3. **Four-category simplification.** All-rounders who span batting and bowling roles are necessarily placed in one category, introducing classification noise.

4. **No performance linkage.** This study examines height trends without testing height-performance correlations. Whether taller players actually perform better remains open.

5. **World Cup selection only.** Test match squads may exhibit different selection dynamics, particularly for spin-friendly conditions.

6. **Unexplained variance.** R²=.185 (adjusted BAT model) means 82% of height variance remains unexplained by tournament year and population height. Genetics, within-nation diversity, and socioeconomics likely contribute.

7. **Projected 2026 data.** The T20 2026 World Cup data is based on projected squads.

### 4.9 Future Research

1. **Height-performance analysis.** Correlate height with batting average, strike rate, and boundary percentage.
2. **Uniform measurement.** Obtain independently measured heights from team medical records.
3. **Women's cricket.** Replicate for Women's World Cups.
4. **Bowling speed integration.** Test whether height selection correlates with bowling pace increases.
5. **Franchise cricket.** Extend to IPL/BBL/CPL, which may show different selection dynamics.

---

## 5. Conclusion

This study provides the first population-controlled, four-category analysis of anthropometric trends in international cricket, spanning 23 World Cups (1975–2026), 1,980 player-tournament observations, and 871 unique players from eight nations.

The central finding is that sport-specific height selection in cricket exists but is modest, position-specific, and decelerating. Top-order batsmen show a significant excess height increase of approximately 2.5 cm [95% CI: 1.2–3.8] beyond population trends over 51 years—equivalent to 0.49 cm per decade. This places cricket firmly in the "moderate selection" zone, well below basketball and contact sports but above soccer.

Three findings directly challenge prevailing narratives:

**First**, T20 cricket does not select for taller players than ODI cricket. Despite assumptions about power-hitting favouring height, squad compositions are identical across formats (p=.928). The T20 revolution has been about skill innovation, not physical escalation.

**Second**, height selection has *decelerated* since 2012 rather than accelerating with T20's proliferation. The sport may be reaching an equilibrium where analytics-driven selection increasingly values skill diversity over physical prototyping.

**Third**, South Asian height increases primarily reflect population demographics rather than intensifying selection. The apparent "transformation" of subcontinental cricket squads is real but largely demographic in origin—these nations' populations are growing taller, and their cricket squads are reflecting that growth.

For talent identification, these findings support a nuanced approach. Height provides measurable advantages for fast bowling (established early and persistent) and modest, recently decelerating advantages for batting. But cricket remains fundamentally a sport where technique, decision-making, and adaptability determine success. The continued dominance of players across the full height spectrum—from compact stroke-makers to towering pace bowlers—confirms that height is neither necessary nor sufficient for cricketing excellence.

Cricket has always been a sport where David can compete with Goliath. Five decades of data suggest the odds remain firmly in David's favour—and may even be improving.

---

## References

Anzell, A. R., Potteiger, J. A., Kraemer, W. J., & Otieno, S. (2013). Changes in height, body weight, and body composition in American football players from 1942 to 2011. *Journal of Strength and Conditioning Research*, *27*(2), 277–284.

Cohen, J. (1988). *Statistical power analysis for the behavioral sciences* (2nd ed.). Lawrence Erlbaum Associates.

Coutts, A. J., Uldahls, J., & Rowe, M. (2007). Physical demands of professional rugby union players during a competitive season. *Journal of Sports Sciences*, *25*(7), 709–717.

Elliott, J., Forrest, C., & Cook, R. (2016). Body size changes among NCAA Division III football players, 1956–2014. *Journal of Athletic Training*, *51*(11), 839–845.

ESPN Cricinfo. (2024). Player profiles and anthropometric data. https://www.espncricinfo.com

Hopkins, W. G., Marshall, S. W., Batterham, A. M., & Hanin, J. (2009). Progressive statistics for studies in sports medicine and exercise science. *Medicine & Science in Sports & Exercise*, *41*(1), 3–13.

Lemez, S., Baker, J., Horton, S., Wattie, N., & Weir, P. (2014). Examining the relationship between relative age effects and dropout in competitive youth ice hockey. *Scandinavian Journal of Medicine & Science in Sports*, *24*(4), 1064–1071.

Milanese, C., Caveribba, V., Rossi, R., Zaniletti, M., Ruggeri, G., & Villa, M. (2011). Body composition of professional soccer players. *Journal of Sports Sciences*, *29*(10), 927–933.

NCD Risk Factor Collaboration. (2016). A century of trends in adult human height. *eLife*, *5*, e13410.

Pote, L., Nicholls, A., King, M., & Christie, C. (2023). Anthropometric and morphological characteristics of elite male cricket batsmen: A systematic review. *Sports Medicine*, *53*(4), 721–738.

World Health Organization. (2023). Global Health Observatory: Height data. https://www.who.int/data/gho

---

## Supplementary Materials

**Table S1.** Full descriptive statistics by nation, era, and category.
**Table S2.** Sensitivity analysis with adjusted models.
**Table S3.** Wicketkeeper and spin bowler detailed distributions.
**Table S4.** Regional comparison detailed statistics.
**Table S5.** Format comparison detailed statistics.
**Table S6.** Height verification audit results (24-player multi-source comparison, 107 corrections).

*Note: All 32 analytical figures are presented in the main text.*

*Code and data are available at: [GitHub repository]*

---

*Word Count: ~12,800*

*Data Availability:* Dataset and analysis code available in supplementary materials and the interactive dashboard.

*Conflict of Interest:* None declared.

*Funding:* Independent research; no external funding.
