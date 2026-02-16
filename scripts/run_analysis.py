#!/usr/bin/env python3
"""
run_analysis.py - Run all statistical analyses for the cricket
anthropometric research project.

Uses the merged CSV from data/processed/all_players.csv.

Analyses performed:
  Table 2 : Descriptive statistics by category and era
  Table 3 : Linear regression  height ~ year, per category
  Table 4 : Population-adjusted regression  height ~ year + pop_height
  Table 5 : Country-wise regression for BAT category
  Table 6 : Regional ANOVA
  Table 7 : Segmented regression / Chow test for breakpoint detection
  Table 8 : Two-way ANOVA  Category x Era
  Table 9 : Mixed-effects model with Nation as random intercept
  Table 10: Sensitivity analyses

Results printed as formatted tables and saved to
data/processed/analysis_results.json.

Usage:
    python scripts/run_analysis.py
"""

import json
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

# Optional imports -- degrade gracefully
try:
    import statsmodels.api as sm
    import statsmodels.formula.api as smf
    from statsmodels.regression.mixed_linear_model import MixedLM
    HAS_STATSMODELS = True
except ImportError:
    HAS_STATSMODELS = False
    print("WARNING: statsmodels not installed. Some analyses will be skipped.")

try:
    import pingouin as pg
    HAS_PINGOUIN = True
except ImportError:
    HAS_PINGOUIN = False

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
MERGED_CSV = BASE_DIR / "data" / "processed" / "all_players.csv"
OUTPUT_JSON = BASE_DIR / "data" / "processed" / "analysis_results.json"

CATEGORIES = ["WK", "BAT", "FAST", "SPIN"]
NATIONS = ["AUS", "ENG", "IND", "PAK", "WI", "NZL", "SL", "RSA"]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def print_header(title: str):
    """Print a formatted section header."""
    print(f"\n{'=' * 72}")
    print(f"  {title}")
    print(f"{'=' * 72}")


def safe_ols(formula: str, data: pd.DataFrame) -> dict:
    """Run OLS regression and return a summary dict. Returns None on error."""
    if not HAS_STATSMODELS:
        return None
    try:
        data_clean = data.dropna(subset=[
            c.strip() for c in formula.replace("~", "+").split("+")
            if c.strip() and c.strip() != ""
        ])
        if len(data_clean) < 5:
            return None
        model = smf.ols(formula, data=data_clean).fit()
        result = {
            "formula": formula,
            "n": int(model.nobs),
            "r_squared": round(float(model.rsquared), 4),
            "adj_r_squared": round(float(model.rsquared_adj), 4),
            "f_statistic": round(float(model.fvalue), 4) if not np.isnan(model.fvalue) else None,
            "f_pvalue": round(float(model.f_pvalue), 6) if not np.isnan(model.f_pvalue) else None,
            "coefficients": {},
        }
        for param in model.params.index:
            result["coefficients"][param] = {
                "estimate": round(float(model.params[param]), 4),
                "std_err": round(float(model.bse[param]), 4),
                "t_value": round(float(model.tvalues[param]), 4),
                "p_value": round(float(model.pvalues[param]), 6),
                "ci_lower": round(float(model.conf_int().loc[param, 0]), 4),
                "ci_upper": round(float(model.conf_int().loc[param, 1]), 4),
            }
        return result
    except Exception as e:
        print(f"    OLS error ({formula}): {e}")
        return None


def format_coef(coef_dict: dict, key: str) -> str:
    """Format a coefficient for table display."""
    if coef_dict is None or key not in coef_dict:
        return "N/A"
    c = coef_dict[key]
    sig = ""
    p = c["p_value"]
    if p < 0.001:
        sig = "***"
    elif p < 0.01:
        sig = "**"
    elif p < 0.05:
        sig = "*"
    return f"{c['estimate']:.4f}{sig} [{c['ci_lower']:.3f}, {c['ci_upper']:.3f}]"


# ---------------------------------------------------------------------------
# Analyses
# ---------------------------------------------------------------------------

