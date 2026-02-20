# Visualization Catalog for Cricket Anthropometric Study

## Overview

This document catalogs all visualizations that can be generated for the cricket anthropometric study, organized by analysis type. Each visualization includes:
- Description and purpose
- Python code template
- Example prompt for Claude Code

---

## 1. Descriptive Statistics Visualizations

### 1.1 Height Distribution by Category (Violin Plot)

**Purpose:** Show height distribution shape for each player category

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def plot_height_by_category(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    order = ['WK', 'BAT', 'SPIN', 'FAST']
    palette = {'WK': '#2ecc71', 'BAT': '#3498db', 'SPIN': '#9b59b6', 'FAST': '#e74c3c'}
    
    sns.violinplot(data=df, x='category', y='height_cm', order=order, 
                   palette=palette, inner='quartile', ax=ax)
    
    ax.set_xlabel('Player Category', fontsize=12)
    ax.set_ylabel('Height (cm)', fontsize=12)
    ax.set_title('Height Distribution by Player Category', fontsize=14)
    
    # Add sample sizes
    for i, cat in enumerate(order):
        n = len(df[df['category'] == cat])
        ax.text(i, df['height_cm'].min() - 2, f'n={n}', ha='center', fontsize=10)
    
    plt.tight_layout()
    return fig

# Claude Code prompt:
# "Create a violin plot showing height distribution by category (WK, BAT, SPIN, FAST)"
```

---

### 1.2 Height Distribution by Era (Box Plot)

**Purpose:** Show how heights changed across eras

```python
def plot_height_by_era(df):
    fig, ax = plt.subplots(figsize=(12, 6))
    
    era_labels = {1: '1975-1987', 2: '1992-1999', 3: '2003-2012', 4: '2014-2026'}
    df['era_label'] = df['era'].map(era_labels)
    
    sns.boxplot(data=df, x='era_label', y='height_cm', hue='category',
                palette='Set2', ax=ax)
    
    ax.set_xlabel('Era', fontsize=12)
    ax.set_ylabel('Height (cm)', fontsize=12)
    ax.set_title('Height Distribution by Era and Category', fontsize=14)
    ax.legend(title='Category', bbox_to_anchor=(1.02, 1))
    
    plt.tight_layout()
    return fig

# Claude Code prompt:
# "Create a box plot showing height by era (1-4) with different colors for each category"
```

---

### 1.3 Height Distribution by Country (Ridgeline Plot)

**Purpose:** Compare height distributions across nations

```python
import numpy as np

def plot_height_ridgeline(df):
    countries = ['AUS', 'ENG', 'NZL', 'RSA', 'WI', 'IND', 'PAK', 'SL']
    
    fig, axes = plt.subplots(len(countries), 1, figsize=(10, 12), sharex=True)
    
    for i, country in enumerate(countries):
        subset = df[df['country'] == country]['height_cm']
        axes[i].hist(subset, bins=20, alpha=0.7, color=plt.cm.viridis(i/len(countries)))
        axes[i].set_ylabel(country)
        axes[i].set_yticks([])
        axes[i].axvline(subset.mean(), color='red', linestyle='--', linewidth=1)
    
    axes[-1].set_xlabel('Height (cm)')
    fig.suptitle('Height Distribution by Country', fontsize=14)
    plt.tight_layout()
    return fig

# Claude Code prompt:
# "Create a ridgeline plot showing height distribution for each of the 8 countries"
```

---

### 1.4 Summary Statistics Heatmap

**Purpose:** Show mean heights across Category × Era

```python
def plot_summary_heatmap(df):
    pivot = df.pivot_table(values='height_cm', index='category', 
                           columns='era', aggfunc='mean')
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(pivot, annot=True, fmt='.1f', cmap='YlOrRd', 
                cbar_kws={'label': 'Mean Height (cm)'}, ax=ax)
    
    ax.set_xlabel('Era', fontsize=12)
    ax.set_ylabel('Category', fontsize=12)
    ax.set_title('Mean Height by Category and Era', fontsize=14)
    
    plt.tight_layout()
    return fig

# Claude Code prompt:
# "Create a heatmap showing mean height for each category across all 4 eras"
```

---

## 2. Temporal Trend Visualizations

### 2.1 Height Over Time (Scatter + Regression)

**Purpose:** Show temporal trend with regression line

```python
from scipy import stats

def plot_temporal_trend(df, category='BAT'):
    subset = df[df['category'] == category]
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Scatter plot
    ax.scatter(subset['tournament_year'], subset['height_cm'], 
               alpha=0.5, s=50, label='Players')
    
    # Regression line
    slope, intercept, r, p, se = stats.linregress(
        subset['tournament_year'], subset['height_cm']
    )
    x_line = np.array([subset['tournament_year'].min(), subset['tournament_year'].max()])
    y_line = slope * x_line + intercept
    
    ax.plot(x_line, y_line, 'r-', linewidth=2, 
            label=f'Trend: {slope:.3f} cm/year (p={p:.3f})')
    
    ax.set_xlabel('Tournament Year', fontsize=12)
    ax.set_ylabel('Height (cm)', fontsize=12)
    ax.set_title(f'{category} Height Trend Over Time', fontsize=14)
    ax.legend()
    
    plt.tight_layout()
    return fig

# Claude Code prompt:
# "Create a scatter plot with regression line showing BAT height trend from 1975-2024"
```

---

### 2.2 Multi-Category Trend Lines

**Purpose:** Compare trends across all categories

```python
def plot_multi_category_trends(df):
    fig, ax = plt.subplots(figsize=(12, 7))
    
    categories = ['WK', 'BAT', 'SPIN', 'FAST']
    colors = {'WK': '#2ecc71', 'BAT': '#3498db', 'SPIN': '#9b59b6', 'FAST': '#e74c3c'}
    
    for cat in categories:
        subset = df[df['category'] == cat]
        
        # Group by year and get mean
        yearly = subset.groupby('tournament_year')['height_cm'].mean()
        
        ax.plot(yearly.index, yearly.values, 'o-', color=colors[cat], 
                label=cat, linewidth=2, markersize=6)
    
    ax.set_xlabel('Tournament Year', fontsize=12)
    ax.set_ylabel('Mean Height (cm)', fontsize=12)
    ax.set_title('Height Trends by Category', fontsize=14)
    ax.legend(title='Category')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig

# Claude Code prompt:
# "Create a line plot showing mean height trend over time for all 4 categories"
```

---

### 2.3 Population-Adjusted Trend

**Purpose:** Show cricket heights vs population baseline

```python
def plot_population_adjusted(df):
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Cricket heights (BAT only)
    bat_df = df[df['category'] == 'BAT']
    cricket_yearly = bat_df.groupby('tournament_year')['height_cm'].mean()
    
    # Population heights
    pop_yearly = bat_df.groupby('tournament_year')['pop_height_birth_cohort'].mean()
    
    ax.plot(cricket_yearly.index, cricket_yearly.values, 'b-o', 
            linewidth=2, markersize=8, label='Cricket (BAT)')
    ax.plot(pop_yearly.index, pop_yearly.values, 'g--s', 
            linewidth=2, markersize=8, label='Population Baseline')
    
    # Shade the excess
    ax.fill_between(cricket_yearly.index, pop_yearly.values, cricket_yearly.values,
                    alpha=0.3, color='blue', label='Selection Excess')
    
    ax.set_xlabel('Tournament Year', fontsize=12)
    ax.set_ylabel('Height (cm)', fontsize=12)
    ax.set_title('Cricket Heights vs Population Baseline', fontsize=14)
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig

# Claude Code prompt:
# "Create a dual line plot comparing BAT heights against population baseline, 
#  with shading for the excess"
```

---

### 2.4 Segmented Regression (Breakpoint)

**Purpose:** Show structural break in trend

```python
def plot_segmented_regression(df, breakpoint=2007):
    bat_df = df[df['category'] == 'BAT']
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Scatter
    ax.scatter(bat_df['tournament_year'], bat_df['height_cm'], alpha=0.4, s=40)
    
    # Pre-breakpoint regression
    pre = bat_df[bat_df['tournament_year'] < breakpoint]
    slope1, int1, _, _, _ = stats.linregress(pre['tournament_year'], pre['height_cm'])
    x1 = np.array([pre['tournament_year'].min(), breakpoint])
    ax.plot(x1, slope1*x1 + int1, 'b-', linewidth=2, label=f'Pre-{breakpoint}: {slope1:.3f} cm/yr')
    
    # Post-breakpoint regression
    post = bat_df[bat_df['tournament_year'] >= breakpoint]
    slope2, int2, _, _, _ = stats.linregress(post['tournament_year'], post['height_cm'])
    x2 = np.array([breakpoint, post['tournament_year'].max()])
    ax.plot(x2, slope2*x2 + int2, 'r-', linewidth=2, label=f'Post-{breakpoint}: {slope2:.3f} cm/yr')
    
    # Breakpoint line
    ax.axvline(breakpoint, color='gray', linestyle='--', linewidth=1, label=f'Breakpoint: {breakpoint}')
    
    ax.set_xlabel('Tournament Year', fontsize=12)
    ax.set_ylabel('Height (cm)', fontsize=12)
    ax.set_title('Segmented Regression with Structural Break', fontsize=14)
    ax.legend()
    
    plt.tight_layout()
    return fig

# Claude Code prompt:
# "Create a segmented regression plot showing the 2007 breakpoint for BAT heights"
```

---

## 3. Comparison Visualizations

### 3.1 ODI vs T20 Format Comparison

**Purpose:** Compare heights between formats

```python
def plot_format_comparison(df):
    # Filter to overlapping years (2007+)
    overlap = df[df['tournament_year'] >= 2007]
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Box plot
    sns.boxplot(data=overlap, x='format', y='height_cm', hue='category',
                ax=axes[0], palette='Set2')
    axes[0].set_title('Height by Format and Category')
    axes[0].set_xlabel('Format')
    axes[0].set_ylabel('Height (cm)')
    
    # Paired comparison (BAT only)
    bat_odi = overlap[(overlap['category'] == 'BAT') & (overlap['format'] == 'ODI')]['height_cm']
    bat_t20 = overlap[(overlap['category'] == 'BAT') & (overlap['format'] == 'T20')]['height_cm']
    
    axes[1].hist(bat_odi, bins=15, alpha=0.6, label=f'ODI (μ={bat_odi.mean():.1f})')
    axes[1].hist(bat_t20, bins=15, alpha=0.6, label=f'T20 (μ={bat_t20.mean():.1f})')
    axes[1].set_xlabel('Height (cm)')
    axes[1].set_ylabel('Frequency')
    axes[1].set_title('BAT Height Distribution: ODI vs T20')
    axes[1].legend()
    
    plt.tight_layout()
    return fig

# Claude Code prompt:
# "Create a comparison plot showing ODI vs T20 heights for years 2007-2024"
```

---

### 3.2 Country Comparison Bar Chart

**Purpose:** Compare mean heights by country

```python
def plot_country_comparison(df, category='BAT'):
    subset = df[df['category'] == category]
    
    country_means = subset.groupby('country')['height_cm'].agg(['mean', 'std', 'count'])
    country_means = country_means.sort_values('mean', ascending=True)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    colors = ['#e74c3c' if c in ['IND', 'PAK', 'SL'] else '#3498db' for c in country_means.index]
    
    bars = ax.barh(country_means.index, country_means['mean'], 
                   xerr=country_means['std']/np.sqrt(country_means['count']),
                   color=colors, edgecolor='black', capsize=3)
    
    # Add value labels
    for bar, val in zip(bars, country_means['mean']):
        ax.text(val + 0.5, bar.get_y() + bar.get_height()/2, 
                f'{val:.1f}', va='center', fontsize=10)
    
    ax.set_xlabel('Mean Height (cm)', fontsize=12)
    ax.set_ylabel('Country', fontsize=12)
    ax.set_title(f'{category} Mean Height by Country (± SE)', fontsize=14)
    ax.axvline(subset['height_cm'].mean(), color='gray', linestyle='--', 
               label=f'Overall: {subset["height_cm"].mean():.1f}')
    ax.legend()
    
    plt.tight_layout()
    return fig

# Claude Code prompt:
# "Create a horizontal bar chart comparing mean BAT height by country with error bars"
```

---

### 3.3 Regional Comparison

**Purpose:** Compare heights by cricket region

```python
def plot_regional_comparison(df):
    # Define regions
    regions = {
        'AUS': 'Oceanian', 'NZL': 'Oceanian',
        'ENG': 'European',
        'IND': 'South Asian', 'PAK': 'South Asian', 'SL': 'South Asian',
        'WI': 'Caribbean',
        'RSA': 'African'
    }
    df['region'] = df['country'].map(regions)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    sns.boxplot(data=df, x='region', y='height_cm', hue='category',
                order=['Oceanian', 'European', 'African', 'Caribbean', 'South Asian'],
                palette='Set2', ax=ax)
    
    ax.set_xlabel('Region', fontsize=12)
    ax.set_ylabel('Height (cm)', fontsize=12)
    ax.set_title('Height Distribution by Region and Category', fontsize=14)
    ax.legend(title='Category', bbox_to_anchor=(1.02, 1))
    
    plt.tight_layout()
    return fig

# Claude Code prompt:
# "Create a regional comparison box plot grouping countries into Oceanian, European, 
#  South Asian, Caribbean, and African"
```

---

## 4. Statistical Analysis Visualizations

### 4.1 ANOVA Results (Forest Plot)

**Purpose:** Show effect sizes with confidence intervals

```python
def plot_anova_forest(effects_df):
    """
    effects_df should have columns: effect, estimate, ci_lower, ci_upper
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    y_pos = range(len(effects_df))
    
    ax.errorbar(effects_df['estimate'], y_pos, 
                xerr=[effects_df['estimate'] - effects_df['ci_lower'],
                      effects_df['ci_upper'] - effects_df['estimate']],
                fmt='o', capsize=5, capthick=2, markersize=8, color='navy')
    
    ax.axvline(0, color='gray', linestyle='--', linewidth=1)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(effects_df['effect'])
    ax.set_xlabel('Effect Size (cm)', fontsize=12)
    ax.set_title('ANOVA Effect Sizes with 95% CI', fontsize=14)
    
    plt.tight_layout()
    return fig

# Claude Code prompt:
# "Create a forest plot showing effect sizes for Category, Era, and Category×Era interaction"
```

---

### 4.2 Regression Coefficients Plot

**Purpose:** Show regression coefficients with CIs

```python
def plot_regression_coefficients(model_results):
    """
    model_results: dict with keys = predictor names, 
                   values = {'coef': float, 'ci_lower': float, 'ci_upper': float, 'p': float}
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    predictors = list(model_results.keys())
    coefs = [model_results[p]['coef'] for p in predictors]
    ci_lower = [model_results[p]['ci_lower'] for p in predictors]
    ci_upper = [model_results[p]['ci_upper'] for p in predictors]
    
    colors = ['green' if model_results[p]['p'] < 0.05 else 'gray' for p in predictors]
    
    y_pos = range(len(predictors))
    
    ax.errorbar(coefs, y_pos, 
                xerr=[np.array(coefs) - np.array(ci_lower),
                      np.array(ci_upper) - np.array(coefs)],
                fmt='o', capsize=5, capthick=2, markersize=10, 
                color='black', ecolor=colors)
    
    ax.axvline(0, color='red', linestyle='--', linewidth=1)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(predictors)
    ax.set_xlabel('Coefficient (cm)', fontsize=12)
    ax.set_title('Regression Coefficients (green = p<0.05)', fontsize=14)
    
    plt.tight_layout()
    return fig

# Claude Code prompt:
# "Create a coefficient plot showing Year, PopHeight, and Format effects with 95% CIs"
```

---

### 4.3 Residual Diagnostics

**Purpose:** Check regression assumptions

```python
def plot_residual_diagnostics(y_true, y_pred):
    residuals = y_true - y_pred
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # Residuals vs Fitted
    axes[0, 0].scatter(y_pred, residuals, alpha=0.5)
    axes[0, 0].axhline(0, color='red', linestyle='--')
    axes[0, 0].set_xlabel('Fitted Values')
    axes[0, 0].set_ylabel('Residuals')
    axes[0, 0].set_title('Residuals vs Fitted')
    
    # Q-Q Plot
    stats.probplot(residuals, dist="norm", plot=axes[0, 1])
    axes[0, 1].set_title('Q-Q Plot')
    
    # Histogram of residuals
    axes[1, 0].hist(residuals, bins=30, edgecolor='black')
    axes[1, 0].set_xlabel('Residuals')
    axes[1, 0].set_ylabel('Frequency')
    axes[1, 0].set_title('Residual Distribution')
    
    # Scale-Location
    axes[1, 1].scatter(y_pred, np.sqrt(np.abs(residuals)), alpha=0.5)
    axes[1, 1].set_xlabel('Fitted Values')
    axes[1, 1].set_ylabel('√|Residuals|')
    axes[1, 1].set_title('Scale-Location')
    
    plt.tight_layout()
    return fig

# Claude Code prompt:
# "Create residual diagnostic plots for the population-adjusted regression model"
```

---

## 5. Publication-Quality Figures

### 5.1 Main Results Figure (Multi-Panel)

**Purpose:** Combined figure for paper

```python
def create_main_figure(df):
    fig = plt.figure(figsize=(14, 10))
    
    # Panel A: Category distributions
    ax1 = fig.add_subplot(2, 2, 1)
    sns.violinplot(data=df, x='category', y='height_cm', 
                   order=['WK', 'BAT', 'SPIN', 'FAST'], palette='Set2', ax=ax1)
    ax1.set_title('A. Height by Category', fontweight='bold')
    ax1.set_xlabel('')
    ax1.set_ylabel('Height (cm)')
    
    # Panel B: Temporal trend
    ax2 = fig.add_subplot(2, 2, 2)
    for cat in ['BAT', 'FAST']:
        subset = df[df['category'] == cat]
        yearly = subset.groupby('tournament_year')['height_cm'].mean()
        ax2.plot(yearly.index, yearly.values, 'o-', label=cat, linewidth=2)
    ax2.set_title('B. Height Trend Over Time', fontweight='bold')
    ax2.set_xlabel('Year')
    ax2.set_ylabel('Mean Height (cm)')
    ax2.legend()
    
    # Panel C: Country comparison
    ax3 = fig.add_subplot(2, 2, 3)
    country_order = df.groupby('country')['height_cm'].mean().sort_values().index
    sns.boxplot(data=df[df['category'] == 'BAT'], x='country', y='height_cm',
                order=country_order, ax=ax3)
    ax3.set_title('C. BAT Height by Country', fontweight='bold')
    ax3.set_xlabel('')
    ax3.set_ylabel('Height (cm)')
    ax3.tick_params(axis='x', rotation=45)
    
    # Panel D: Format comparison
    ax4 = fig.add_subplot(2, 2, 4)
    overlap = df[df['tournament_year'] >= 2007]
    sns.boxplot(data=overlap, x='format', y='height_cm', hue='category',
                hue_order=['BAT', 'FAST'], ax=ax4)
    ax4.set_title('D. ODI vs T20 (2007-2024)', fontweight='bold')
    ax4.set_xlabel('')
    ax4.set_ylabel('Height (cm)')
    
    plt.tight_layout()
    return fig

# Claude Code prompt:
# "Create a 4-panel publication figure showing: A) category distributions, 
#  B) temporal trends, C) country comparison, D) format comparison"
```

---

### 5.2 Supplementary Figure: All Countries

**Purpose:** Detailed country-level analysis

```python
def create_country_supplement(df):
    countries = ['AUS', 'ENG', 'NZL', 'RSA', 'WI', 'IND', 'PAK', 'SL']
    
    fig, axes = plt.subplots(2, 4, figsize=(16, 8), sharey=True)
    axes = axes.flatten()
    
    for i, country in enumerate(countries):
        subset = df[df['country'] == country]
        
        for cat in ['BAT', 'FAST']:
            cat_data = subset[subset['category'] == cat]
            yearly = cat_data.groupby('tournament_year')['height_cm'].mean()
            axes[i].plot(yearly.index, yearly.values, 'o-', label=cat, markersize=4)
        
        axes[i].set_title(country, fontweight='bold')
        axes[i].set_xlabel('Year')
        if i % 4 == 0:
            axes[i].set_ylabel('Height (cm)')
        axes[i].legend(fontsize=8)
        axes[i].grid(True, alpha=0.3)
    
    plt.suptitle('Height Trends by Country', fontsize=14, fontweight='bold')
    plt.tight_layout()
    return fig

# Claude Code prompt:
# "Create an 8-panel figure showing height trends for each country separately"
```

---

## 6. Interactive/Exploratory Visualizations

### 6.1 Player Height Explorer (Scatter Matrix)

```python
def plot_scatter_matrix(df):
    from pandas.plotting import scatter_matrix
    
    numeric_cols = ['height_cm', 'age_at_tournament', 'birth_year', 'tournament_year']
    
    fig, axes = scatter_matrix(df[numeric_cols], figsize=(12, 12), 
                                diagonal='hist', alpha=0.5)
    plt.suptitle('Variable Relationships', y=1.02)
    return fig

# Claude Code prompt:
# "Create a scatter matrix showing relationships between height, age, birth year, and tournament year"
```

---

### 6.2 Player Career Timeline

**Purpose:** Track individual players across tournaments

```python
def plot_player_career(df, player_id):
    player = df[df['player_id'] == player_id]
    
    fig, ax = plt.subplots(figsize=(10, 4))
    
    ax.scatter(player['tournament_year'], [1]*len(player), 
               c=['blue' if f == 'ODI' else 'green' for f in player['format']],
               s=100, zorder=3)
    
    ax.axhline(1, color='gray', linewidth=0.5)
    ax.set_ylim(0.5, 1.5)
    ax.set_yticks([])
    ax.set_xlabel('Tournament Year')
    ax.set_title(f"World Cup Appearances: {player['full_name'].iloc[0]}")
    
    # Legend
    ax.scatter([], [], c='blue', label='ODI WC')
    ax.scatter([], [], c='green', label='T20 WC')
    ax.legend()
    
    plt.tight_layout()
    return fig

# Claude Code prompt:
# "Create a timeline showing Virat Kohli's World Cup appearances (ODI and T20)"
```

---

## 7. Data Quality Visualizations

### 7.1 Verification Status

```python
def plot_verification_status(df):
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # By verification status
    status_counts = df['height_verified'].value_counts()
    axes[0].pie(status_counts, labels=['Verified', 'Unverified'], 
                autopct='%1.1f%%', colors=['#2ecc71', '#e74c3c'])
    axes[0].set_title('Height Verification Status')
    
    # By flag type
    flag_counts = df['flag'].value_counts()
    axes[1].barh(flag_counts.index, flag_counts.values, color='steelblue')
    axes[1].set_xlabel('Count')
    axes[1].set_title('Data Quality Flags')
    
    plt.tight_layout()
    return fig

# Claude Code prompt:
# "Create a data quality summary showing verification status and flag distribution"
```

---

### 7.2 Missing Data Heatmap

```python
def plot_missing_data(df):
    # Check missing by tournament and field
    fields = ['height_cm', 'date_of_birth', 'pop_height_birth_cohort']
    
    missing = df.groupby('tournament_id')[fields].apply(
        lambda x: x.isna().sum() / len(x) * 100
    )
    
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(missing, annot=True, fmt='.0f', cmap='Reds', ax=ax)
    ax.set_title('Missing Data % by Tournament')
    ax.set_xlabel('Field')
    ax.set_ylabel('Tournament')
    
    plt.tight_layout()
    return fig

# Claude Code prompt:
# "Create a heatmap showing missing data percentage for each tournament"
```

---

## Quick Reference: Prompts for Claude Code

### Basic Visualizations
```
"Create a violin plot of height by category"
"Create a box plot of height by era"
"Create a bar chart of mean height by country"
"Create a histogram of BAT heights"
```

### Trend Analysis
```
"Create a scatter plot with regression line for BAT heights over time"
"Create a line plot comparing category trends over time"
"Create a segmented regression plot with breakpoint at 2007"
"Create a dual-axis plot comparing cricket heights vs population baseline"
```

### Comparisons
```
"Create a comparison of ODI vs T20 heights for 2007-2024"
"Create a regional comparison grouping countries by cricket region"
"Create a faceted plot showing trends for each country separately"
```

### Statistical
```
"Create a forest plot of ANOVA effect sizes"
"Create residual diagnostic plots for the regression model"
"Create a coefficient plot with confidence intervals"
```

### Publication
```
"Create a 4-panel figure suitable for publication"
"Create a supplementary figure with all 8 countries"
"Save all figures as 300 DPI PNG files"
```

---

*Version: 1.0 | Last Updated: 2025-02-15*
