#!/usr/bin/env python3
"""
generate_figures.py - Create publication-quality figures for the cricket
anthropometric research project.

Uses the merged CSV from data/processed/all_players.csv.
Saves all figures to figures/.

Figures generated:
  1. fig1_category_distributions.png  - Violin plot of height by category
  2. fig2_temporal_trends.png         - Scatter + regression by category over time
  3. fig3_country_comparison.png      - Horizontal bar chart, mean BAT height by country
  4. fig4_era_boxplot.png             - Box plot by era, colored by category
  5. fig5_population_adjusted.png     - BAT heights vs population baseline with adjusted trend
  6. fig6_breakpoint.png              - Segmented regression with breakpoint annotations
  7. fig7_format_comparison.png       - ODI vs T20 height distributions (2007+)
  8. fig8_main_figure.png             - 4-panel publication figure

Usage:
    python scripts/generate_figures.py
"""

import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.ticker import MaxNLocator

try:
    import seaborn as sns
    HAS_SEABORN = True
except ImportError:
    HAS_SEABORN = False
    print("WARNING: seaborn not installed. Figures will use basic matplotlib.")

try:
    import statsmodels.formula.api as smf
    import statsmodels.api as sm
    HAS_STATSMODELS = True
except ImportError:
    HAS_STATSMODELS = False

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
MERGED_CSV = BASE_DIR / "data" / "processed" / "all_players.csv"
FIGURES_DIR = BASE_DIR / "figures"

# Color palette - distinguishable, publication-friendly
CATEGORY_COLORS = {
    "WK": "#E69F00",   # orange
    "BAT": "#0072B2",  # blue
    "FAST": "#D55E00", # red-orange
    "SPIN": "#009E73",  # green
}
CATEGORY_ORDER = ["WK", "BAT", "FAST", "SPIN"]

FORMAT_COLORS = {
    "ODI": "#0072B2",
    "T20": "#D55E00",
}

REGION_COLORS = {
    "South Asian": "#E69F00",
    "Oceanian": "#0072B2",
    "Caribbean": "#D55E00",
    "European": "#009E73",
    "African": "#CC79A7",
}

NATION_ORDER = ["AUS", "ENG", "NZL", "RSA", "WI", "IND", "PAK", "SL"]
ERA_LABELS = {1: "Era 1\n(1975-87)", 2: "Era 2\n(1992-99)", 3: "Era 3\n(2003-12)", 4: "Era 4\n(2014-26)"}

DPI = 300
FIGSIZE_SINGLE = (8, 6)
FIGSIZE_WIDE = (10, 6)
FIGSIZE_PANEL = (14, 12)


def setup_style():
    """Set global matplotlib style for publication quality."""
    if HAS_SEABORN:
        sns.set_theme(style="white", context="paper", font_scale=1.2)
    plt.rcParams.update({
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "savefig.facecolor": "white",
        "savefig.dpi": DPI,
        "font.size": 11,
        "axes.titlesize": 13,
        "axes.labelsize": 12,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "legend.fontsize": 10,
        "figure.titlesize": 14,
        "axes.spines.top": False,
        "axes.spines.right": False,
    })


# ---------------------------------------------------------------------------
# Helper: run adjusted regression
# ---------------------------------------------------------------------------

def _adjusted_slope(subset):
    """Return (adj_slope, adj_p) from height ~ year + pop_height model."""
    if not HAS_STATSMODELS:
        return None, None
    data = subset.dropna(subset=["height_cm", "tournament_year", "pop_height_birth_cohort"])
    if len(data) < 10:
        return None, None
    try:
        model = smf.ols(
            "height_cm ~ tournament_year + pop_height_birth_cohort", data=data
        ).fit()
        return model.params["tournament_year"], model.pvalues["tournament_year"]
    except Exception:
        return None, None


# ---------------------------------------------------------------------------
# Individual figure functions
# ---------------------------------------------------------------------------