def table2_descriptive(df: pd.DataFrame) -> dict:
    """Table 2: Descriptive statistics by category and era."""
    print_header("TABLE 2: Descriptive Statistics by Category and Era")

    results = {}

    # By category
    print("\n--- By Category ---")
    cat_stats = df.groupby("category")["height_cm"].agg(
        ["count", "mean", "std", "min", "max"]
    ).round(2)
    print(cat_stats.to_string())
    results["by_category"] = cat_stats.to_dict()

    # By era
    print("\n--- By Era ---")
    era_stats = df.groupby("era")["height_cm"].agg(
        ["count", "mean", "std", "min", "max"]
    ).round(2)
    print(era_stats.to_string())
    results["by_era"] = era_stats.to_dict()

    # Category x Era
    print("\n--- Category x Era (Mean Height cm) ---")
    pivot = df.pivot_table(
        values="height_cm", index="category", columns="era",
        aggfunc=["mean", "count"]
    ).round(2)
    print(pivot.to_string())

    # Height excess by category
    if df["height_excess"].notna().any():
        print("\n--- Height Excess Over Population by Category ---")
        excess_stats = df.groupby("category")["height_excess"].agg(
            ["count", "mean", "std", "min", "max"]
        ).round(2)
        print(excess_stats.to_string())
        results["excess_by_category"] = excess_stats.to_dict()

    # Overall
    n = len(df)
    n_verified = df["height_verified"].sum() if "height_verified" in df.columns else 0
    results["overall"] = {
        "n": int(n),
        "n_verified": int(n_verified),
        "mean_height": round(float(df["height_cm"].mean()), 2),
        "std_height": round(float(df["height_cm"].std()), 2),
        "n_unique_players": int(df["player_id"].nunique()),
        "n_tournaments": int(df["tournament_id"].nunique()),
    }

    print(f"\nOverall: n={n}, verified={n_verified}, "
          f"mean={results['overall']['mean_height']:.2f} cm, "
          f"sd={results['overall']['std_height']:.2f} cm")

    return results


def table3_unadjusted_regression(df: pd.DataFrame) -> dict:
    """Table 3: Linear regression height ~ year, for each category."""
    print_header("TABLE 3: Unadjusted Linear Regression (height ~ tournament_year)")

    results = {}
    for cat in CATEGORIES:
        subset = df[df["category"] == cat].dropna(subset=["height_cm", "tournament_year"])
        if len(subset) < 5:
            print(f"\n  {cat}: Insufficient data (n={len(subset)})")
            continue

        res = safe_ols("height_cm ~ tournament_year", subset)
        results[cat] = res
        if res:
            print(f"\n  {cat} (n={res['n']}, R2={res['r_squared']:.4f}):")
            print(f"    Slope: {format_coef(res['coefficients'], 'tournament_year')}")
            print(f"    Intercept: {format_coef(res['coefficients'], 'Intercept')}")

    # All categories combined
    subset_all = df.dropna(subset=["height_cm", "tournament_year"])
    if len(subset_all) >= 5:
        res_all = safe_ols("height_cm ~ tournament_year", subset_all)
        results["ALL"] = res_all
        if res_all:
            print(f"\n  ALL (n={res_all['n']}, R2={res_all['r_squared']:.4f}):")
            print(f"    Slope: {format_coef(res_all['coefficients'], 'tournament_year')}")

    return results


def table4_adjusted_regression(df: pd.DataFrame) -> dict:
    """Table 4: Population-adjusted regression height ~ year + pop_height."""
    print_header("TABLE 4: Population-Adjusted Regression (height ~ year + pop_height)")

    results = {}
    subset_all = df.dropna(subset=["height_cm", "tournament_year", "pop_height_birth_cohort"])

    if len(subset_all) < 5:
        print("  Insufficient data with population heights for adjusted regression.")
        return results

    for cat in CATEGORIES:
        subset = subset_all[subset_all["category"] == cat]
        if len(subset) < 5:
            print(f"\n  {cat}: Insufficient data (n={len(subset)})")
            continue

        res = safe_ols("height_cm ~ tournament_year + pop_height_birth_cohort", subset)
        results[cat] = res
        if res:
            print(f"\n  {cat} (n={res['n']}, R2={res['r_squared']:.4f}, "
                  f"Adj-R2={res['adj_r_squared']:.4f}):")
            print(f"    Year slope (adjusted): {format_coef(res['coefficients'], 'tournament_year')}")
            print(f"    Pop height coef:       {format_coef(res['coefficients'], 'pop_height_birth_cohort')}")

    # All combined
    res_all = safe_ols("height_cm ~ tournament_year + pop_height_birth_cohort", subset_all)
    results["ALL"] = res_all
    if res_all:
        print(f"\n  ALL (n={res_all['n']}, R2={res_all['r_squared']:.4f}):")
        print(f"    Year slope (adjusted): {format_coef(res_all['coefficients'], 'tournament_year')}")
        print(f"    Pop height coef:       {format_coef(res_all['coefficients'], 'pop_height_birth_cohort')}")

    # Compute attenuation
    print("\n--- Attenuation Analysis ---")
    for cat in CATEGORIES:
        unadj_key = f"tournament_year"
        if cat in results and results[cat] is not None:
            adj_slope = results[cat]["coefficients"].get(unadj_key, {}).get("estimate")
            # Need unadjusted from Table 3
            subset_cat = df[df["category"] == cat].dropna(subset=["height_cm", "tournament_year"])
            unadj_res = safe_ols("height_cm ~ tournament_year", subset_cat)
            if unadj_res and adj_slope is not None:
                unadj_slope = unadj_res["coefficients"].get(unadj_key, {}).get("estimate")
                if unadj_slope and unadj_slope != 0:
                    attenuation = 1 - (adj_slope / unadj_slope)
                    print(f"  {cat}: Unadjusted={unadj_slope:.4f}, "
                          f"Adjusted={adj_slope:.4f}, "
                          f"Attenuation={attenuation:.1%}")

    return results


def table5_country_regression(df: pd.DataFrame) -> dict:
    """Table 5: Country-wise regression for BAT category."""
    print_header("TABLE 5: Country-wise Regression for BAT (height ~ year)")

    results = {}
    bat = df[df["category"] == "BAT"].dropna(subset=["height_cm", "tournament_year"])

    for nation in NATIONS:
        subset = bat[bat["country"] == nation]
        if len(subset) < 5:
            print(f"\n  {nation}: Insufficient data (n={len(subset)})")
            continue

        res = safe_ols("height_cm ~ tournament_year", subset)
        results[nation] = res
        if res:
            print(f"\n  {nation} (n={res['n']}, R2={res['r_squared']:.4f}):")
            print(f"    Slope: {format_coef(res['coefficients'], 'tournament_year')}")

    return results


def table6_regional_anova(df: pd.DataFrame) -> dict:
    """Table 6: Regional analysis - ANOVA comparing regions."""
    print_header("TABLE 6: Regional ANOVA")

    results = {}
    subset = df.dropna(subset=["height_cm", "region"])

    regions = sorted(subset["region"].unique())
    print(f"  Regions: {regions}")

    # Overall ANOVA
    groups = [
        subset[subset["region"] == r]["height_cm"].values
        for r in regions
        if len(subset[subset["region"] == r]) >= 2
    ]
    valid_regions = [
        r for r in regions
        if len(subset[subset["region"] == r]) >= 2
    ]

    if len(groups) >= 2:
        f_stat, p_value = stats.f_oneway(*groups)
        print(f"\n  One-way ANOVA: F={f_stat:.4f}, p={p_value:.6f}")
        results["overall_anova"] = {
            "f_statistic": round(float(f_stat), 4),
            "p_value": round(float(p_value), 6),
            "regions": valid_regions,
        }

        # Descriptive by region
        print("\n  --- Height by Region ---")
        region_stats = subset.groupby("region")["height_cm"].agg(
            ["count", "mean", "std"]
        ).round(2)
        print(region_stats.to_string())
        results["region_descriptive"] = region_stats.to_dict()

        # Post-hoc pairwise comparisons (Tukey's or Bonferroni-corrected t-tests)
        if HAS_PINGOUIN:
            print("\n  --- Pairwise Comparisons (Games-Howell) ---")
            try:
                posthoc = pg.pairwise_gameshowell(
                    data=subset, dv="height_cm", between="region"
                )
                print(posthoc.to_string())
            except Exception as e:
                print(f"    Post-hoc error: {e}")
        else:
            # Manual Bonferroni t-tests
            print("\n  --- Pairwise t-tests (Bonferroni corrected) ---")
            n_comparisons = len(valid_regions) * (len(valid_regions) - 1) // 2
            pairwise_results = []
            for i, r1 in enumerate(valid_regions):
                for r2 in valid_regions[i + 1:]:
                    g1 = subset[subset["region"] == r1]["height_cm"]
                    g2 = subset[subset["region"] == r2]["height_cm"]
                    t, p = stats.ttest_ind(g1, g2, equal_var=False)
                    p_adj = min(p * n_comparisons, 1.0)
                    sig = "*" if p_adj < 0.05 else ""
                    print(f"    {r1} vs {r2}: t={t:.3f}, p_adj={p_adj:.4f} {sig}")
                    pairwise_results.append({
                        "pair": f"{r1} vs {r2}",
                        "t": round(float(t), 4),
                        "p_adj": round(float(p_adj), 6),
                    })
            results["pairwise"] = pairwise_results

    # By category within regions
    print("\n  --- BAT Height by Region ---")
    bat_region = subset[subset["category"] == "BAT"]
    if len(bat_region) > 0:
        bat_stats = bat_region.groupby("region")["height_cm"].agg(
            ["count", "mean", "std"]
        ).round(2)
        print(bat_stats.to_string())

    return results