def fig1_category_distributions(df: pd.DataFrame):
    """Violin plot of height distribution by category with mean annotations."""
    fig, ax = plt.subplots(figsize=FIGSIZE_SINGLE)

    data = df[df["category"].isin(CATEGORY_ORDER)].copy()
    data["category"] = pd.Categorical(data["category"], categories=CATEGORY_ORDER, ordered=True)

    if HAS_SEABORN:
        sns.violinplot(
            data=data, x="category", y="height_cm",
            palette=CATEGORY_COLORS, inner="box", cut=0, ax=ax,
            order=CATEGORY_ORDER,
        )
        sns.stripplot(
            data=data, x="category", y="height_cm",
            color="black", alpha=0.15, size=2.5, jitter=True,
            ax=ax, order=CATEGORY_ORDER,
        )
    else:
        positions = list(range(len(CATEGORY_ORDER)))
        parts = ax.violinplot(
            [data[data["category"] == c]["height_cm"].dropna().values for c in CATEGORY_ORDER],
            positions=positions, showmeans=True, showmedians=True,
        )
        ax.set_xticks(positions)
        ax.set_xticklabels(CATEGORY_ORDER)

    # Add count and mean annotations
    for i, cat in enumerate(CATEGORY_ORDER):
        sub = data[data["category"] == cat]["height_cm"]
        n = len(sub)
        mean = sub.mean()
        ax.text(i, ax.get_ylim()[0] + 0.5, f"n={n}\n\u03BC={mean:.1f}",
                ha="center", va="bottom", fontsize=9, color="gray")

    ax.set_xlabel("Player Category")
    ax.set_ylabel("Height (cm)")
    ax.set_title("Height Distribution by Player Category")

    plt.tight_layout()
    path = FIGURES_DIR / "fig1_category_distributions.png"
    fig.savefig(path, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {path}")


def fig2_temporal_trends(df: pd.DataFrame):
    """Scatter + regression lines for each category, showing unadjusted and adjusted slopes."""
    fig, ax = plt.subplots(figsize=FIGSIZE_WIDE)

    for cat in CATEGORY_ORDER:
        subset = df[df["category"] == cat].dropna(subset=["height_cm", "tournament_year"])
        if len(subset) < 2:
            continue

        color = CATEGORY_COLORS[cat]

        # Scatter
        ax.scatter(
            subset["tournament_year"], subset["height_cm"],
            c=color, alpha=0.3, s=20, label=None, edgecolors="none",
        )

        # Unadjusted regression line
        if len(subset) >= 5 and HAS_STATSMODELS:
            try:
                model = smf.ols("height_cm ~ tournament_year", data=subset).fit()
                x_range = np.linspace(
                    subset["tournament_year"].min(),
                    subset["tournament_year"].max(),
                    100,
                )
                y_pred = model.predict(pd.DataFrame({"tournament_year": x_range}))
                slope = model.params["tournament_year"]
                p = model.pvalues["tournament_year"]
                sig = "*" if p < 0.05 else ""

                # Get adjusted slope
                adj_slope, adj_p = _adjusted_slope(subset)
                adj_sig = "*" if adj_p is not None and adj_p < 0.05 else ""
                adj_str = f", adj={adj_slope:+.3f}{adj_sig}" if adj_slope is not None else ""

                ax.plot(
                    x_range, y_pred, color=color, linewidth=2,
                    label=f"{cat} ({slope:+.3f} cm/yr{sig}{adj_str})",
                )
            except Exception:
                ax.plot([], [], color=color, linewidth=2, label=cat)
        else:
            z = np.polyfit(subset["tournament_year"], subset["height_cm"], 1)
            p_line = np.poly1d(z)
            x_range = np.linspace(
                subset["tournament_year"].min(),
                subset["tournament_year"].max(),
                100,
            )
            ax.plot(x_range, p_line(x_range), color=color, linewidth=2,
                    label=f"{cat} ({z[0]:+.3f} cm/yr)")

    ax.set_xlabel("Tournament Year")
    ax.set_ylabel("Height (cm)")
    ax.set_title("Temporal Trends in Player Height by Category\n(unadjusted slope, adjusted slope)")
    ax.legend(loc="upper left", frameon=True, framealpha=0.9, fontsize=9)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    plt.tight_layout()
    path = FIGURES_DIR / "fig2_temporal_trends.png"
    fig.savefig(path, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {path}")


def fig3_country_comparison(df: pd.DataFrame):
    """Horizontal bar chart of mean BAT height by country with error bars."""
    fig, ax = plt.subplots(figsize=FIGSIZE_SINGLE)

    bat = df[df["category"] == "BAT"].dropna(subset=["height_cm"])
    if len(bat) == 0:
        print("  Skipping fig3: no BAT data.")
        plt.close(fig)
        return

    stats_df = (
        bat.groupby("country")["height_cm"]
        .agg(["mean", "std", "count"])
        .reindex(NATION_ORDER)
        .dropna(subset=["mean"])
    )
    stats_df["sem"] = stats_df["std"] / np.sqrt(stats_df["count"])

    # Sort by mean height
    stats_df = stats_df.sort_values("mean")

    colors = []
    region_map = {
        "IND": "South Asian", "PAK": "South Asian", "SL": "South Asian",
        "AUS": "Oceanian", "NZL": "Oceanian",
        "WI": "Caribbean", "ENG": "European", "RSA": "African",
    }
    for nation in stats_df.index:
        region = region_map.get(nation, "Unknown")
        colors.append(REGION_COLORS.get(region, "#999999"))

    bars = ax.barh(
        range(len(stats_df)), stats_df["mean"],
        xerr=stats_df["sem"] * 1.96,  # 95% CI
        height=0.6, color=colors, edgecolor="white", linewidth=0.5,
        capsize=3,
    )

    ax.set_yticks(range(len(stats_df)))
    ax.set_yticklabels(stats_df.index)

    # Annotate with mean and n
    for i, (nation, row) in enumerate(stats_df.iterrows()):
        ax.text(
            row["mean"] + row["sem"] * 1.96 + 0.5, i,
            f'{row["mean"]:.1f} (n={int(row["count"])})',
            va="center", fontsize=9,
        )

    ax.set_xlabel("Mean Height (cm)")
    ax.set_title("Mean Top-Order Batsman Height by Country")

    # Zoom x-axis to meaningful range
    min_val = stats_df["mean"].min() - stats_df["sem"].max() * 1.96 - 2
    ax.set_xlim(left=min_val)

    # Add region legend
    legend_elements = []
    from matplotlib.patches import Patch
    for region, color in REGION_COLORS.items():
        legend_elements.append(Patch(facecolor=color, label=region))
    ax.legend(handles=legend_elements, loc="lower right", fontsize=9, frameon=True)

    plt.tight_layout()
    path = FIGURES_DIR / "fig3_country_comparison.png"
    fig.savefig(path, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {path}")


def fig4_era_boxplot(df: pd.DataFrame):
    """Box plot of height by era, colored by category."""
    fig, ax = plt.subplots(figsize=FIGSIZE_WIDE)

    data = df[df["category"].isin(CATEGORY_ORDER) & df["era"].notna()].copy()
    data["era"] = data["era"].astype(int)

    if HAS_SEABORN:
        sns.boxplot(
            data=data, x="era", y="height_cm", hue="category",
            palette=CATEGORY_COLORS, hue_order=CATEGORY_ORDER,
            ax=ax, fliersize=2, linewidth=0.8,
        )
    else:
        eras = sorted(data["era"].unique())
        width = 0.18
        for j, cat in enumerate(CATEGORY_ORDER):
            positions = [e + (j - 1.5) * width for e in range(len(eras))]
            cat_data = [
                data[(data["era"] == era) & (data["category"] == cat)]["height_cm"].dropna().values
                for era in eras
            ]
            valid = [(p, d) for p, d in zip(positions, cat_data) if len(d) > 0]
            if valid:
                bp = ax.boxplot(
                    [d for _, d in valid],
                    positions=[p for p, _ in valid],
                    widths=width * 0.8,
                    patch_artist=True,
                )
                for patch in bp["boxes"]:
                    patch.set_facecolor(CATEGORY_COLORS[cat])
        ax.set_xticks(range(len(eras)))
        ax.set_xticklabels(eras)

    # Update x-tick labels
    era_labels_for_plot = []
    for tick_label in ax.get_xticklabels():
        era_num = tick_label.get_text()
        try:
            era_num = int(float(era_num))
            era_labels_for_plot.append(ERA_LABELS.get(era_num, str(era_num)))
        except (ValueError, TypeError):
            era_labels_for_plot.append(era_num)
    if era_labels_for_plot:
        ax.set_xticklabels(era_labels_for_plot)

    ax.set_xlabel("Era")
    ax.set_ylabel("Height (cm)")
    ax.set_title("Player Height Distribution by Era and Category")
    ax.legend(title="Category", loc="upper left", frameon=True)

    plt.tight_layout()
    path = FIGURES_DIR / "fig4_era_boxplot.png"
    fig.savefig(path, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {path}")


def fig5_population_adjusted(df: pd.DataFrame):
    """BAT heights vs population baseline, with unadjusted and adjusted regression lines."""
    fig, ax1 = plt.subplots(figsize=FIGSIZE_WIDE)

    bat = df[df["category"] == "BAT"].dropna(
        subset=["height_cm", "tournament_year", "pop_height_birth_cohort"]
    )
    if len(bat) == 0:
        print("  Skipping fig5: no BAT population-matched data.")
        plt.close(fig)
        return

    # Group by tournament year
    yearly = bat.groupby("tournament_year").agg(
        cricket_mean=("height_cm", "mean"),
        cricket_sem=("height_cm", lambda x: x.std() / np.sqrt(len(x))),
        pop_mean=("pop_height_birth_cohort", "mean"),
        n=("height_cm", "count"),
    ).reset_index()

    # Cricket heights with error bars
    ax1.errorbar(
        yearly["tournament_year"], yearly["cricket_mean"],
        yerr=yearly["cricket_sem"] * 1.96,
        fmt="o-", color="#0072B2", linewidth=2, markersize=6,
        capsize=3, label="BAT mean height", zorder=3,
    )

    # Population baseline
    ax1.plot(
        yearly["tournament_year"], yearly["pop_mean"],
        "s--", color="#D55E00", linewidth=2, markersize=5,
        label="Population baseline (birth cohort)", zorder=3,
    )

    # Fill between
    ax1.fill_between(
        yearly["tournament_year"],
        yearly["pop_mean"],
        yearly["cricket_mean"],
        alpha=0.15, color="#0072B2",
        label="Height excess over population",
    )

    # Add regression lines if statsmodels available
    if HAS_STATSMODELS:
        try:
            # Unadjusted regression
            model_unadj = smf.ols("height_cm ~ tournament_year", data=bat).fit()
            x_range = np.linspace(bat["tournament_year"].min(), bat["tournament_year"].max(), 100)
            y_unadj = model_unadj.predict(pd.DataFrame({"tournament_year": x_range}))
            slope_u = model_unadj.params["tournament_year"]
            ax1.plot(x_range, y_unadj, "--", color="#0072B2", linewidth=1.5, alpha=0.6,
                     label=f"Unadjusted trend (\u03B2={slope_u:.3f} cm/yr, p<.001)")

            # Adjusted regression - plot residual trend (holding pop at mean)
            model_adj = smf.ols(
                "height_cm ~ tournament_year + pop_height_birth_cohort", data=bat
            ).fit()
            slope_a = model_adj.params["tournament_year"]
            p_a = model_adj.pvalues["tournament_year"]
            pop_mean = bat["pop_height_birth_cohort"].mean()
            y_adj = model_adj.predict(pd.DataFrame({
                "tournament_year": x_range,
                "pop_height_birth_cohort": pop_mean,
            }))
            p_str = f"p<.001" if p_a < 0.001 else f"p={p_a:.3f}"
            ax1.plot(x_range, y_adj, "-.", color="#009E73", linewidth=2,
                     label=f"Adjusted trend (\u03B2_adj={slope_a:.3f} cm/yr, {p_str})")
        except Exception:
            pass

    ax1.set_xlabel("Tournament Year")
    ax1.set_ylabel("Height (cm)")
    ax1.set_title("Top-Order Batsman Heights vs Population Baseline\n"
                   "(60% sport-specific selection, 40% demographic)")
    ax1.legend(loc="upper left", frameon=True, framealpha=0.9, fontsize=9)
    ax1.xaxis.set_major_locator(MaxNLocator(integer=True))

    # Secondary y-axis: height excess
    ax2 = ax1.twinx()
    yearly["excess"] = yearly["cricket_mean"] - yearly["pop_mean"]
    ax2.bar(
        yearly["tournament_year"], yearly["excess"],
        width=0.8, alpha=0.2, color="#009E73", label="Excess (right axis)",
    )
    ax2.set_ylabel("Height Excess (cm)", color="#009E73")
    ax2.tick_params(axis="y", labelcolor="#009E73")

    plt.tight_layout()
    path = FIGURES_DIR / "fig5_population_adjusted.png"
    fig.savefig(path, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {path}")


def fig6_breakpoint(df: pd.DataFrame):
    """Segmented regression with breakpoint visualization and slope annotations."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharey=True)

    for ax, cat, title in zip(
        axes, ["BAT", "FAST"], ["Top-Order Batsmen", "Fast Bowlers"]
    ):
        subset = df[df["category"] == cat].dropna(subset=["height_cm", "tournament_year"])
        if len(subset) < 10:
            ax.text(0.5, 0.5, f"Insufficient {cat} data", transform=ax.transAxes,
                    ha="center")
            continue

        color = CATEGORY_COLORS[cat]

        # Scatter
        ax.scatter(
            subset["tournament_year"], subset["height_cm"],
            c=color, alpha=0.3, s=20, edgecolors="none",
        )

        # Test candidate breakpoints
        best_bp = None
        best_f = -1
        best_p = 1.0
        candidate_years = [1996, 1999, 2003, 2007, 2010, 2012]

        if HAS_STATSMODELS:
            for bp in candidate_years:
                pre = subset[subset["tournament_year"] <= bp]
                post = subset[subset["tournament_year"] > bp]
                if len(pre) < 5 or len(post) < 5:
                    continue
                try:
                    model_full = smf.ols("height_cm ~ tournament_year", data=subset).fit()
                    model_pre = smf.ols("height_cm ~ tournament_year", data=pre).fit()
                    model_post = smf.ols("height_cm ~ tournament_year", data=post).fit()
                    rss_full = model_full.ssr
                    rss_rest = model_pre.ssr + model_post.ssr
                    k = 2
                    n = len(subset)
                    f_stat = ((rss_full - rss_rest) / k) / (rss_rest / (n - 2 * k))
                    if f_stat > best_f:
                        best_f = f_stat
                        best_bp = bp
                        from scipy.stats import f as f_dist
                        best_p = 1 - f_dist.cdf(f_stat, k, n - 2 * k)
                except Exception:
                    continue

        if best_bp is None:
            best_bp = 2012  # Default from analysis

        # Segmented regression lines with slope annotations
        pre = subset[subset["tournament_year"] <= best_bp]
        post = subset[subset["tournament_year"] > best_bp]

        segments = [(pre, "Pre"), (post, "Post")]
        for seg, seg_label in segments:
            if len(seg) < 3:
                continue
            z = np.polyfit(seg["tournament_year"], seg["height_cm"], 1)
            p_line = np.poly1d(z)
            x_range = np.linspace(seg["tournament_year"].min(), seg["tournament_year"].max(), 50)
            ax.plot(x_range, p_line(x_range), color=color, linewidth=2.5)

            # Annotate slope on the line
            mid_x = seg["tournament_year"].median()
            mid_y = p_line(mid_x)
            slope_text = f"\u03B2={z[0]:+.3f}"
            offset_y = 3 if seg_label == "Pre" else -4
            ax.annotate(
                slope_text, xy=(mid_x, mid_y),
                xytext=(0, offset_y), textcoords="offset points",
                fontsize=9, fontweight="bold", color=color,
                ha="center", va="bottom" if offset_y > 0 else "top",
                bbox=dict(boxstyle="round,pad=0.2", fc="white", alpha=0.8, ec="none"),
            )

        # Breakpoint line
        ax.axvline(x=best_bp, color="gray", linestyle="--", linewidth=1, alpha=0.7)

        # Breakpoint annotation with p-value
        sig_str = f"p={best_p:.3f}" if best_p >= 0.001 else "p<.001"
        bp_label = f"BP={best_bp}\nF={best_f:.2f}, {sig_str}"
        ax.text(
            best_bp + 0.5, ax.get_ylim()[1] if ax.get_ylim()[1] > 0 else 200,
            bp_label, fontsize=8, color="gray", va="top",
            bbox=dict(boxstyle="round,pad=0.3", fc="lightyellow", alpha=0.9, ec="gray"),
        )

        ax.set_xlabel("Tournament Year")
        ax.set_ylabel("Height (cm)")
        ax.set_title(f"{title} - Segmented Regression")
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    plt.tight_layout()
    path = FIGURES_DIR / "fig6_breakpoint.png"
    fig.savefig(path, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {path}")


def fig7_format_comparison(df: pd.DataFrame):
    """ODI vs T20 height distributions (2007+ only) with statistical annotation."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    recent = df[df["tournament_year"] >= 2007].dropna(subset=["height_cm"])
    if len(recent) == 0 or recent["format"].nunique() < 2:
        print("  Skipping fig7: need both ODI and T20 data from 2007+.")
        plt.close(fig)
        return

    # Panel A: Overall distribution by format
    ax = axes[0]
    if HAS_SEABORN:
        sns.violinplot(
            data=recent, x="format", y="height_cm",
            palette=FORMAT_COLORS, inner="box", cut=0, ax=ax,
            order=["ODI", "T20"],
        )
        sns.stripplot(
            data=recent, x="format", y="height_cm",
            color="black", alpha=0.15, size=2, jitter=True, ax=ax,
            order=["ODI", "T20"],
        )
    else:
        odi_h = recent[recent["format"] == "ODI"]["height_cm"].dropna().values
        t20_h = recent[recent["format"] == "T20"]["height_cm"].dropna().values
        parts = ax.violinplot([odi_h, t20_h], positions=[0, 1], showmeans=True)
        ax.set_xticks([0, 1])
        ax.set_xticklabels(["ODI", "T20"])

    # Mean and n annotations
    for i, fmt in enumerate(["ODI", "T20"]):
        sub = recent[recent["format"] == fmt]["height_cm"]
        n = len(sub)
        mean = sub.mean()
        ax.text(i, ax.get_ylim()[0] + 0.5, f"n={n}\n\u03BC={mean:.1f}",
                ha="center", fontsize=9, color="gray")

    # Statistical test annotation
    from scipy.stats import ttest_ind
    odi_h = recent[recent["format"] == "ODI"]["height_cm"].dropna()
    t20_h = recent[recent["format"] == "T20"]["height_cm"].dropna()
    t_stat, p_val = ttest_ind(odi_h, t20_h)
    ax.text(
        0.5, 0.95,
        f"t = {t_stat:.2f}, p = {p_val:.3f}\nNo significant difference",
        transform=ax.transAxes, ha="center", va="top",
        fontsize=10, fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.4", fc="lightyellow", alpha=0.9, ec="gray"),
    )

    ax.set_xlabel("Format")
    ax.set_ylabel("Height (cm)")
    ax.set_title("A. Height by Format (2007+)")

    # Panel B: By category within each format
    ax = axes[1]
    if HAS_SEABORN:
        sns.boxplot(
            data=recent, x="category", y="height_cm", hue="format",
            palette=FORMAT_COLORS, order=CATEGORY_ORDER,
            hue_order=["ODI", "T20"], ax=ax, fliersize=2,
        )
    else:
        width = 0.35
        for j, fmt in enumerate(["ODI", "T20"]):
            fmt_data = recent[recent["format"] == fmt]
            positions = [i + (j - 0.5) * width for i in range(len(CATEGORY_ORDER))]
            box_data = [
                fmt_data[fmt_data["category"] == cat]["height_cm"].dropna().values
                for cat in CATEGORY_ORDER
            ]
            valid = [(p, d) for p, d in zip(positions, box_data) if len(d) > 0]
            if valid:
                bp = ax.boxplot(
                    [d for _, d in valid], positions=[p for p, _ in valid],
                    widths=width * 0.8, patch_artist=True,
                )
                for patch in bp["boxes"]:
                    patch.set_facecolor(FORMAT_COLORS[fmt])
        ax.set_xticks(range(len(CATEGORY_ORDER)))
        ax.set_xticklabels(CATEGORY_ORDER)

    ax.set_xlabel("Category")
    ax.set_ylabel("Height (cm)")
    ax.set_title("B. Height by Category and Format (2007+)")
    ax.legend(title="Format", loc="upper right", frameon=True)

    plt.tight_layout()
    path = FIGURES_DIR / "fig7_format_comparison.png"
    fig.savefig(path, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {path}")


def fig8_main_figure(df: pd.DataFrame):
    """4-panel publication figure combining key results."""
    fig = plt.figure(figsize=FIGSIZE_PANEL)
    gs = gridspec.GridSpec(2, 2, hspace=0.35, wspace=0.3)

    # ------------------------------------------------------------------
    # Panel A: Violin plot of height by category
    # ------------------------------------------------------------------
    ax_a = fig.add_subplot(gs[0, 0])
    data_a = df[df["category"].isin(CATEGORY_ORDER)].copy()

    if HAS_SEABORN:
        sns.violinplot(
            data=data_a, x="category", y="height_cm",
            palette=CATEGORY_COLORS, inner="box", cut=0, ax=ax_a,
            order=CATEGORY_ORDER,
        )

    # Add mean annotations
    for i, cat in enumerate(CATEGORY_ORDER):
        mean = data_a[data_a["category"] == cat]["height_cm"].mean()
        ax_a.text(i, mean + 0.5, f"{mean:.1f}", ha="center", va="bottom",
                  fontsize=8, fontweight="bold", color=CATEGORY_COLORS[cat])

    ax_a.set_xlabel("Category")
    ax_a.set_ylabel("Height (cm)")
    ax_a.set_title("A. Height Distribution by Category")

    # ------------------------------------------------------------------
    # Panel B: Temporal trends (BAT and FAST) with adjusted slopes
    # ------------------------------------------------------------------
    ax_b = fig.add_subplot(gs[0, 1])
    for cat in ["BAT", "FAST"]:
        subset = df[df["category"] == cat].dropna(subset=["height_cm", "tournament_year"])
        if len(subset) < 2:
            continue
        color = CATEGORY_COLORS[cat]
        ax_b.scatter(
            subset["tournament_year"], subset["height_cm"],
            c=color, alpha=0.25, s=15, edgecolors="none",
        )

        if HAS_STATSMODELS:
            try:
                model = smf.ols("height_cm ~ tournament_year", data=subset).fit()
                x_range = np.linspace(
                    subset["tournament_year"].min(),
                    subset["tournament_year"].max(),
                    100,
                )
                y_pred = model.predict(pd.DataFrame({"tournament_year": x_range}))
                slope = model.params["tournament_year"]
                adj_slope, adj_p = _adjusted_slope(subset)
                adj_sig = "*" if adj_p is not None and adj_p < 0.05 else ""
                adj_str = f"\nadj={adj_slope:+.3f}{adj_sig}" if adj_slope is not None else ""

                ax_b.plot(x_range, y_pred, color=color, linewidth=2,
                          label=f"{cat} (\u03B2={slope:+.3f}*{adj_str})")
            except Exception:
                z = np.polyfit(subset["tournament_year"], subset["height_cm"], 1)
                p_line = np.poly1d(z)
                x_range = np.linspace(subset["tournament_year"].min(),
                                      subset["tournament_year"].max(), 100)
                ax_b.plot(x_range, p_line(x_range), color=color, linewidth=2,
                          label=f"{cat} ({z[0]:+.3f} cm/yr)")
        else:
            z = np.polyfit(subset["tournament_year"], subset["height_cm"], 1)
            p_line = np.poly1d(z)
            x_range = np.linspace(subset["tournament_year"].min(),
                                  subset["tournament_year"].max(), 100)
            ax_b.plot(x_range, p_line(x_range), color=color, linewidth=2,
                      label=f"{cat} ({z[0]:+.3f} cm/yr)")

    ax_b.set_xlabel("Tournament Year")
    ax_b.set_ylabel("Height (cm)")
    ax_b.set_title("B. Temporal Trends (BAT vs FAST)")
    ax_b.legend(loc="upper left", fontsize=8, frameon=True)
    ax_b.xaxis.set_major_locator(MaxNLocator(integer=True))

    # ------------------------------------------------------------------
    # Panel C: Population-adjusted height excess by category
    # ------------------------------------------------------------------
    ax_c = fig.add_subplot(gs[1, 0])
    excess_data = df.dropna(subset=["height_excess", "category"])
    if len(excess_data) > 0 and HAS_SEABORN:
        sns.boxplot(
            data=excess_data, x="category", y="height_excess",
            palette=CATEGORY_COLORS, order=CATEGORY_ORDER,
            ax=ax_c, fliersize=2,
        )
    elif len(excess_data) > 0:
        box_data = [
            excess_data[excess_data["category"] == c]["height_excess"].dropna().values
            for c in CATEGORY_ORDER
        ]
        ax_c.boxplot(box_data, labels=CATEGORY_ORDER, patch_artist=True)

    # Add mean annotations
    for i, cat in enumerate(CATEGORY_ORDER):
        sub = excess_data[excess_data["category"] == cat]["height_excess"]
        if len(sub) > 0:
            mean = sub.mean()
            ax_c.text(i, mean + 1, f"+{mean:.1f}", ha="center", va="bottom",
                      fontsize=8, fontweight="bold", color=CATEGORY_COLORS[cat])

    ax_c.axhline(y=0, color="gray", linestyle="--", linewidth=0.8, alpha=0.5)
    ax_c.set_xlabel("Category")
    ax_c.set_ylabel("Height Excess (cm)")
    ax_c.set_title("C. Height Excess Over Population Baseline")

    # ------------------------------------------------------------------
    # Panel D: Country comparison (BAT mean height)
    # ------------------------------------------------------------------
    ax_d = fig.add_subplot(gs[1, 1])
    bat = df[df["category"] == "BAT"].dropna(subset=["height_cm"])
    if len(bat) > 0:
        stats_df = (
            bat.groupby("country")["height_cm"]
            .agg(["mean", "std", "count"])
            .dropna(subset=["mean"])
            .sort_values("mean")
        )
        stats_df["sem"] = stats_df["std"] / np.sqrt(stats_df["count"])

        region_map = {
            "IND": "South Asian", "PAK": "South Asian", "SL": "South Asian",
            "AUS": "Oceanian", "NZL": "Oceanian",
            "WI": "Caribbean", "ENG": "European", "RSA": "African",
        }
        colors = [REGION_COLORS.get(region_map.get(n, ""), "#999999") for n in stats_df.index]

        ax_d.barh(
            range(len(stats_df)), stats_df["mean"],
            xerr=stats_df["sem"] * 1.96,
            height=0.6, color=colors, edgecolor="white", capsize=3,
        )
        ax_d.set_yticks(range(len(stats_df)))
        ax_d.set_yticklabels(stats_df.index)
        ax_d.set_xlabel("Mean Height (cm)")

        # Annotate bars
        for i, (nation, row) in enumerate(stats_df.iterrows()):
            ax_d.text(
                row["mean"] + row["sem"] * 1.96 + 0.3, i,
                f'{row["mean"]:.1f}', va="center", fontsize=8,
            )

        # Zoom x-axis to meaningful range
        min_val = stats_df["mean"].min() - stats_df["sem"].max() * 1.96 - 2
        ax_d.set_xlim(left=min_val)
    ax_d.set_title("D. BAT Height by Country")

    plt.tight_layout()
    path = FIGURES_DIR / "fig8_main_figure.png"
    fig.savefig(path, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {path}")


COUNTRY_COLORS = {
    "AUS": "#FFD700",  # gold
    "ENG": "#003478",  # navy
    "IND": "#FF9933",  # saffron
    "PAK": "#01411C",  # dark green
    "WI": "#7B0041",   # maroon
    "NZL": "#000000",  # black
    "SL": "#0000FF",   # blue
    "RSA": "#007749",  # green
}

COUNTRY_NAMES = {
    "AUS": "Australia", "ENG": "England", "IND": "India", "PAK": "Pakistan",
    "WI": "West Indies", "NZL": "New Zealand", "SL": "Sri Lanka", "RSA": "South Africa",
}


def fig9_country_bat_vs_population(df: pd.DataFrame):
    """Per-country BAT heights vs population baseline (2x4 grid)."""
    bat = df[df["category"] == "BAT"].dropna(
        subset=["height_cm", "tournament_year", "pop_height_birth_cohort"]
    )
    if len(bat) == 0:
        print("  Skipping fig9: no BAT population-matched data.")
        return

    fig, axes = plt.subplots(2, 4, figsize=(20, 10), sharey=True)
    axes = axes.flatten()

    for idx, country in enumerate(NATION_ORDER):
        ax = axes[idx]
        sub = bat[bat["country"] == country]
        if len(sub) < 3:
            ax.text(0.5, 0.5, f"{COUNTRY_NAMES[country]}\nInsufficient data",
                    transform=ax.transAxes, ha="center", va="center", fontsize=11)
            ax.set_title(COUNTRY_NAMES[country], fontsize=11, fontweight="bold")
            continue

        # Group by tournament year
        yearly = sub.groupby("tournament_year").agg(
            cricket_mean=("height_cm", "mean"),
            cricket_sem=("height_cm", lambda x: x.std() / np.sqrt(len(x)) if len(x) > 1 else 0),
            pop_mean=("pop_height_birth_cohort", "mean"),
            n=("height_cm", "count"),
        ).reset_index()

        # Cricket heights with error bars
        ax.errorbar(
            yearly["tournament_year"], yearly["cricket_mean"],
            yerr=yearly["cricket_sem"] * 1.96,
            fmt="o-", color=COUNTRY_COLORS.get(country, "#0072B2"),
            linewidth=1.5, markersize=4, capsize=2, label="BAT mean", zorder=3,
        )

        # Population baseline
        ax.plot(
            yearly["tournament_year"], yearly["pop_mean"],
            "s--", color="#D55E00", linewidth=1.5, markersize=3,
            label="Population", zorder=3,
        )

        # Fill between
        ax.fill_between(
            yearly["tournament_year"],
            yearly["pop_mean"],
            yearly["cricket_mean"],
            alpha=0.15, color=COUNTRY_COLORS.get(country, "#0072B2"),
        )

        # Regression lines
        if HAS_STATSMODELS and len(sub) >= 10:
            try:
                model_unadj = smf.ols("height_cm ~ tournament_year", data=sub).fit()
                x_range = np.linspace(sub["tournament_year"].min(), sub["tournament_year"].max(), 50)
                y_unadj = model_unadj.predict(pd.DataFrame({"tournament_year": x_range}))
                slope_u = model_unadj.params["tournament_year"]
                p_u = model_unadj.pvalues["tournament_year"]
                sig_u = "*" if p_u < 0.05 else ""

                model_adj = smf.ols(
                    "height_cm ~ tournament_year + pop_height_birth_cohort", data=sub
                ).fit()
                slope_a = model_adj.params["tournament_year"]
                p_a = model_adj.pvalues["tournament_year"]
                sig_a = "*" if p_a < 0.05 else ""

                ax.plot(x_range, y_unadj, "--", color=COUNTRY_COLORS.get(country, "#0072B2"),
                        linewidth=1, alpha=0.5)

                # Annotation box
                ax.text(
                    0.05, 0.95,
                    f"\u03B2={slope_u:+.3f}{sig_u}\n\u03B2_adj={slope_a:+.3f}{sig_a}\nn={len(sub)}",
                    transform=ax.transAxes, fontsize=8, va="top",
                    bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.8, ec="gray"),
                )
            except Exception:
                ax.text(0.05, 0.95, f"n={len(sub)}", transform=ax.transAxes, fontsize=8, va="top",
                        bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.8, ec="gray"))
        else:
            ax.text(0.05, 0.95, f"n={len(sub)}", transform=ax.transAxes, fontsize=8, va="top",
                    bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.8, ec="gray"))

        ax.set_title(COUNTRY_NAMES[country], fontsize=11, fontweight="bold")
        ax.xaxis.set_major_locator(MaxNLocator(integer=True, nbins=5))

        if idx % 4 == 0:
            ax.set_ylabel("Height (cm)")
        if idx >= 4:
            ax.set_xlabel("Tournament Year")

    # Common legend
    handles, labels = axes[0].get_legend_handles_labels()
    if handles:
        fig.legend(handles, labels, loc="lower center", ncol=3, fontsize=10,
                   bbox_to_anchor=(0.5, -0.02), frameon=True)

    fig.suptitle("Top-Order Batsman Heights vs Population Baseline by Country",
                 fontsize=14, fontweight="bold", y=1.02)
    plt.tight_layout()
    path = FIGURES_DIR / "fig9_country_bat_vs_population.png"
    fig.savefig(path, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {path}")


def _country_segmented_regression(df: pd.DataFrame, category: str, cat_label: str, fig_name: str):
    """Per-country segmented regression for a given category (2x4 grid)."""
    cat_data = df[df["category"] == category].dropna(subset=["height_cm", "tournament_year"])
    if len(cat_data) == 0:
        print(f"  Skipping {fig_name}: no {category} data.")
        return

    fig, axes = plt.subplots(2, 4, figsize=(20, 10), sharey=True)
    axes = axes.flatten()

    candidate_years = [1996, 1999, 2003, 2007, 2010, 2012]

    for idx, country in enumerate(NATION_ORDER):
        ax = axes[idx]
        sub = cat_data[cat_data["country"] == country]
        color = COUNTRY_COLORS.get(country, "#0072B2")

        if len(sub) < 10:
            ax.text(0.5, 0.5, f"{COUNTRY_NAMES[country]}\nInsufficient data\n(n={len(sub)})",
                    transform=ax.transAxes, ha="center", va="center", fontsize=11)
            ax.set_title(COUNTRY_NAMES[country], fontsize=11, fontweight="bold")
            continue

        # Scatter
        ax.scatter(
            sub["tournament_year"], sub["height_cm"],
            c=color, alpha=0.35, s=20, edgecolors="none",
        )

        # Find best breakpoint via Chow test
        best_bp = None
        best_f = -1
        best_p = 1.0

        if HAS_STATSMODELS:
            for bp in candidate_years:
                pre = sub[sub["tournament_year"] <= bp]
                post = sub[sub["tournament_year"] > bp]
                if len(pre) < 5 or len(post) < 5:
                    continue
                try:
                    model_full = smf.ols("height_cm ~ tournament_year", data=sub).fit()
                    model_pre = smf.ols("height_cm ~ tournament_year", data=pre).fit()
                    model_post = smf.ols("height_cm ~ tournament_year", data=post).fit()
                    rss_full = model_full.ssr
                    rss_rest = model_pre.ssr + model_post.ssr
                    k = 2
                    n = len(sub)
                    f_stat = ((rss_full - rss_rest) / k) / (rss_rest / (n - 2 * k))
                    if f_stat > best_f:
                        best_f = f_stat
                        best_bp = bp
                        from scipy.stats import f as f_dist
                        best_p = 1 - f_dist.cdf(f_stat, k, n - 2 * k)
                except Exception:
                    continue

        if best_bp is None:
            # No valid breakpoint found; draw single regression
            z = np.polyfit(sub["tournament_year"], sub["height_cm"], 1)
            p_line = np.poly1d(z)
            x_range = np.linspace(sub["tournament_year"].min(), sub["tournament_year"].max(), 50)
            ax.plot(x_range, p_line(x_range), color=color, linewidth=2)
            ax.text(
                0.05, 0.95,
                f"\u03B2={z[0]:+.3f}\nn={len(sub)}\nNo valid BP",
                transform=ax.transAxes, fontsize=8, va="top",
                bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.8, ec="gray"),
            )
        else:
            # Segmented regression
            pre = sub[sub["tournament_year"] <= best_bp]
            post = sub[sub["tournament_year"] > best_bp]

            for seg, seg_label in [(pre, "Pre"), (post, "Post")]:
                if len(seg) < 3:
                    continue
                z = np.polyfit(seg["tournament_year"], seg["height_cm"], 1)
                p_line = np.poly1d(z)
                x_range = np.linspace(seg["tournament_year"].min(), seg["tournament_year"].max(), 50)
                ax.plot(x_range, p_line(x_range), color=color, linewidth=2.5)

                # Annotate slope on the line
                mid_x = seg["tournament_year"].median()
                mid_y = p_line(mid_x)
                offset_y = 3 if seg_label == "Pre" else -4
                ax.annotate(
                    f"\u03B2={z[0]:+.3f}", xy=(mid_x, mid_y),
                    xytext=(0, offset_y), textcoords="offset points",
                    fontsize=8, fontweight="bold", color=color,
                    ha="center", va="bottom" if offset_y > 0 else "top",
                    bbox=dict(boxstyle="round,pad=0.2", fc="white", alpha=0.8, ec="none"),
                )

            # Breakpoint vertical line
            ax.axvline(x=best_bp, color="gray", linestyle="--", linewidth=1, alpha=0.7)

            # Breakpoint info box
            sig_str = f"p={best_p:.3f}" if best_p >= 0.001 else "p<.001"
            bp_sig = "*" if best_p < 0.05 else ""
            ax.text(
                0.05, 0.95,
                f"BP={best_bp}{bp_sig}\nF={best_f:.1f}, {sig_str}\nn={len(sub)}",
                transform=ax.transAxes, fontsize=8, va="top",
                bbox=dict(boxstyle="round,pad=0.3", fc="lightyellow", alpha=0.9, ec="gray"),
            )

        ax.set_title(COUNTRY_NAMES[country], fontsize=11, fontweight="bold")
        ax.xaxis.set_major_locator(MaxNLocator(integer=True, nbins=5))

        if idx % 4 == 0:
            ax.set_ylabel("Height (cm)")
        if idx >= 4:
            ax.set_xlabel("Tournament Year")

    fig.suptitle(f"{cat_label} — Segmented Regression by Country",
                 fontsize=14, fontweight="bold", y=1.02)
    plt.tight_layout()
    path = FIGURES_DIR / fig_name
    fig.savefig(path, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {path}")


def fig10_country_bat_segmented(df: pd.DataFrame):
    """Per-country segmented regression for top-order batsmen."""
    _country_segmented_regression(df, "BAT", "Top-Order Batsmen", "fig10_country_bat_segmented.png")


def fig11_country_fast_segmented(df: pd.DataFrame):
    """Per-country segmented regression for fast bowlers."""
    _country_segmented_regression(df, "FAST", "Fast Bowlers", "fig11_country_fast_segmented.png")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    if not MERGED_CSV.exists():
        print(f"ERROR: Merged CSV not found: {MERGED_CSV}")
        print("       Run merge_all_tournaments.py first.")
        sys.exit(1)

    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(MERGED_CSV)
    print(f"Loaded {len(df)} player-tournament records from {MERGED_CSV}")

    # Ensure numeric types
    for col in ["height_cm", "tournament_year", "pop_height_birth_cohort",
                 "height_excess", "era", "birth_year", "age_at_tournament"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df_valid = df[df["height_cm"].notna()].copy()
    print(f"Records with valid height: {len(df_valid)}")

    if len(df_valid) == 0:
        print("ERROR: No records with valid height data.")
        sys.exit(1)

    setup_style()

    print("\nGenerating figures...")
    fig1_category_distributions(df_valid)
    fig2_temporal_trends(df_valid)
    fig3_country_comparison(df_valid)
    fig4_era_boxplot(df_valid)
    fig5_population_adjusted(df_valid)
    fig6_breakpoint(df_valid)
    fig7_format_comparison(df_valid)
    fig8_main_figure(df_valid)
    fig9_country_bat_vs_population(df_valid)
    fig10_country_bat_segmented(df_valid)
    fig11_country_fast_segmented(df_valid)

    print(f"\nAll figures saved to: {FIGURES_DIR}")
    print("Done.")


if __name__ == "__main__":
    main()