def table7_breakpoint(df: pd.DataFrame) -> dict:
    """Table 7: Segmented regression with Chow test for breakpoint."""
    print_header("TABLE 7: Breakpoint Analysis (Segmented Regression + Chow Test)")

    if not HAS_STATSMODELS:
        print("  Skipped: statsmodels not available.")
        return {}

    results = {}
    candidate_years = [1996, 1999, 2003, 2007, 2010, 2012]

    for cat in ["BAT", "FAST", "ALL"]:
        if cat == "ALL":
            subset = df.dropna(subset=["height_cm", "tournament_year"])
        else:
            subset = df[df["category"] == cat].dropna(
                subset=["height_cm", "tournament_year"]
            )

        if len(subset) < 10:
            print(f"\n  {cat}: Insufficient data")
            continue

        print(f"\n  {cat} (n={len(subset)}):")

        best_bp = None
        best_f = -1
        best_p = 1.0

        for bp in candidate_years:
            pre = subset[subset["tournament_year"] <= bp]
            post = subset[subset["tournament_year"] > bp]

            if len(pre) < 5 or len(post) < 5:
                continue

            # Full model (pooled)
            try:
                model_full = smf.ols("height_cm ~ tournament_year", data=subset).fit()
                rss_full = model_full.ssr

                # Restricted models (separate regressions)
                model_pre = smf.ols("height_cm ~ tournament_year", data=pre).fit()
                model_post = smf.ols("height_cm ~ tournament_year", data=post).fit()
                rss_restricted = model_pre.ssr + model_post.ssr

                # Chow test
                k = 2  # number of parameters
                n = len(subset)
                f_stat = ((rss_full - rss_restricted) / k) / (rss_restricted / (n - 2 * k))
                p_value = 1 - stats.f.cdf(f_stat, k, n - 2 * k)

                sig = "*" if p_value < 0.05 else ""
                print(f"    Breakpoint {bp}: F={f_stat:.4f}, p={p_value:.4f} {sig}")

                if f_stat > best_f:
                    best_f = f_stat
                    best_p = p_value
                    best_bp = bp

            except Exception as e:
                print(f"    Breakpoint {bp}: Error - {e}")

        if best_bp:
            results[cat] = {
                "best_breakpoint": best_bp,
                "f_statistic": round(float(best_f), 4),
                "p_value": round(float(best_p), 6),
                "significant": best_p < 0.05,
            }
            print(f"    >>> Best breakpoint: {best_bp} (F={best_f:.4f}, p={best_p:.4f})")

            # Segmented regression details
            pre = subset[subset["tournament_year"] <= best_bp]
            post = subset[subset["tournament_year"] > best_bp]
            res_pre = safe_ols("height_cm ~ tournament_year", pre)
            res_post = safe_ols("height_cm ~ tournament_year", post)
            if res_pre:
                print(f"    Pre-{best_bp} slope: "
                      f"{format_coef(res_pre['coefficients'], 'tournament_year')}")
                results[cat]["pre_slope"] = res_pre["coefficients"].get(
                    "tournament_year", {}
                ).get("estimate")
            if res_post:
                print(f"    Post-{best_bp} slope: "
                      f"{format_coef(res_post['coefficients'], 'tournament_year')}")
                results[cat]["post_slope"] = res_post["coefficients"].get(
                    "tournament_year", {}
                ).get("estimate")

    return results


def table8_two_way_anova(df: pd.DataFrame) -> dict:
    """Table 8: Two-way ANOVA Category x Era."""
    print_header("TABLE 8: Two-way ANOVA (Category x Era)")

    results = {}
    subset = df.dropna(subset=["height_cm", "category", "era"]).copy()
    subset["era"] = subset["era"].astype(str)

    if len(subset) < 10:
        print("  Insufficient data.")
        return results

    if HAS_STATSMODELS:
        try:
            model = smf.ols("height_cm ~ C(category) * C(era)", data=subset).fit()
            anova_table = sm.stats.anova_lm(model, typ=2)
            print(anova_table.to_string())
            results["anova_table"] = {
                str(k): {
                    "sum_sq": round(float(v["sum_sq"]), 4) if not pd.isna(v["sum_sq"]) else None,
                    "df": round(float(v["df"]), 1),
                    "F": round(float(v["F"]), 4) if not pd.isna(v["F"]) else None,
                    "PR(>F)": round(float(v["PR(>F)"]), 6) if not pd.isna(v["PR(>F)"]) else None,
                }
                for k, v in anova_table.iterrows()
            }

            # Effect sizes (eta-squared)
            ss_total = anova_table["sum_sq"].sum()
            print("\n  Effect sizes (eta-squared):")
            for factor in anova_table.index:
                if factor != "Residual":
                    eta_sq = anova_table.loc[factor, "sum_sq"] / ss_total
                    print(f"    {factor}: eta2 = {eta_sq:.4f}")

        except Exception as e:
            print(f"  Error: {e}")
    elif HAS_PINGOUIN:
        try:
            aov = pg.anova(
                data=subset, dv="height_cm",
                between=["category", "era"],
                detailed=True,
            )
            print(aov.to_string())
        except Exception as e:
            print(f"  Error: {e}")
    else:
        print("  Skipped: neither statsmodels nor pingouin available.")

    return results


def table9_mixed_effects(df: pd.DataFrame) -> dict:
    """Table 9: Mixed-effects model with Nation as random intercept."""
    print_header("TABLE 9: Mixed-Effects Model (Nation as Random Intercept)")

    if not HAS_STATSMODELS:
        print("  Skipped: statsmodels not available.")
        return {}

    results = {}
    subset = df.dropna(subset=["height_cm", "tournament_year", "country"]).copy()

    if len(subset) < 10:
        print("  Insufficient data.")
        return results

    # Ensure at least 2 groups
    if subset["country"].nunique() < 2:
        print("  Need at least 2 countries for mixed model.")
        return results

    try:
        # Model 1: Random intercept for nation
        print("\n  Model 1: height ~ year + category (random intercept: country)")
        subset_m1 = subset.dropna(subset=["height_cm", "tournament_year", "category"])
        # Create dummy variables for category
        subset_m1 = pd.get_dummies(subset_m1, columns=["category"], drop_first=True, dtype=float)

        cat_cols = [c for c in subset_m1.columns if c.startswith("category_")]
        formula_vars = ["tournament_year"] + cat_cols
        exog_cols = ["tournament_year"] + cat_cols

        X = subset_m1[exog_cols].copy()
        X.insert(0, "Intercept", 1.0)
        y = subset_m1["height_cm"]
        groups = subset_m1["country"]

        model = MixedLM(y, X, groups=groups)
        fit = model.fit(reml=True)
        print(fit.summary())

        results["model1"] = {
            "converged": fit.converged,
            "n": int(fit.nobs),
            "n_groups": int(fit.k_re),
            "log_likelihood": round(float(fit.llf), 4),
            "aic": round(float(fit.aic), 4),
            "bic": round(float(fit.bic), 4),
            "fixed_effects": {},
        }
        for param in fit.fe_params.index:
            results["model1"]["fixed_effects"][param] = {
                "estimate": round(float(fit.fe_params[param]), 4),
                "std_err": round(float(fit.bse_fe[param]), 4) if param in fit.bse_fe else None,
            }

        # Model 2: With population height
        subset_m2 = subset.dropna(
            subset=["height_cm", "tournament_year", "pop_height_birth_cohort"]
        )
        if len(subset_m2) >= 10 and subset_m2["country"].nunique() >= 2:
            print("\n  Model 2: height ~ year + pop_height + category "
                  "(random intercept: country)")
            subset_m2 = pd.get_dummies(subset_m2, columns=["category"], drop_first=True, dtype=float)
            cat_cols2 = [c for c in subset_m2.columns if c.startswith("category_")]
            exog_cols2 = ["tournament_year", "pop_height_birth_cohort"] + cat_cols2

            X2 = subset_m2[exog_cols2].copy()
            X2.insert(0, "Intercept", 1.0)
            y2 = subset_m2["height_cm"]
            groups2 = subset_m2["country"]

            model2 = MixedLM(y2, X2, groups=groups2)
            fit2 = model2.fit(reml=True)
            print(fit2.summary())

            results["model2"] = {
                "converged": fit2.converged,
                "n": int(fit2.nobs),
                "log_likelihood": round(float(fit2.llf), 4),
                "aic": round(float(fit2.aic), 4),
                "bic": round(float(fit2.bic), 4),
            }

    except Exception as e:
        print(f"  Mixed model error: {e}")
        import traceback
        traceback.print_exc()

    return results


def table10_sensitivity(df: pd.DataFrame) -> dict:
    """Sensitivity analyses."""
    print_header("TABLE 10: Sensitivity Analyses")

    results = {}

    # 1. Verified-only analysis
    print("\n  --- 1. Verified heights only ---")
    verified = df[df["height_verified"] == True]
    if len(verified) > 0:
        res = safe_ols("height_cm ~ tournament_year", verified)
        if res:
            print(f"    n={res['n']}, R2={res['r_squared']:.4f}")
            print(f"    Slope: {format_coef(res['coefficients'], 'tournament_year')}")
            results["verified_only"] = res

    # 2. Exclude flagged players
    print("\n  --- 2. Exclude flagged players ---")
    unflagged = df[df["flag"].isna() | (df["flag"] == "")]
    if len(unflagged) > 0:
        res = safe_ols("height_cm ~ tournament_year", unflagged)
        if res:
            print(f"    n={res['n']}, R2={res['r_squared']:.4f}")
            print(f"    Slope: {format_coef(res['coefficients'], 'tournament_year')}")
            results["unflagged_only"] = res

    # 3. ODI-only analysis
    print("\n  --- 3. ODI format only ---")
    odi = df[df["format"] == "ODI"]
    if len(odi) >= 5:
        res = safe_ols("height_cm ~ tournament_year", odi)
        if res:
            print(f"    n={res['n']}, R2={res['r_squared']:.4f}")
            print(f"    Slope: {format_coef(res['coefficients'], 'tournament_year')}")
            results["odi_only"] = res

    # 4. T20-only analysis
    print("\n  --- 4. T20 format only ---")
    t20 = df[df["format"] == "T20"]
    if len(t20) >= 5:
        res = safe_ols("height_cm ~ tournament_year", t20)
        if res:
            print(f"    n={res['n']}, R2={res['r_squared']:.4f}")
            print(f"    Slope: {format_coef(res['coefficients'], 'tournament_year')}")
            results["t20_only"] = res

    # 5. Format comparison (ODI vs T20, 2007+ only)
    print("\n  --- 5. ODI vs T20 comparison (2007+ only) ---")
    recent = df[df["tournament_year"] >= 2007].dropna(subset=["height_cm"])
    if len(recent) >= 5 and recent["format"].nunique() >= 2:
        odi_heights = recent[recent["format"] == "ODI"]["height_cm"]
        t20_heights = recent[recent["format"] == "T20"]["height_cm"]
        if len(odi_heights) >= 3 and len(t20_heights) >= 3:
            t, p = stats.ttest_ind(odi_heights, t20_heights, equal_var=False)
            d = (odi_heights.mean() - t20_heights.mean()) / np.sqrt(
                (odi_heights.std() ** 2 + t20_heights.std() ** 2) / 2
            )
            print(f"    ODI:  mean={odi_heights.mean():.2f}, n={len(odi_heights)}")
            print(f"    T20:  mean={t20_heights.mean():.2f}, n={len(t20_heights)}")
            print(f"    t={t:.4f}, p={p:.4f}, Cohen's d={d:.4f}")
            results["format_comparison"] = {
                "odi_mean": round(float(odi_heights.mean()), 2),
                "odi_n": int(len(odi_heights)),
                "t20_mean": round(float(t20_heights.mean()), 2),
                "t20_n": int(len(t20_heights)),
                "t_statistic": round(float(t), 4),
                "p_value": round(float(p), 6),
                "cohens_d": round(float(d), 4),
            }

    # 6. Effect size: FAST vs BAT
    print("\n  --- 6. FAST vs BAT effect size ---")
    fast = df[df["category"] == "FAST"]["height_cm"].dropna()
    bat = df[df["category"] == "BAT"]["height_cm"].dropna()
    if len(fast) >= 3 and len(bat) >= 3:
        diff = fast.mean() - bat.mean()
        pooled_sd = np.sqrt((fast.std() ** 2 + bat.std() ** 2) / 2)
        d = diff / pooled_sd if pooled_sd > 0 else 0
        t, p = stats.ttest_ind(fast, bat, equal_var=False)
        print(f"    FAST: mean={fast.mean():.2f}, sd={fast.std():.2f}, n={len(fast)}")
        print(f"    BAT:  mean={bat.mean():.2f}, sd={bat.std():.2f}, n={len(bat)}")
        print(f"    Difference: {diff:.2f} cm, Cohen's d={d:.4f}")
        print(f"    t={t:.4f}, p={p:.6f}")
        results["fast_vs_bat"] = {
            "fast_mean": round(float(fast.mean()), 2),
            "bat_mean": round(float(bat.mean()), 2),
            "difference": round(float(diff), 2),
            "cohens_d": round(float(d), 4),
            "t_statistic": round(float(t), 4),
            "p_value": round(float(p), 6),
        }

    return results


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    if not MERGED_CSV.exists():
        print(f"ERROR: Merged CSV not found: {MERGED_CSV}")
        print("       Run merge_all_tournaments.py first.")
        sys.exit(1)

    df = pd.read_csv(MERGED_CSV)
    print(f"Loaded {len(df)} player-tournament records from {MERGED_CSV}")
    print(f"Columns: {list(df.columns)}")

    # Ensure numeric types
    for col in ["height_cm", "tournament_year", "birth_year", "age_at_tournament",
                 "pop_height_birth_cohort", "height_excess", "era"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Filter to valid height data
    df_valid = df[df["height_cm"].notna()].copy()
    print(f"Records with valid height: {len(df_valid)}")

    if len(df_valid) == 0:
        print("ERROR: No records with valid height data.")
        sys.exit(1)

    # ------------------------------------------------------------------
    # Run all analyses
    # ------------------------------------------------------------------
    all_results = {}

    all_results["table2_descriptive"] = table2_descriptive(df_valid)
    all_results["table3_unadjusted"] = table3_unadjusted_regression(df_valid)
    all_results["table4_adjusted"] = table4_adjusted_regression(df_valid)
    all_results["table5_country"] = table5_country_regression(df_valid)
    all_results["table6_regional"] = table6_regional_anova(df_valid)
    all_results["table7_breakpoint"] = table7_breakpoint(df_valid)
    all_results["table8_two_way_anova"] = table8_two_way_anova(df_valid)
    all_results["table9_mixed_effects"] = table9_mixed_effects(df_valid)
    all_results["table10_sensitivity"] = table10_sensitivity(df_valid)

    # ------------------------------------------------------------------
    # Save results
    # ------------------------------------------------------------------
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)

    # Convert any numpy types for JSON serialization
    def convert_numpy(obj):
        if isinstance(obj, (np.integer,)):
            return int(obj)
        elif isinstance(obj, (np.floating,)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, pd.Timestamp):
            return str(obj)
        elif isinstance(obj, (np.bool_,)):
            return bool(obj)
        return obj

    class NumpyEncoder(json.JSONEncoder):
        def default(self, obj):
            converted = convert_numpy(obj)
            if converted is not obj:
                return converted
            return super().default(obj)

    with open(OUTPUT_JSON, "w", encoding="utf-8") as fh:
        json.dump(all_results, fh, indent=2, cls=NumpyEncoder, default=str)

    print(f"\n\nResults saved to: {OUTPUT_JSON}")
    print("Done.")


if __name__ == "__main__":
    main()
