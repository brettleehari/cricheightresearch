#!/usr/bin/env python3
"""
generate_new_figures.py - Additional cross-sectional visualizations for the
cricket anthropometric research project.

Creates ~15 unique figures slicing the dataset in novel ways that would
fascinate the cricketing community.

Usage:
    python scripts/generate_new_figures.py
"""

import sys
import warnings
from pathlib import Path
from itertools import combinations

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.ticker import MaxNLocator
from matplotlib.patches import Patch, FancyBboxPatch
from matplotlib.lines import Line2D
import matplotlib.patheffects as pe

try:
    import seaborn as sns
    HAS_SEABORN = True
except ImportError:
    HAS_SEABORN = False

try:
    import statsmodels.formula.api as smf
    HAS_STATSMODELS = True
except ImportError:
    HAS_STATSMODELS = False

from scipy import stats as sp_stats
from scipy.cluster.hierarchy import dendrogram, linkage

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
MERGED_CSV = BASE_DIR / "data" / "processed" / "all_players.csv"
FIGURES_DIR = BASE_DIR / "figures"
DPI = 300

CATEGORY_COLORS = {
    "WK": "#E69F00",
    "BAT": "#0072B2",
    "FAST": "#D55E00",
    "SPIN": "#009E73",
}
CATEGORY_ORDER = ["WK", "BAT", "FAST", "SPIN"]

COUNTRY_COLORS = {
    "AUS": "#FFD700",
    "ENG": "#003478",
    "IND": "#FF9933",
    "PAK": "#01411C",
    "WI": "#7B0041",
    "NZL": "#000000",
    "SL": "#0000FF",
    "RSA": "#007749",
}

COUNTRY_NAMES = {
    "AUS": "Australia", "ENG": "England", "IND": "India", "PAK": "Pakistan",
    "WI": "West Indies", "NZL": "New Zealand", "SL": "Sri Lanka", "RSA": "South Africa",
}

NATION_ORDER = ["AUS", "ENG", "NZL", "RSA", "WI", "IND", "PAK", "SL"]

REGION_COLORS = {
    "South Asian": "#E69F00",
    "Oceanian": "#0072B2",
    "Caribbean": "#D55E00",
    "European": "#009E73",
    "African": "#CC79A7",
}

ERA_LABELS = {
    1: "1975-87", 2: "1992-99", 3: "2003-12", 4: "2014-26"
}

FORMAT_COLORS = {"ODI": "#0072B2", "T20": "#D55E00"}


def setup_style():
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


# ===================================================================
# FIGURE 12: "The Height Arms Race" - Heatmap of mean height by
# country x decade showing how each nation's selection has evolved
# ===================================================================
def fig12_height_arms_race(df):
    """Heatmap: mean height by country x era — the 'arms race' of selection."""
    fig, axes = plt.subplots(1, 2, figsize=(16, 7), gridspec_kw={"width_ratios": [1, 1]})

    for ax, metric, title, cmap, fmt in [
        (axes[0], "height_cm", "Raw Height (cm)", "YlOrRd", ".1f"),
        (axes[1], "height_excess", "Height Excess Over Population (cm)", "RdYlGn", ".1f"),
    ]:
        pivot = df.pivot_table(
            values=metric, index="country", columns="era", aggfunc="mean"
        ).reindex(NATION_ORDER)
        pivot.columns = [ERA_LABELS.get(int(c), str(c)) for c in pivot.columns]

        if HAS_SEABORN:
            sns.heatmap(
                pivot, annot=True, fmt=fmt, cmap=cmap, ax=ax,
                linewidths=1, linecolor="white",
                yticklabels=[COUNTRY_NAMES.get(c, c) for c in pivot.index],
                cbar_kws={"shrink": 0.8},
            )
        else:
            im = ax.imshow(pivot.values, aspect="auto", cmap=cmap)
            ax.set_xticks(range(len(pivot.columns)))
            ax.set_xticklabels(pivot.columns)
            ax.set_yticks(range(len(pivot.index)))
            ax.set_yticklabels([COUNTRY_NAMES.get(c, c) for c in pivot.index])
            for i in range(len(pivot.index)):
                for j in range(len(pivot.columns)):
                    val = pivot.values[i, j]
                    if not np.isnan(val):
                        ax.text(j, i, f"{val:{fmt}}", ha="center", va="center", fontsize=9)
            fig.colorbar(im, ax=ax, shrink=0.8)

        ax.set_title(title, fontweight="bold")
        ax.set_xlabel("Era")

    fig.suptitle("The Height Arms Race: How Each Nation's Selection Has Evolved",
                 fontsize=15, fontweight="bold", y=1.02)
    plt.tight_layout()
    path = FIGURES_DIR / "fig12_height_arms_race.png"
    fig.savefig(path, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {path}")


# ===================================================================
# FIGURE 13: "The Tallest XIs" - Each nation's tallest-ever Playing XI
# vs shortest-ever Playing XI (stacked horizontal bars)
# ===================================================================
def fig13_tallest_vs_shortest_xi(df):
    """Compare each nation's tallest vs shortest Playing XI ever fielded."""
    fig, axes = plt.subplots(4, 2, figsize=(16, 20))
    axes = axes.flatten()

    for idx, country in enumerate(NATION_ORDER):
        ax = axes[idx]
        sub = df[df["country"] == country]

        # Get mean team height per tournament
        team_means = sub.groupby("tournament_id").agg(
            mean_height=("height_cm", "mean"),
            tournament_year=("tournament_year", "first"),
            fmt=("format", "first"),
        ).sort_values("mean_height")

        if len(team_means) < 2:
            ax.text(0.5, 0.5, "Insufficient data", transform=ax.transAxes, ha="center")
            ax.set_title(COUNTRY_NAMES[country])
            continue

        shortest = team_means.iloc[0]
        tallest = team_means.iloc[-1]

        # Get the actual XI for each
        shortest_xi = sub[sub["tournament_id"] == team_means.index[0]].sort_values("batting_position")
        tallest_xi = sub[sub["tournament_id"] == team_means.index[-1]].sort_values("batting_position")

        # Plot all tournament means as a bar chart
        colors = []
        for tid in team_means.index:
            if tid == team_means.index[0]:
                colors.append("#3498db")  # blue for shortest
            elif tid == team_means.index[-1]:
                colors.append("#e74c3c")  # red for tallest
            else:
                colors.append("#bdc3c7")  # gray for others

        bars = ax.barh(
            range(len(team_means)),
            team_means["mean_height"],
            color=colors, edgecolor="white", height=0.7,
        )

        labels = []
        for tid, row in team_means.iterrows():
            yr = int(row["tournament_year"])
            fmt = row["fmt"]
            labels.append(f"{fmt} {yr}")

        ax.set_yticks(range(len(team_means)))
        ax.set_yticklabels(labels, fontsize=8)

        # Annotate shortest and tallest
        ax.text(
            shortest["mean_height"] + 0.3, 0,
            f'{shortest["mean_height"]:.1f} cm',
            va="center", fontsize=8, fontweight="bold", color="#3498db",
        )
        ax.text(
            tallest["mean_height"] + 0.3, len(team_means) - 1,
            f'{tallest["mean_height"]:.1f} cm',
            va="center", fontsize=8, fontweight="bold", color="#e74c3c",
        )

        # Zoom x-axis
        min_val = team_means["mean_height"].min() - 3
        max_val = team_means["mean_height"].max() + 5
        ax.set_xlim(min_val, max_val)
        ax.set_xlabel("Mean Team Height (cm)")
        ax.set_title(f"{COUNTRY_NAMES[country]}", fontsize=12, fontweight="bold")

    fig.suptitle("Tournament Team Heights: Every Playing XI Ranked\n"
                 "(Blue = shortest XI ever, Red = tallest XI ever)",
                 fontsize=15, fontweight="bold", y=1.02)
    plt.tight_layout()
    path = FIGURES_DIR / "fig13_tallest_vs_shortest_xi.png"
    fig.savefig(path, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {path}")


# ===================================================================
# FIGURE 14: "The Giant Killers" - Scatter of team mean height vs
# tournament performance (did they win/lose?)
# ===================================================================
def fig14_batting_position_height_profile(df):
    """Height profile by batting position — how the batting order is 'shaped'."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))

    # Panel A: Mean height by batting position (all eras pooled)
    ax = axes[0, 0]
    bp_stats = df.groupby("batting_position")["height_cm"].agg(["mean", "std", "count"]).reset_index()
    bp_stats["sem"] = bp_stats["std"] / np.sqrt(bp_stats["count"])

    colors_bp = []
    for bp in bp_stats["batting_position"]:
        if bp <= 6:
            colors_bp.append(CATEGORY_COLORS["BAT"])
        else:
            colors_bp.append("#999999")

    ax.bar(bp_stats["batting_position"], bp_stats["mean"],
           yerr=bp_stats["sem"] * 1.96, capsize=3,
           color=colors_bp, edgecolor="white", width=0.7)
    for _, row in bp_stats.iterrows():
        ax.text(row["batting_position"], row["mean"] + row["sem"] * 1.96 + 0.3,
                f'{row["mean"]:.1f}', ha="center", fontsize=8, fontweight="bold")
    ax.set_xlabel("Batting Position")
    ax.set_ylabel("Mean Height (cm)")
    ax.set_title("A. Mean Height by Batting Position (All Eras)")
    ax.set_xticks(range(1, 12))

    # Panel B: Height by batting position, split by era
    ax = axes[0, 1]
    era_colors = {1: "#fee08b", 2: "#fdae61", 3: "#f46d43", 4: "#d73027"}
    for era in sorted(df["era"].dropna().unique()):
        era_int = int(era)
        sub = df[df["era"] == era]
        bp_means = sub.groupby("batting_position")["height_cm"].mean()
        ax.plot(bp_means.index, bp_means.values, "o-",
                color=era_colors.get(era_int, "#999"),
                label=ERA_LABELS.get(era_int, str(era_int)),
                markersize=5, linewidth=1.5)
    ax.set_xlabel("Batting Position")
    ax.set_ylabel("Mean Height (cm)")
    ax.set_title("B. Batting Position Profile by Era")
    ax.legend(title="Era", fontsize=9)
    ax.set_xticks(range(1, 12))

    # Panel C: Height by batting position, split by region
    ax = axes[1, 0]
    for region, color in REGION_COLORS.items():
        sub = df[df["region"] == region]
        bp_means = sub.groupby("batting_position")["height_cm"].mean()
        if len(bp_means) >= 3:
            ax.plot(bp_means.index, bp_means.values, "o-",
                    color=color, label=region, markersize=5, linewidth=1.5)
    ax.set_xlabel("Batting Position")
    ax.set_ylabel("Mean Height (cm)")
    ax.set_title("C. Batting Position Profile by Region")
    ax.legend(title="Region", fontsize=9)
    ax.set_xticks(range(1, 12))

    # Panel D: Opener (pos 1-2) vs middle order (pos 3-6) height evolution
    ax = axes[1, 1]
    df_bat = df[df["category"] == "BAT"]
    df_bat = df_bat.copy()
    df_bat["batting_role"] = df_bat["batting_position"].apply(
        lambda x: "Opener (1-2)" if x <= 2 else "Middle Order (3-6)"
    )
    for role, color, marker in [("Opener (1-2)", "#2980b9", "o"),
                                  ("Middle Order (3-6)", "#c0392b", "s")]:
        sub = df_bat[df_bat["batting_role"] == role]
        yearly = sub.groupby("tournament_year")["height_cm"].mean()
        ax.plot(yearly.index, yearly.values, f"{marker}-",
                color=color, label=role, markersize=5, linewidth=1.5)
    ax.set_xlabel("Tournament Year")
    ax.set_ylabel("Mean Height (cm)")
    ax.set_title("D. Opener vs Middle-Order Height Over Time")
    ax.legend(fontsize=9)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    fig.suptitle("The Shape of a Cricket Team: Height by Batting Position",
                 fontsize=15, fontweight="bold", y=1.02)
    plt.tight_layout()
    path = FIGURES_DIR / "fig14_batting_position_profile.png"
    fig.savefig(path, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {path}")


# ===================================================================
# FIGURE 15: "The FAST Bowler Premium" — how much taller are fast
# bowlers than batsmen in the SAME team, by country and era
# ===================================================================
def fig15_fast_bat_gap(df):
    """The FAST-BAT height gap within teams over time."""
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))

    # Calculate per-team FAST mean - BAT mean
    team_gaps = []
    for (tid, country), grp in df.groupby(["tournament_id", "country"]):
        bat_mean = grp[grp["category"] == "BAT"]["height_cm"].mean()
        fast_mean = grp[grp["category"] == "FAST"]["height_cm"].mean()
        if pd.notna(bat_mean) and pd.notna(fast_mean):
            team_gaps.append({
                "tournament_id": tid,
                "country": country,
                "tournament_year": grp["tournament_year"].iloc[0],
                "era": grp["era"].iloc[0],
                "gap": fast_mean - bat_mean,
                "region": grp["region"].iloc[0],
            })
    gaps = pd.DataFrame(team_gaps)

    if len(gaps) == 0:
        plt.close(fig)
        print("  Skipping fig15: insufficient data.")
        return

    # Panel A: Gap over time by country
    ax = axes[0]
    for country in NATION_ORDER:
        sub = gaps[gaps["country"] == country]
        yearly = sub.groupby("tournament_year")["gap"].mean()
        if len(yearly) >= 3:
            ax.plot(yearly.index, yearly.values, "o-",
                    color=COUNTRY_COLORS[country], label=COUNTRY_NAMES[country],
                    markersize=4, linewidth=1.5, alpha=0.8)
    ax.axhline(y=0, color="gray", linestyle="--", linewidth=0.8, alpha=0.5)
    ax.set_xlabel("Tournament Year")
    ax.set_ylabel("FAST - BAT Height Gap (cm)")
    ax.set_title("A. Fast Bowler Height Premium Over Batsmen\n(Per-Team Gap Over Time)")
    ax.legend(fontsize=8, ncol=2)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    # Panel B: Gap by country (box plot)
    ax = axes[1]
    gap_data = [gaps[gaps["country"] == c]["gap"].dropna().values for c in NATION_ORDER]
    box_colors = [COUNTRY_COLORS[c] for c in NATION_ORDER]

    bp = ax.boxplot(
        gap_data, labels=[COUNTRY_NAMES[c] for c in NATION_ORDER],
        patch_artist=True, widths=0.6, flierprops=dict(markersize=3),
    )
    for patch, color in zip(bp["boxes"], box_colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    for median in bp["medians"]:
        median.set_color("black")
        median.set_linewidth(2)

    ax.axhline(y=0, color="gray", linestyle="--", linewidth=0.8, alpha=0.5)
    ax.set_ylabel("FAST - BAT Height Gap (cm)")
    ax.set_title("B. Distribution of FAST-BAT Gap by Country")
    ax.tick_params(axis="x", rotation=45)

    # Annotate medians
    for i, c in enumerate(NATION_ORDER):
        sub = gaps[gaps["country"] == c]["gap"]
        if len(sub) > 0:
            med = sub.median()
            ax.text(i + 1, med + 0.5, f"{med:.1f}", ha="center", fontsize=8, fontweight="bold")

    fig.suptitle("The Fast Bowler Premium: Height Gap Over Batsmen Within Teams",
                 fontsize=15, fontweight="bold", y=1.02)
    plt.tight_layout()
    path = FIGURES_DIR / "fig15_fast_bat_gap.png"
    fig.savefig(path, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {path}")


# ===================================================================
# FIGURE 16: "Age vs Height" — Do teams pick younger/taller or
# older/shorter players over time?
# ===================================================================
def fig16_age_height_relationship(df):
    """Scatter of age vs height colored by era, with team composition insight."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))

    era_colors = {1: "#fee08b", 2: "#fdae61", 3: "#f46d43", 4: "#d73027"}

    # Panel A: Age vs height scatter (all data)
    ax = axes[0, 0]
    for era in sorted(df["era"].dropna().unique()):
        era_int = int(era)
        sub = df[df["era"] == era].dropna(subset=["age_at_tournament", "height_cm"])
        ax.scatter(sub["age_at_tournament"], sub["height_cm"],
                   c=era_colors.get(era_int, "#999"), alpha=0.3, s=15,
                   label=ERA_LABELS.get(era_int, str(era_int)), edgecolors="none")
    ax.set_xlabel("Age at Tournament")
    ax.set_ylabel("Height (cm)")
    ax.set_title("A. Age vs Height (All Players)")
    ax.legend(title="Era", fontsize=9)

    # Panel B: Mean age over time by category
    ax = axes[0, 1]
    for cat in CATEGORY_ORDER:
        sub = df[df["category"] == cat]
        yearly = sub.groupby("tournament_year")["age_at_tournament"].mean()
        ax.plot(yearly.index, yearly.values, "o-",
                color=CATEGORY_COLORS[cat], label=cat, markersize=4, linewidth=1.5)
    ax.set_xlabel("Tournament Year")
    ax.set_ylabel("Mean Age at Tournament")
    ax.set_title("B. Mean Player Age Over Time by Category")
    ax.legend(fontsize=9)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    # Panel C: Birth year distribution by era (are they picking from taller generations?)
    ax = axes[1, 0]
    for era in sorted(df["era"].dropna().unique()):
        era_int = int(era)
        sub = df[df["era"] == era]["birth_year"].dropna()
        if len(sub) > 5:
            ax.hist(sub, bins=20, alpha=0.5,
                    color=era_colors.get(era_int, "#999"),
                    label=ERA_LABELS.get(era_int, str(era_int)),
                    density=True, edgecolor="white")
    ax.set_xlabel("Birth Year")
    ax.set_ylabel("Density")
    ax.set_title("C. Birth Year Distribution by Era")
    ax.legend(title="Era", fontsize=9)

    # Panel D: Mean height of DEBUTANTS (first tournament appearance)
    ax = axes[1, 1]
    # Find first tournament for each player
    first_appearances = df.sort_values("tournament_year").drop_duplicates(
        subset="player_id", keep="first"
    )
    for cat in ["BAT", "FAST"]:
        sub = first_appearances[first_appearances["category"] == cat]
        yearly = sub.groupby("tournament_year")["height_cm"].mean()
        ax.plot(yearly.index, yearly.values, "o-",
                color=CATEGORY_COLORS[cat], label=f"{cat} debutants",
                markersize=5, linewidth=1.5)

    # Also plot population baseline
    pop_yearly = first_appearances.groupby("tournament_year")["pop_height_birth_cohort"].mean()
    ax.plot(pop_yearly.index, pop_yearly.values, "s--", color="#999",
            label="Population baseline", markersize=4, linewidth=1.5)

    ax.set_xlabel("Tournament Year")
    ax.set_ylabel("Mean Height (cm)")
    ax.set_title("D. Height of World Cup Debutants Over Time")
    ax.legend(fontsize=9)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    fig.suptitle("Age, Generations, and Selection: The Demographic Engine",
                 fontsize=15, fontweight="bold", y=1.02)
    plt.tight_layout()
    path = FIGURES_DIR / "fig16_age_height_demographics.png"
    fig.savefig(path, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {path}")


# ===================================================================
# FIGURE 17: "The Wicketkeeper Paradox" — WK are the shortest but
# how does their height compare to population? Are they STILL selected
# for height?
# ===================================================================
def fig17_wicketkeeper_paradox(df):
    """The wicketkeeper height paradox — shortest category but still taller than population."""
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    # Panel A: WK height excess over population vs other categories
    ax = axes[0]
    excess_means = []
    for cat in CATEGORY_ORDER:
        sub = df[df["category"] == cat]["height_excess"].dropna()
        excess_means.append({
            "category": cat,
            "mean_excess": sub.mean(),
            "sem": sub.std() / np.sqrt(len(sub)) if len(sub) > 1 else 0,
            "n": len(sub),
        })
    edf = pd.DataFrame(excess_means)
    bars = ax.bar(edf["category"], edf["mean_excess"],
                  yerr=edf["sem"] * 1.96, capsize=4,
                  color=[CATEGORY_COLORS[c] for c in edf["category"]],
                  edgecolor="white", width=0.6)
    for i, row in edf.iterrows():
        ax.text(i, row["mean_excess"] + row["sem"] * 1.96 + 0.3,
                f'+{row["mean_excess"]:.1f} cm\n(n={row["n"]})',
                ha="center", fontsize=9, fontweight="bold")
    ax.axhline(y=0, color="gray", linestyle="--", linewidth=0.8)
    ax.set_ylabel("Height Excess Over Population (cm)")
    ax.set_title("A. Even Keepers Are Taller\nThan Their Population")

    # Panel B: WK height range comparison (smallest range?)
    ax = axes[1]
    for cat in CATEGORY_ORDER:
        sub = df[df["category"] == cat]["height_cm"].dropna()
        ax.violinplot(
            [sub.values], positions=[CATEGORY_ORDER.index(cat)],
            showmeans=True, showmedians=True,
        )
    ax.set_xticks(range(len(CATEGORY_ORDER)))
    ax.set_xticklabels(CATEGORY_ORDER)

    # Annotate range
    for i, cat in enumerate(CATEGORY_ORDER):
        sub = df[df["category"] == cat]["height_cm"].dropna()
        rng = sub.max() - sub.min()
        sd = sub.std()
        ax.text(i, sub.min() - 2, f"Range: {rng:.0f}\nSD: {sd:.1f}",
                ha="center", fontsize=8, color=CATEGORY_COLORS[cat])

    ax.set_ylabel("Height (cm)")
    ax.set_title("B. Height Variability by Category\n(WK = most compact range)")

    # Panel C: WK height over time vs population
    ax = axes[2]
    wk = df[df["category"] == "WK"].dropna(subset=["height_cm", "tournament_year", "pop_height_birth_cohort"])
    if len(wk) > 5:
        yearly = wk.groupby("tournament_year").agg(
            wk_mean=("height_cm", "mean"),
            pop_mean=("pop_height_birth_cohort", "mean"),
        ).reset_index()
        ax.plot(yearly["tournament_year"], yearly["wk_mean"], "o-",
                color=CATEGORY_COLORS["WK"], label="WK mean", markersize=5, linewidth=2)
        ax.plot(yearly["tournament_year"], yearly["pop_mean"], "s--",
                color="#D55E00", label="Population baseline", markersize=4, linewidth=1.5)
        ax.fill_between(yearly["tournament_year"], yearly["pop_mean"], yearly["wk_mean"],
                        alpha=0.15, color=CATEGORY_COLORS["WK"])
        ax.legend(fontsize=9)
    ax.set_xlabel("Tournament Year")
    ax.set_ylabel("Height (cm)")
    ax.set_title("C. Wicketkeeper Heights Over Time\nvs Population Baseline")
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    fig.suptitle("The Wicketkeeper Paradox: Shortest Category, Still Selected for Height",
                 fontsize=15, fontweight="bold", y=1.02)
    plt.tight_layout()
    path = FIGURES_DIR / "fig17_wicketkeeper_paradox.png"
    fig.savefig(path, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {path}")


# ===================================================================
# FIGURE 18: "Team Height Diversity" — Within-team height variance
# (homogeneous vs diverse teams)
# ===================================================================
def fig18_team_height_diversity(df):
    """Within-team height standard deviation over time by country."""
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))

    # Calculate per-team SD
    team_stats = df.groupby(["tournament_id", "country"]).agg(
        mean_height=("height_cm", "mean"),
        sd_height=("height_cm", "std"),
        range_height=("height_cm", lambda x: x.max() - x.min()),
        tournament_year=("tournament_year", "first"),
        region=("region", "first"),
    ).reset_index()

    # Panel A: Team SD over time
    ax = axes[0]
    overall_sd = team_stats.groupby("tournament_year")["sd_height"].mean()
    ax.plot(overall_sd.index, overall_sd.values, "ko-", linewidth=2, markersize=6,
            label="All nations", zorder=5)

    for country in NATION_ORDER:
        sub = team_stats[team_stats["country"] == country]
        yearly = sub.groupby("tournament_year")["sd_height"].mean()
        if len(yearly) >= 3:
            ax.plot(yearly.index, yearly.values, "--",
                    color=COUNTRY_COLORS[country], alpha=0.5, linewidth=1)

    ax.set_xlabel("Tournament Year")
    ax.set_ylabel("Within-Team Height SD (cm)")
    ax.set_title("A. Team Height Diversity Over Time\n(Higher = more diverse heights)")
    ax.legend(fontsize=9)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    # Panel B: Team height range by country
    ax = axes[1]
    range_data = [team_stats[team_stats["country"] == c]["range_height"].dropna().values
                  for c in NATION_ORDER]
    box_colors = [COUNTRY_COLORS[c] for c in NATION_ORDER]

    bp = ax.boxplot(
        range_data, labels=[COUNTRY_NAMES.get(c, c) for c in NATION_ORDER],
        patch_artist=True, widths=0.6, flierprops=dict(markersize=3),
    )
    for patch, color in zip(bp["boxes"], box_colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    for median in bp["medians"]:
        median.set_color("black")
        median.set_linewidth(2)

    # Annotate medians
    for i, c in enumerate(NATION_ORDER):
        sub = team_stats[team_stats["country"] == c]["range_height"]
        if len(sub) > 0:
            med = sub.median()
            ax.text(i + 1, med + 1, f"{med:.0f}", ha="center", fontsize=8, fontweight="bold")

    ax.set_ylabel("Within-Team Height Range (cm)")
    ax.set_title("B. Team Height Range (Max - Min) by Country")
    ax.tick_params(axis="x", rotation=45)

    fig.suptitle("Team Height Diversity: Are Teams Becoming More or Less Uniform?",
                 fontsize=15, fontweight="bold", y=1.02)
    plt.tight_layout()
    path = FIGURES_DIR / "fig18_team_height_diversity.png"
    fig.savefig(path, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {path}")


# ===================================================================
# FIGURE 19: "The Spin Bowler Story" — Spin vs Fast height gap by
# country (subcontinent vs pace nations)
# ===================================================================
def fig19_spin_vs_fast_by_country(df):
    """SPIN vs FAST bowler heights by country — subcontinent vs pace nations."""
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))

    bowlers = df[df["category"].isin(["FAST", "SPIN"])].copy()

    # Panel A: Side-by-side violin for FAST vs SPIN by country
    ax = axes[0]
    country_fast_means = []
    country_spin_means = []
    for i, country in enumerate(NATION_ORDER):
        fast_sub = bowlers[(bowlers["country"] == country) & (bowlers["category"] == "FAST")]["height_cm"]
        spin_sub = bowlers[(bowlers["country"] == country) & (bowlers["category"] == "SPIN")]["height_cm"]
        if len(fast_sub) > 2:
            ax.scatter(np.full(len(fast_sub), i - 0.15), fast_sub,
                       c=CATEGORY_COLORS["FAST"], alpha=0.3, s=10, edgecolors="none")
            country_fast_means.append(fast_sub.mean())
        else:
            country_fast_means.append(np.nan)
        if len(spin_sub) > 2:
            ax.scatter(np.full(len(spin_sub), i + 0.15), spin_sub,
                       c=CATEGORY_COLORS["SPIN"], alpha=0.3, s=10, edgecolors="none")
            country_spin_means.append(spin_sub.mean())
        else:
            country_spin_means.append(np.nan)

    # Plot means as connected markers
    x_pos = np.arange(len(NATION_ORDER))
    ax.scatter(x_pos - 0.15, country_fast_means, c=CATEGORY_COLORS["FAST"],
               s=80, marker="D", zorder=5, edgecolors="black", linewidth=0.5, label="FAST mean")
    ax.scatter(x_pos + 0.15, country_spin_means, c=CATEGORY_COLORS["SPIN"],
               s=80, marker="D", zorder=5, edgecolors="black", linewidth=0.5, label="SPIN mean")

    # Connect FAST-SPIN pairs with lines showing gap
    for i in range(len(NATION_ORDER)):
        if not np.isnan(country_fast_means[i]) and not np.isnan(country_spin_means[i]):
            ax.plot([i - 0.15, i + 0.15], [country_fast_means[i], country_spin_means[i]],
                    "k-", linewidth=1, alpha=0.5)
            gap = country_fast_means[i] - country_spin_means[i]
            mid_y = (country_fast_means[i] + country_spin_means[i]) / 2
            ax.text(i + 0.25, mid_y, f"{gap:+.1f}", fontsize=7, va="center", fontweight="bold")

    ax.set_xticks(range(len(NATION_ORDER)))
    ax.set_xticklabels([COUNTRY_NAMES[c] for c in NATION_ORDER], rotation=45, ha="right")
    ax.set_ylabel("Height (cm)")
    ax.set_title("A. FAST vs SPIN Heights by Country\n(Gap annotated)")
    ax.legend(fontsize=9)

    # Panel B: Proportion of SPIN bowlers over time by region
    ax = axes[1]
    lower_order = df[df["category"].isin(["FAST", "SPIN"])].copy()
    for region, color in REGION_COLORS.items():
        sub = lower_order[lower_order["region"] == region]
        yearly = sub.groupby("tournament_year")["category"].apply(
            lambda x: (x == "SPIN").sum() / len(x) * 100
        )
        if len(yearly) >= 3:
            ax.plot(yearly.index, yearly.values, "o-",
                    color=color, label=region, markersize=4, linewidth=1.5)

    ax.set_xlabel("Tournament Year")
    ax.set_ylabel("Spin Bowlers as % of All Bowlers")
    ax.set_title("B. Spin Bowling Reliance Over Time by Region")
    ax.legend(fontsize=9)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    fig.suptitle("The Spin vs Pace Height Story: Subcontinent vs Pace Nations",
                 fontsize=15, fontweight="bold", y=1.02)
    plt.tight_layout()
    path = FIGURES_DIR / "fig19_spin_vs_fast.png"
    fig.savefig(path, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {path}")


# ===================================================================
# FIGURE 20: "Career Span Giants" — Players appearing in most WCs
# and their heights (the longevity-height relationship)
# ===================================================================
def fig20_career_span_giants(df):
    """Players with most World Cup appearances — are tall players more durable?"""
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))

    # Count WC appearances per player
    player_wcs = df.groupby(["player_id", "full_name", "country", "category"]).agg(
        num_wcs=("tournament_id", "nunique"),
        height_cm=("height_cm", "first"),
        height_excess=("height_excess", "first"),
        first_year=("tournament_year", "min"),
        last_year=("tournament_year", "max"),
    ).reset_index()
    player_wcs["career_span"] = player_wcs["last_year"] - player_wcs["first_year"]

    # Panel A: Top 30 most-capped WC players
    ax = axes[0]
    top_players = player_wcs.nlargest(30, "num_wcs").sort_values("num_wcs")
    colors = [CATEGORY_COLORS.get(cat, "#999") for cat in top_players["category"]]

    bars = ax.barh(range(len(top_players)), top_players["height_cm"],
                   color=colors, edgecolor="white", height=0.7)

    labels = []
    for _, row in top_players.iterrows():
        name = row["full_name"]
        if len(name) > 18:
            name = name[:16] + ".."
        labels.append(f'{name} ({row["country"]}) [{int(row["num_wcs"])} WCs]')
    ax.set_yticks(range(len(top_players)))
    ax.set_yticklabels(labels, fontsize=7)
    ax.set_xlabel("Height (cm)")
    ax.set_title("A. Heights of Most World Cup-Capped Players")

    # Add mean line
    mean_h = top_players["height_cm"].mean()
    ax.axvline(x=mean_h, color="gray", linestyle="--", linewidth=1, alpha=0.7)
    ax.text(mean_h + 0.5, len(top_players) - 1, f"Mean: {mean_h:.1f}",
            fontsize=8, color="gray")

    # Legend
    legend_elements = [Patch(facecolor=CATEGORY_COLORS[c], label=c) for c in CATEGORY_ORDER]
    ax.legend(handles=legend_elements, fontsize=8, loc="lower right")

    # Panel B: Career span vs height scatter
    ax = axes[1]
    multi_wc = player_wcs[player_wcs["num_wcs"] >= 2]
    for cat in CATEGORY_ORDER:
        sub = multi_wc[multi_wc["category"] == cat]
        ax.scatter(sub["height_cm"], sub["career_span"],
                   c=CATEGORY_COLORS[cat], alpha=0.5, s=sub["num_wcs"] * 15,
                   label=cat, edgecolors="white", linewidth=0.3)

    # Add correlation
    valid = multi_wc.dropna(subset=["height_cm", "career_span"])
    if len(valid) > 10:
        r, p = sp_stats.pearsonr(valid["height_cm"], valid["career_span"])
        ax.text(0.05, 0.95, f"r = {r:.3f}, p = {p:.3f}",
                transform=ax.transAxes, fontsize=10, va="top",
                bbox=dict(boxstyle="round,pad=0.3", fc="lightyellow", alpha=0.9, ec="gray"))

    ax.set_xlabel("Height (cm)")
    ax.set_ylabel("Career Span (years between first and last WC)")
    ax.set_title("B. Height vs Career Longevity\n(Bubble size = num. of WCs)")
    ax.legend(fontsize=9)

    fig.suptitle("Career Span Giants: Do Taller Players Last Longer on the World Stage?",
                 fontsize=15, fontweight="bold", y=1.02)
    plt.tight_layout()
    path = FIGURES_DIR / "fig20_career_span_giants.png"
    fig.savefig(path, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {path}")


# ===================================================================
# FIGURE 21: "The South Asian Catch-Up" — South Asian player heights
# are converging toward Oceanian/European heights
# ===================================================================
def fig21_south_asian_catchup(df):
    """Regional convergence plot — are South Asian players catching up?"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))

    # Panel A: Regional mean height over time
    ax = axes[0, 0]
    for region, color in REGION_COLORS.items():
        sub = df[df["region"] == region]
        yearly = sub.groupby("tournament_year")["height_cm"].mean()
        if len(yearly) >= 3:
            ax.plot(yearly.index, yearly.values, "o-",
                    color=color, label=region, markersize=5, linewidth=2)
    ax.set_xlabel("Tournament Year")
    ax.set_ylabel("Mean Height (cm)")
    ax.set_title("A. Regional Height Trends Over Time")
    ax.legend(fontsize=9)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    # Panel B: Height EXCESS over time by region (population-adjusted)
    ax = axes[0, 1]
    for region, color in REGION_COLORS.items():
        sub = df[df["region"] == region]
        yearly = sub.groupby("tournament_year")["height_excess"].mean()
        if len(yearly) >= 3:
            ax.plot(yearly.index, yearly.values, "o-",
                    color=color, label=region, markersize=5, linewidth=2)
    ax.axhline(y=0, color="gray", linestyle="--", linewidth=0.8, alpha=0.5)
    ax.set_xlabel("Tournament Year")
    ax.set_ylabel("Height Excess (cm)")
    ax.set_title("B. Population-Adjusted Height Excess\n(Sport-Specific Selection)")
    ax.legend(fontsize=9)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    # Panel C: Gap between tallest region and shortest region over time
    ax = axes[1, 0]
    regional_yearly = df.groupby(["tournament_year", "region"])["height_cm"].mean().unstack()
    if "Oceanian" in regional_yearly.columns and "South Asian" in regional_yearly.columns:
        gap = regional_yearly["Oceanian"] - regional_yearly["South Asian"]
        ax.plot(gap.index, gap.values, "o-", color="#333", linewidth=2, markersize=6)
        ax.fill_between(gap.index, 0, gap.values, alpha=0.2, color="#e74c3c")

        # Add trend line
        valid = gap.dropna()
        if len(valid) >= 5:
            z = np.polyfit(valid.index.astype(float), valid.values, 1)
            p_line = np.poly1d(z)
            x_range = np.linspace(valid.index.min(), valid.index.max(), 100)
            ax.plot(x_range, p_line(x_range), "--", color="#e74c3c", linewidth=1.5,
                    label=f"Trend: {z[0]:+.3f} cm/yr")
            ax.legend(fontsize=9)

    ax.set_xlabel("Tournament Year")
    ax.set_ylabel("Height Gap (cm)")
    ax.set_title("C. Oceanian - South Asian Height Gap\n(Convergence = declining gap)")
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    # Panel D: Country-level excess comparison (IND, SL, PAK vs AUS, ENG, NZL)
    ax = axes[1, 1]
    sa_countries = ["IND", "PAK", "SL"]
    anglo_countries = ["AUS", "ENG", "NZL"]

    for country in sa_countries + anglo_countries:
        sub = df[df["country"] == country]
        yearly = sub.groupby("tournament_year")["height_excess"].mean()
        if len(yearly) >= 3:
            style = "-" if country in sa_countries else "--"
            ax.plot(yearly.index, yearly.values, f"o{style}",
                    color=COUNTRY_COLORS[country], label=COUNTRY_NAMES[country],
                    markersize=4, linewidth=1.5)
    ax.axhline(y=0, color="gray", linestyle="--", linewidth=0.8, alpha=0.5)
    ax.set_xlabel("Tournament Year")
    ax.set_ylabel("Height Excess (cm)")
    ax.set_title("D. Country-Level Height Excess Trends\n(Solid = South Asian, Dashed = Anglo)")
    ax.legend(fontsize=8, ncol=2)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    fig.suptitle("The South Asian Catch-Up: Convergence in Cricket's Height Selection",
                 fontsize=15, fontweight="bold", y=1.02)
    plt.tight_layout()
    path = FIGURES_DIR / "fig21_south_asian_catchup.png"
    fig.savefig(path, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {path}")


# ===================================================================
# FIGURE 22: "The Ridgeline Plot" — Distribution of heights across
# decades (joy/ridgeline plot)
# ===================================================================
def fig22_ridgeline_decades(df):
    """Ridgeline/joy plot: height distribution evolution across decades."""
    fig, ax = plt.subplots(figsize=(10, 10))

    # Create decade bins
    df_copy = df.copy()
    df_copy["decade"] = (df_copy["tournament_year"] // 10) * 10
    decades = sorted(df_copy["decade"].dropna().unique())

    overlap = 0.6
    n_decades = len(decades)
    colors = plt.cm.magma(np.linspace(0.2, 0.85, n_decades))

    for i, decade in enumerate(decades):
        sub = df_copy[df_copy["decade"] == decade]["height_cm"].dropna()
        if len(sub) < 10:
            continue

        # KDE
        x_range = np.linspace(155, 210, 200)
        kde = sp_stats.gaussian_kde(sub)
        y_kde = kde(x_range)

        # Scale and offset
        y_kde_scaled = y_kde / y_kde.max() * overlap
        baseline = i

        ax.fill_between(x_range, baseline, baseline + y_kde_scaled,
                        alpha=0.7, color=colors[i], edgecolor="black", linewidth=0.5)
        ax.plot(x_range, baseline + y_kde_scaled, color="black", linewidth=0.8)

        # Label
        ax.text(155, baseline + 0.05, f"{int(decade)}s (n={len(sub)})",
                fontsize=10, fontweight="bold", va="bottom")

        # Mean marker
        mean_h = sub.mean()
        ax.plot(mean_h, baseline + kde(mean_h) / y_kde.max() * overlap,
                "v", color="white", markersize=6, markeredgecolor="black", markeredgewidth=0.8)
        ax.text(mean_h, baseline - 0.05, f"{mean_h:.1f}",
                ha="center", fontsize=7, color="gray")

    ax.set_xlabel("Height (cm)", fontsize=12)
    ax.set_yticks([])
    ax.set_title("Evolution of Cricket Player Height Distribution by Decade",
                 fontsize=14, fontweight="bold")
    ax.set_xlim(155, 210)

    # Remove y-axis spine
    ax.spines["left"].set_visible(False)

    plt.tight_layout()
    path = FIGURES_DIR / "fig22_ridgeline_decades.png"
    fig.savefig(path, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {path}")


# ===================================================================
# FIGURE 23: "The All-Rounder Effect" — Players flagged as
# CATEGORY_AMBIGUOUS vs clear categories
# ===================================================================
def fig23_allrounder_effect(df):
    """Height of ambiguous (all-rounder) players vs clear role players."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Panel A: Ambiguous vs non-ambiguous height distributions
    ax = axes[0]
    df_copy = df.copy()
    df_copy["is_ambiguous"] = df_copy["flag"].str.contains("CATEGORY_AMBIGUOUS", na=False)

    ambig = df_copy[df_copy["is_ambiguous"]]["height_cm"].dropna()
    clear = df_copy[~df_copy["is_ambiguous"]]["height_cm"].dropna()

    if len(ambig) > 5:
        data_to_plot = [clear.values, ambig.values]
        labels = [f"Clear Role\n(n={len(clear)})", f"Ambiguous/All-Rounder\n(n={len(ambig)})"]
        colors = ["#3498db", "#e74c3c"]

        bp = ax.boxplot(data_to_plot, labels=labels, patch_artist=True,
                        widths=0.5, flierprops=dict(markersize=3))
        for patch, color in zip(bp["boxes"], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)

        # t-test
        t_stat, p_val = sp_stats.ttest_ind(clear, ambig)
        ax.text(0.5, 0.95, f"t = {t_stat:.2f}, p = {p_val:.3f}",
                transform=ax.transAxes, ha="center", va="top", fontsize=10,
                bbox=dict(boxstyle="round,pad=0.3", fc="lightyellow", alpha=0.9, ec="gray"))
    else:
        ax.text(0.5, 0.5, "Insufficient ambiguous players", transform=ax.transAxes, ha="center")

    ax.set_ylabel("Height (cm)")
    ax.set_title("A. All-Rounders vs Specialists: Height Comparison")

    # Panel B: Ambiguous players by assigned category
    ax = axes[1]
    ambig_players = df_copy[df_copy["is_ambiguous"]]
    if len(ambig_players) > 5:
        cat_counts = ambig_players["category"].value_counts()
        cat_means = ambig_players.groupby("category")["height_cm"].mean()

        x_pos = range(len(cat_counts))
        bar_colors = [CATEGORY_COLORS.get(c, "#999") for c in cat_counts.index]
        bars = ax.bar(x_pos, cat_counts.values, color=bar_colors, edgecolor="white", width=0.6)
        ax.set_xticks(x_pos)
        ax.set_xticklabels(cat_counts.index)
        ax.set_ylabel("Count of Ambiguous Players")
        ax.set_title("B. Where All-Rounders Are Classified")

        # Secondary axis for mean height
        ax2 = ax.twinx()
        for i, cat in enumerate(cat_counts.index):
            if cat in cat_means.index:
                ax2.plot(i, cat_means[cat], "D", color="black", markersize=10, zorder=5)
                ax2.text(i + 0.15, cat_means[cat], f"{cat_means[cat]:.1f}",
                         fontsize=8, fontweight="bold")
        ax2.set_ylabel("Mean Height of Ambiguous Players (cm)")
    else:
        ax.text(0.5, 0.5, "Insufficient data", transform=ax.transAxes, ha="center")

    fig.suptitle("The All-Rounder Effect: Do Multi-Skilled Players Have a Different Height Profile?",
                 fontsize=14, fontweight="bold", y=1.02)
    plt.tight_layout()
    path = FIGURES_DIR / "fig23_allrounder_effect.png"
    fig.savefig(path, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {path}")


# ===================================================================
# FIGURE 24: "Team Silhouette" — Height 'silhouette' for a complete XI
# showing batting order 1-11 for select iconic teams
# ===================================================================
def fig24_team_silhouettes(df):
    """Height silhouettes for iconic World Cup XIs across eras."""
    # Pick iconic teams
    iconic_teams = [
        ("odi-1975", "WI", "WI 1975 (Clive Lloyd)"),
        ("odi-1983", "IND", "India 1983 (Kapil Dev)"),
        ("odi-1999", "AUS", "Australia 1999"),
        ("odi-2003", "AUS", "Australia 2003"),
        ("odi-2011", "IND", "India 2011"),
        ("odi-2019", "ENG", "England 2019"),
        ("t20-2007", "IND", "India T20 2007"),
        ("odi-2023", "AUS", "Australia 2023"),
    ]

    fig, axes = plt.subplots(2, 4, figsize=(20, 10))
    axes = axes.flatten()

    for idx, (tid, country, label) in enumerate(iconic_teams):
        ax = axes[idx]
        team = df[(df["tournament_id"] == tid) & (df["country"] == country)].sort_values("batting_position")

        if len(team) == 0:
            ax.text(0.5, 0.5, f"{label}\nNo data", transform=ax.transAxes, ha="center")
            ax.set_title(label)
            continue

        positions = team["batting_position"].values
        heights = team["height_cm"].values
        categories = team["category"].values
        names = team["full_name"].values

        bar_colors = [CATEGORY_COLORS.get(cat, "#999") for cat in categories]

        bars = ax.bar(positions, heights, color=bar_colors, edgecolor="white",
                      width=0.7, zorder=3)

        # Add player name labels (rotated)
        for pos, h, name, cat in zip(positions, heights, names, categories):
            short_name = name.split()[-1] if " " in name else name
            if len(short_name) > 10:
                short_name = short_name[:8] + ".."
            ax.text(pos, h + 0.5, short_name, ha="center", va="bottom",
                    fontsize=6, rotation=45, fontweight="bold")

        # Mean line
        mean_h = np.mean(heights)
        ax.axhline(y=mean_h, color="gray", linestyle="--", linewidth=0.8, alpha=0.7)
        ax.text(11.5, mean_h, f"{mean_h:.1f}", fontsize=7, va="center", color="gray")

        ax.set_xlim(0.3, 11.7)
        ax.set_ylim(155, 205)
        ax.set_xticks(range(1, 12))
        ax.set_xlabel("Batting Position")
        if idx % 4 == 0:
            ax.set_ylabel("Height (cm)")
        ax.set_title(label, fontsize=10, fontweight="bold")

    # Common legend
    legend_elements = [Patch(facecolor=CATEGORY_COLORS[c], label=c) for c in CATEGORY_ORDER]
    fig.legend(handles=legend_elements, loc="lower center", ncol=4, fontsize=10,
               bbox_to_anchor=(0.5, -0.02), frameon=True)

    fig.suptitle("Height Silhouettes of Iconic World Cup XIs\n(Each bar = one player, ordered by batting position)",
                 fontsize=15, fontweight="bold", y=1.02)
    plt.tight_layout()
    path = FIGURES_DIR / "fig24_team_silhouettes.png"
    fig.savefig(path, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {path}")


# ===================================================================
# FIGURE 25: "The 180cm Club" — What % of players are above 180cm
# and 185cm, tracked over time
# ===================================================================
def fig25_height_thresholds(df):
    """Percentage of players exceeding height thresholds over time."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))

    # Panel A: % above 180cm over time (all players)
    ax = axes[0, 0]
    thresholds = [175, 180, 185, 190]
    threshold_colors = ["#2ecc71", "#3498db", "#e74c3c", "#9b59b6"]
    for threshold, color in zip(thresholds, threshold_colors):
        pct = df.groupby("tournament_year")["height_cm"].apply(
            lambda x: (x >= threshold).sum() / len(x) * 100
        )
        ax.plot(pct.index, pct.values, "o-", color=color,
                label=f">= {threshold} cm", markersize=4, linewidth=1.5)
    ax.set_xlabel("Tournament Year")
    ax.set_ylabel("% of Players")
    ax.set_title("A. Players Exceeding Height Thresholds Over Time")
    ax.legend(fontsize=9)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    # Panel B: % above 185cm by category
    ax = axes[0, 1]
    for cat in CATEGORY_ORDER:
        sub = df[df["category"] == cat]
        pct = sub.groupby("tournament_year")["height_cm"].apply(
            lambda x: (x >= 185).sum() / len(x) * 100
        )
        ax.plot(pct.index, pct.values, "o-", color=CATEGORY_COLORS[cat],
                label=cat, markersize=4, linewidth=1.5)
    ax.set_xlabel("Tournament Year")
    ax.set_ylabel("% of Players >= 185 cm")
    ax.set_title("B. '6-Foot Club' (185cm+) by Category")
    ax.legend(fontsize=9)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    # Panel C: % above 180cm by country
    ax = axes[1, 0]
    for country in NATION_ORDER:
        sub = df[df["country"] == country]
        pct = sub.groupby("tournament_year")["height_cm"].apply(
            lambda x: (x >= 180).sum() / len(x) * 100
        )
        if len(pct) >= 3:
            ax.plot(pct.index, pct.values, "o-", color=COUNTRY_COLORS[country],
                    label=COUNTRY_NAMES[country], markersize=3, linewidth=1.2, alpha=0.8)
    ax.set_xlabel("Tournament Year")
    ax.set_ylabel("% of Players >= 180 cm")
    ax.set_title("C. '180 Club' Membership by Country")
    ax.legend(fontsize=8, ncol=2)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    # Panel D: Tallest player in each tournament
    ax = axes[1, 1]
    tallest = df.loc[df.groupby("tournament_year")["height_cm"].idxmax()]
    tallest = tallest.sort_values("tournament_year")

    bar_colors = [COUNTRY_COLORS.get(c, "#999") for c in tallest["country"]]
    bars = ax.bar(range(len(tallest)), tallest["height_cm"].values,
                  color=bar_colors, edgecolor="white", width=0.7)

    # Labels
    labels = []
    for _, row in tallest.iterrows():
        yr = int(row["tournament_year"])
        fmt = row["format"]
        labels.append(f"{fmt}\n{yr}")
    ax.set_xticks(range(len(tallest)))
    ax.set_xticklabels(labels, fontsize=6, rotation=45, ha="right")

    # Annotate with player name
    for i, (_, row) in enumerate(tallest.iterrows()):
        name = row["full_name"].split()[-1] if " " in row["full_name"] else row["full_name"]
        ax.text(i, row["height_cm"] + 0.5,
                f'{name}\n({row["country"]})\n{row["height_cm"]:.0f}cm',
                ha="center", fontsize=6, fontweight="bold", va="bottom")

    ax.set_ylabel("Height (cm)")
    ax.set_title("D. Tallest Player in Each World Cup")
    ax.set_ylim(bottom=180)

    fig.suptitle("The Height Threshold Revolution: How the Tall End Is Growing",
                 fontsize=15, fontweight="bold", y=1.02)
    plt.tight_layout()
    path = FIGURES_DIR / "fig25_height_thresholds.png"
    fig.savefig(path, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {path}")


# ===================================================================
# FIGURE 26: "Height Clustering" — Dendrogram/cluster showing which
# nations have the most similar height profiles
# ===================================================================
def fig26_nation_clustering(df):
    """Cluster nations by their height profile similarity."""
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))

    # Build feature matrix: mean height by category for each country
    features = []
    labels = []
    for country in NATION_ORDER:
        sub = df[df["country"] == country]
        row = []
        for cat in CATEGORY_ORDER:
            cat_sub = sub[sub["category"] == cat]["height_cm"]
            row.append(cat_sub.mean() if len(cat_sub) > 0 else np.nan)
        # Also add mean excess and height trend slope
        excess = sub["height_excess"].mean()
        row.append(excess if pd.notna(excess) else 0)
        features.append(row)
        labels.append(COUNTRY_NAMES[country])

    feature_matrix = np.array(features)

    # Handle NaN by replacing with column mean
    col_means = np.nanmean(feature_matrix, axis=0)
    for i in range(feature_matrix.shape[0]):
        for j in range(feature_matrix.shape[1]):
            if np.isnan(feature_matrix[i, j]):
                feature_matrix[i, j] = col_means[j]

    # Panel A: Dendrogram
    ax = axes[0]
    Z = linkage(feature_matrix, method="ward")
    dendrogram(Z, labels=labels, ax=ax, leaf_rotation=45, leaf_font_size=10,
               color_threshold=10)
    ax.set_ylabel("Distance (Ward)")
    ax.set_title("A. Hierarchical Clustering of Nations\n(by height profiles)")

    # Panel B: Radar/spider chart of height profiles
    ax = axes[1]
    categories_radar = CATEGORY_ORDER + ["Excess"]
    N = len(categories_radar)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    angles += angles[:1]

    ax = fig.add_subplot(122, polar=True)

    for i, country in enumerate(NATION_ORDER):
        values = feature_matrix[i].tolist()
        # Normalize to 0-1 range per feature
        normed = []
        for j, v in enumerate(values):
            col_min = feature_matrix[:, j].min()
            col_max = feature_matrix[:, j].max()
            if col_max - col_min > 0:
                normed.append((v - col_min) / (col_max - col_min))
            else:
                normed.append(0.5)
        normed += normed[:1]
        ax.plot(angles, normed, "o-", color=COUNTRY_COLORS[country],
                label=COUNTRY_NAMES[country], linewidth=1.5, markersize=3, alpha=0.7)
        ax.fill(angles, normed, color=COUNTRY_COLORS[country], alpha=0.05)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories_radar, fontsize=9)
    ax.set_title("B. Normalized Height Profiles\n(Radar Chart)", y=1.1)
    ax.legend(loc="lower left", bbox_to_anchor=(-0.2, -0.15), ncol=4, fontsize=8)

    fig.suptitle("National Height DNA: How Cricket Nations Compare",
                 fontsize=15, fontweight="bold", y=1.05)
    plt.tight_layout()
    path = FIGURES_DIR / "fig26_nation_clustering.png"
    fig.savefig(path, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {path}")


# ===================================================================
# FIGURE 27: "The Data Quality Mosaic" — Height verification status
# by era and country
# ===================================================================
def fig27_data_quality_mosaic(df):
    """Data quality overview: verified vs estimated heights across eras/countries."""
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    df_copy = df.copy()
    df_copy["height_verified"] = df_copy["height_verified"].astype(str).str.lower().isin(["true", "1"])

    # Panel A: Verification rate by era
    ax = axes[0]
    era_verify = df_copy.groupby("era")["height_verified"].mean() * 100
    bars = ax.bar([ERA_LABELS.get(int(e), str(e)) for e in era_verify.index],
                  era_verify.values,
                  color=["#e74c3c" if v < 50 else "#f39c12" if v < 70 else "#2ecc71"
                         for v in era_verify.values],
                  edgecolor="white", width=0.6)
    for bar, val in zip(bars, era_verify.values):
        ax.text(bar.get_x() + bar.get_width() / 2, val + 1,
                f"{val:.0f}%", ha="center", fontsize=10, fontweight="bold")
    ax.set_ylabel("% Height Verified")
    ax.set_title("A. Height Verification Rate by Era")
    ax.set_ylim(0, 105)

    # Panel B: Verification rate by country
    ax = axes[1]
    country_verify = df_copy.groupby("country")["height_verified"].mean() * 100
    country_verify = country_verify.reindex(NATION_ORDER)
    bars = ax.barh(
        [COUNTRY_NAMES.get(c, c) for c in country_verify.index],
        country_verify.values,
        color=[COUNTRY_COLORS.get(c, "#999") for c in country_verify.index],
        edgecolor="white", height=0.6,
    )
    for bar, val in zip(bars, country_verify.values):
        ax.text(val + 1, bar.get_y() + bar.get_height() / 2,
                f"{val:.0f}%", va="center", fontsize=9, fontweight="bold")
    ax.set_xlabel("% Height Verified")
    ax.set_title("B. Verification Rate by Country")
    ax.set_xlim(0, 105)

    # Panel C: Flag distribution
    ax = axes[2]
    df_copy["flag_clean"] = df_copy["flag"].fillna("No Flag")
    # Simplify flags
    flag_counts = df_copy["flag_clean"].value_counts().head(8)
    colors_flag = plt.cm.Set3(np.linspace(0, 1, len(flag_counts)))
    wedges, texts, autotexts = ax.pie(
        flag_counts.values, labels=None, autopct="%1.0f%%",
        colors=colors_flag, startangle=90, pctdistance=0.85,
    )
    ax.legend(flag_counts.index, loc="center left", bbox_to_anchor=(1, 0.5), fontsize=8)
    ax.set_title("C. Distribution of Data Quality Flags")

    fig.suptitle("Data Quality Dashboard: How Reliable Is Our Height Data?",
                 fontsize=15, fontweight="bold", y=1.02)
    plt.tight_layout()
    path = FIGURES_DIR / "fig27_data_quality_mosaic.png"
    fig.savefig(path, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {path}")


# ===================================================================
# FIGURE 28: "The Effect Size Dashboard" — Cohen's d for all pairwise
# country and category comparisons
# ===================================================================
def fig28_effect_size_dashboard(df):
    """Cohen's d effect size heatmap for pairwise comparisons."""
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))

    # Panel A: Category pairwise Cohen's d
    ax = axes[0]
    cats = CATEGORY_ORDER
    d_matrix = np.zeros((len(cats), len(cats)))
    for i, c1 in enumerate(cats):
        for j, c2 in enumerate(cats):
            h1 = df[df["category"] == c1]["height_cm"].dropna()
            h2 = df[df["category"] == c2]["height_cm"].dropna()
            if len(h1) > 2 and len(h2) > 2:
                pooled_std = np.sqrt(((len(h1) - 1) * h1.std() ** 2 + (len(h2) - 1) * h2.std() ** 2) /
                                     (len(h1) + len(h2) - 2))
                if pooled_std > 0:
                    d_matrix[i, j] = (h1.mean() - h2.mean()) / pooled_std

    if HAS_SEABORN:
        sns.heatmap(d_matrix, annot=True, fmt=".2f", cmap="RdBu_r", center=0,
                    xticklabels=cats, yticklabels=cats, ax=ax,
                    linewidths=1, linecolor="white",
                    cbar_kws={"label": "Cohen's d"})
    else:
        im = ax.imshow(d_matrix, cmap="RdBu_r", vmin=-1.5, vmax=1.5)
        ax.set_xticks(range(len(cats)))
        ax.set_xticklabels(cats)
        ax.set_yticks(range(len(cats)))
        ax.set_yticklabels(cats)
        for i in range(len(cats)):
            for j in range(len(cats)):
                ax.text(j, i, f"{d_matrix[i, j]:.2f}", ha="center", va="center", fontsize=10)
        fig.colorbar(im, ax=ax, label="Cohen's d")

    ax.set_title("A. Effect Size: Category Pairwise (Cohen's d)")

    # Panel B: Country pairwise Cohen's d (BAT only)
    ax = axes[1]
    bat = df[df["category"] == "BAT"]
    countries = NATION_ORDER
    d_matrix_c = np.zeros((len(countries), len(countries)))
    for i, c1 in enumerate(countries):
        for j, c2 in enumerate(countries):
            h1 = bat[bat["country"] == c1]["height_cm"].dropna()
            h2 = bat[bat["country"] == c2]["height_cm"].dropna()
            if len(h1) > 2 and len(h2) > 2:
                pooled_std = np.sqrt(((len(h1) - 1) * h1.std() ** 2 + (len(h2) - 1) * h2.std() ** 2) /
                                     (len(h1) + len(h2) - 2))
                if pooled_std > 0:
                    d_matrix_c[i, j] = (h1.mean() - h2.mean()) / pooled_std

    country_labels = [COUNTRY_NAMES.get(c, c) for c in countries]
    if HAS_SEABORN:
        sns.heatmap(d_matrix_c, annot=True, fmt=".2f", cmap="RdBu_r", center=0,
                    xticklabels=country_labels, yticklabels=country_labels, ax=ax,
                    linewidths=1, linecolor="white",
                    cbar_kws={"label": "Cohen's d"})
    else:
        im = ax.imshow(d_matrix_c, cmap="RdBu_r", vmin=-1.5, vmax=1.5)
        ax.set_xticks(range(len(countries)))
        ax.set_xticklabels(country_labels, rotation=45, ha="right")
        ax.set_yticks(range(len(countries)))
        ax.set_yticklabels(country_labels)
        for i in range(len(countries)):
            for j in range(len(countries)):
                ax.text(j, i, f"{d_matrix_c[i, j]:.2f}", ha="center", va="center", fontsize=8)
        fig.colorbar(im, ax=ax, label="Cohen's d")

    ax.set_title("B. Effect Size: Country Pairwise for BAT (Cohen's d)")
    ax.tick_params(axis="x", rotation=45)

    fig.suptitle("Effect Size Dashboard: How Big Are the Height Differences?",
                 fontsize=15, fontweight="bold", y=1.02)
    plt.tight_layout()
    path = FIGURES_DIR / "fig28_effect_size_dashboard.png"
    fig.savefig(path, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {path}")


# ===================================================================
# FIGURE 29: "The Height Inequality" — Gini coefficient of heights
# within teams (are some teams more "unequal" in height?)
# ===================================================================
def fig29_height_inequality(df):
    """Height inequality within teams — Gini coefficient and coefficient of variation."""
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))

    def gini(arr):
        arr = np.sort(arr)
        n = len(arr)
        if n < 2 or arr.sum() == 0:
            return 0
        index = np.arange(1, n + 1)
        return (2 * np.sum(index * arr) - (n + 1) * np.sum(arr)) / (n * np.sum(arr))

    # Calculate per-team Gini and CV
    team_ineq = []
    for (tid, country), grp in df.groupby(["tournament_id", "country"]):
        heights = grp["height_cm"].dropna().values
        if len(heights) >= 8:
            team_ineq.append({
                "tournament_id": tid,
                "country": country,
                "tournament_year": grp["tournament_year"].iloc[0],
                "gini": gini(heights),
                "cv": heights.std() / heights.mean() * 100,  # CV as %
                "region": grp["region"].iloc[0],
            })
    ineq = pd.DataFrame(team_ineq)

    if len(ineq) == 0:
        plt.close(fig)
        print("  Skipping fig29: insufficient data.")
        return

    # Panel A: CV over time by region
    ax = axes[0]
    for region, color in REGION_COLORS.items():
        sub = ineq[ineq["region"] == region]
        yearly = sub.groupby("tournament_year")["cv"].mean()
        if len(yearly) >= 3:
            ax.plot(yearly.index, yearly.values, "o-",
                    color=color, label=region, markersize=4, linewidth=1.5)

    # Overall trend
    overall = ineq.groupby("tournament_year")["cv"].mean()
    ax.plot(overall.index, overall.values, "ks--", linewidth=2, markersize=6,
            label="Overall", zorder=5)

    ax.set_xlabel("Tournament Year")
    ax.set_ylabel("Coefficient of Variation (%)")
    ax.set_title("A. Within-Team Height Inequality Over Time\n(Higher CV = more height diversity)")
    ax.legend(fontsize=9)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    # Panel B: Country ranking by mean CV
    ax = axes[1]
    country_cv = ineq.groupby("country")["cv"].agg(["mean", "std", "count"]).reindex(NATION_ORDER)
    country_cv["sem"] = country_cv["std"] / np.sqrt(country_cv["count"])
    country_cv = country_cv.sort_values("mean")

    bar_colors = [COUNTRY_COLORS.get(c, "#999") for c in country_cv.index]
    ax.barh(
        [COUNTRY_NAMES.get(c, c) for c in country_cv.index],
        country_cv["mean"],
        xerr=country_cv["sem"] * 1.96,
        color=bar_colors, edgecolor="white", height=0.6, capsize=3,
    )
    for i, (nation, row) in enumerate(country_cv.iterrows()):
        ax.text(row["mean"] + row["sem"] * 1.96 + 0.05, i,
                f'{row["mean"]:.2f}%', va="center", fontsize=9, fontweight="bold")

    ax.set_xlabel("Mean Coefficient of Variation (%)")
    ax.set_title("B. Mean Height Inequality by Country\n(Higher = more varied XIs)")

    fig.suptitle("Height Inequality: Which Teams Are Most Diverse in Stature?",
                 fontsize=15, fontweight="bold", y=1.02)
    plt.tight_layout()
    path = FIGURES_DIR / "fig29_height_inequality.png"
    fig.savefig(path, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {path}")


# ===================================================================
# FIGURE 30: "The Generation Game" — Birth cohort analysis showing
# how birth decades of WC players have shifted
# ===================================================================
def fig30_generation_game(df):
    """Birth cohort analysis: which generations produced the most WC cricketers?"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))

    df_copy = df.copy()
    df_copy["birth_decade"] = (df_copy["birth_year"] // 10) * 10

    # Panel A: Number of players by birth decade and category
    ax = axes[0, 0]
    unique_players = df_copy.drop_duplicates(subset="player_id")
    cross = unique_players.groupby(["birth_decade", "category"]).size().unstack(fill_value=0)
    cross = cross.reindex(columns=CATEGORY_ORDER, fill_value=0)
    cross.plot(kind="bar", stacked=True, ax=ax,
               color=[CATEGORY_COLORS[c] for c in cross.columns],
               edgecolor="white", width=0.7)
    ax.set_xlabel("Birth Decade")
    ax.set_ylabel("Number of Unique Players")
    ax.set_title("A. WC Players by Birth Decade and Category")
    ax.legend(title="Category", fontsize=9)
    ax.tick_params(axis="x", rotation=0)

    # Panel B: Mean height by birth decade
    ax = axes[0, 1]
    for cat in ["BAT", "FAST"]:
        sub = unique_players[unique_players["category"] == cat]
        decade_means = sub.groupby("birth_decade")["height_cm"].mean()
        ax.plot(decade_means.index, decade_means.values, "o-",
                color=CATEGORY_COLORS[cat], label=cat, markersize=5, linewidth=2)

    # Population baseline by birth decade
    pop_means = unique_players.groupby("birth_decade")["pop_height_birth_cohort"].mean()
    ax.plot(pop_means.index, pop_means.values, "s--", color="#999",
            label="Population baseline", markersize=4, linewidth=1.5)

    ax.set_xlabel("Birth Decade")
    ax.set_ylabel("Mean Height (cm)")
    ax.set_title("B. Height by Birth Decade (BAT vs FAST vs Population)")
    ax.legend(fontsize=9)

    # Panel C: Height excess by birth decade and country
    ax = axes[1, 0]
    for country in ["IND", "AUS", "ENG", "WI"]:
        sub = unique_players[unique_players["country"] == country]
        decade_excess = sub.groupby("birth_decade")["height_excess"].mean()
        if len(decade_excess) >= 3:
            ax.plot(decade_excess.index, decade_excess.values, "o-",
                    color=COUNTRY_COLORS[country], label=COUNTRY_NAMES[country],
                    markersize=4, linewidth=1.5)
    ax.axhline(y=0, color="gray", linestyle="--", linewidth=0.8, alpha=0.5)
    ax.set_xlabel("Birth Decade")
    ax.set_ylabel("Height Excess (cm)")
    ax.set_title("C. Height Excess by Birth Decade\n(Selected Countries)")
    ax.legend(fontsize=9)

    # Panel D: Mean age at WC debut by birth decade
    ax = axes[1, 1]
    first_wc = df_copy.sort_values("tournament_year").drop_duplicates(subset="player_id", keep="first")
    decade_age = first_wc.groupby("birth_decade")["age_at_tournament"].agg(["mean", "std", "count"])
    decade_age["sem"] = decade_age["std"] / np.sqrt(decade_age["count"])

    ax.errorbar(decade_age.index, decade_age["mean"],
                yerr=decade_age["sem"] * 1.96,
                fmt="o-", color="#8e44ad", linewidth=2, markersize=6, capsize=3)
    for idx_val, row in decade_age.iterrows():
        ax.text(idx_val, row["mean"] + row["sem"] * 1.96 + 0.3,
                f'n={int(row["count"])}', ha="center", fontsize=7, color="gray")

    ax.set_xlabel("Birth Decade")
    ax.set_ylabel("Mean Age at WC Debut")
    ax.set_title("D. Age at WC Debut by Birth Decade")

    fig.suptitle("The Generation Game: Birth Cohort Analysis of World Cup Cricketers",
                 fontsize=15, fontweight="bold", y=1.02)
    plt.tight_layout()
    path = FIGURES_DIR / "fig30_generation_game.png"
    fig.savefig(path, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {path}")


# ===================================================================
# FIGURE 31: "Country Category Composition" — Stacked area chart
# showing how team composition (% of each category) has evolved
# ===================================================================
def fig31_team_composition_evolution(df):
    """How team composition by category has evolved over time."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))

    # Panel A: Overall composition over time (stacked area)
    ax = axes[0, 0]
    comp = df.groupby(["tournament_year", "category"]).size().unstack(fill_value=0)
    comp_pct = comp.div(comp.sum(axis=1), axis=0) * 100
    comp_pct = comp_pct.reindex(columns=CATEGORY_ORDER, fill_value=0)

    ax.stackplot(
        comp_pct.index, [comp_pct[c].values for c in CATEGORY_ORDER],
        labels=CATEGORY_ORDER,
        colors=[CATEGORY_COLORS[c] for c in CATEGORY_ORDER],
        alpha=0.8,
    )
    ax.set_xlabel("Tournament Year")
    ax.set_ylabel("% of Playing XI")
    ax.set_title("A. Team Composition Over Time (All Nations)")
    ax.legend(loc="upper right", fontsize=9)
    ax.set_ylim(0, 100)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    # Panel B: FAST bowler count per team over time
    ax = axes[0, 1]
    fast_count = df[df["category"] == "FAST"].groupby(["tournament_year", "country"]).size().reset_index(name="n_fast")
    for country in NATION_ORDER:
        sub = fast_count[fast_count["country"] == country]
        if len(sub) >= 3:
            ax.plot(sub["tournament_year"], sub["n_fast"], "o-",
                    color=COUNTRY_COLORS[country], label=COUNTRY_NAMES[country],
                    markersize=3, linewidth=1.2, alpha=0.8)

    overall_fast = fast_count.groupby("tournament_year")["n_fast"].mean()
    ax.plot(overall_fast.index, overall_fast.values, "ks--", linewidth=2, markersize=6,
            label="Overall mean", zorder=5)

    ax.set_xlabel("Tournament Year")
    ax.set_ylabel("Fast Bowlers per XI")
    ax.set_title("B. Number of Fast Bowlers per Team Over Time")
    ax.legend(fontsize=7, ncol=3)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    # Panel C: Mean team height weighted by FAST bowler count
    ax = axes[1, 0]
    team_data = df.groupby(["tournament_id", "country"]).agg(
        mean_height=("height_cm", "mean"),
        n_fast=("category", lambda x: (x == "FAST").sum()),
        tournament_year=("tournament_year", "first"),
    ).reset_index()

    # Scatter: more fast bowlers -> taller team?
    colors = [COUNTRY_COLORS.get(c, "#999") for c in team_data["country"]]
    ax.scatter(team_data["n_fast"], team_data["mean_height"],
               c=colors, alpha=0.5, s=30, edgecolors="white", linewidth=0.3)

    # Trend line
    valid = team_data.dropna(subset=["n_fast", "mean_height"])
    if len(valid) > 10:
        z = np.polyfit(valid["n_fast"], valid["mean_height"], 1)
        p_line = np.poly1d(z)
        x_range = np.linspace(valid["n_fast"].min(), valid["n_fast"].max(), 50)
        ax.plot(x_range, p_line(x_range), "r--", linewidth=2,
                label=f"Trend: {z[0]:+.2f} cm per extra pacer")
        r, p = sp_stats.pearsonr(valid["n_fast"], valid["mean_height"])
        ax.text(0.05, 0.95, f"r = {r:.3f}, p = {p:.3f}",
                transform=ax.transAxes, fontsize=9, va="top",
                bbox=dict(boxstyle="round,pad=0.3", fc="lightyellow", alpha=0.9, ec="gray"))

    ax.set_xlabel("Number of Fast Bowlers in XI")
    ax.set_ylabel("Mean Team Height (cm)")
    ax.set_title("C. More Fast Bowlers = Taller Teams?")
    ax.legend(fontsize=9)

    # Panel D: ODI vs T20 composition
    ax = axes[1, 1]
    for fmt, color in FORMAT_COLORS.items():
        sub = df[df["format"] == fmt]
        comp_fmt = sub.groupby("category").size()
        comp_fmt = comp_fmt.reindex(CATEGORY_ORDER, fill_value=0)
        comp_pct_fmt = comp_fmt / comp_fmt.sum() * 100
        offset = -0.2 if fmt == "ODI" else 0.2
        ax.bar(np.arange(len(CATEGORY_ORDER)) + offset, comp_pct_fmt.values,
               width=0.35, color=color, edgecolor="white", label=fmt, alpha=0.8)

    ax.set_xticks(range(len(CATEGORY_ORDER)))
    ax.set_xticklabels(CATEGORY_ORDER)
    ax.set_ylabel("% of All Player Records")
    ax.set_title("D. Category Distribution: ODI vs T20")
    ax.legend(fontsize=10)

    fig.suptitle("Team Composition Evolution: The Changing Shape of World Cup Cricket",
                 fontsize=15, fontweight="bold", y=1.02)
    plt.tight_layout()
    path = FIGURES_DIR / "fig31_team_composition.png"
    fig.savefig(path, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {path}")


# ===================================================================
# FIGURE 32: "The Outlier Gallery" — Extreme heights and their stories
# ===================================================================
def fig32_outlier_gallery(df):
    """Highlight the extreme outliers — tallest, shortest, biggest excess."""
    fig, axes = plt.subplots(1, 3, figsize=(18, 8))

    # Panel A: Top 15 tallest players ever
    ax = axes[0]
    unique_players = df.drop_duplicates(subset="player_id")
    tallest = unique_players.nlargest(15, "height_cm").sort_values("height_cm")

    colors = [CATEGORY_COLORS.get(cat, "#999") for cat in tallest["category"]]
    bars = ax.barh(range(len(tallest)), tallest["height_cm"],
                   color=colors, edgecolor="white", height=0.7)

    labels = [f'{row["full_name"]} ({row["country"]})' for _, row in tallest.iterrows()]
    ax.set_yticks(range(len(tallest)))
    ax.set_yticklabels(labels, fontsize=8)

    for i, (_, row) in enumerate(tallest.iterrows()):
        ax.text(row["height_cm"] + 0.3, i, f'{row["height_cm"]:.0f} cm',
                va="center", fontsize=8, fontweight="bold")

    ax.set_xlabel("Height (cm)")
    ax.set_title("A. Top 15 Tallest WC Players Ever")
    ax.set_xlim(left=185)

    # Panel B: Top 15 shortest players
    ax = axes[1]
    shortest = unique_players.nsmallest(15, "height_cm").sort_values("height_cm", ascending=False)

    colors = [CATEGORY_COLORS.get(cat, "#999") for cat in shortest["category"]]
    bars = ax.barh(range(len(shortest)), shortest["height_cm"],
                   color=colors, edgecolor="white", height=0.7)

    labels = [f'{row["full_name"]} ({row["country"]})' for _, row in shortest.iterrows()]
    ax.set_yticks(range(len(shortest)))
    ax.set_yticklabels(labels, fontsize=8)

    for i, (_, row) in enumerate(shortest.iterrows()):
        ax.text(row["height_cm"] + 0.3, i, f'{row["height_cm"]:.0f} cm',
                va="center", fontsize=8, fontweight="bold")

    ax.set_xlabel("Height (cm)")
    ax.set_title("B. Top 15 Shortest WC Players Ever")
    max_h = shortest["height_cm"].max()
    ax.set_xlim(left=155, right=max_h + 5)

    # Panel C: Top 15 biggest height excess over population
    ax = axes[2]
    biggest_excess = unique_players.nlargest(15, "height_excess").sort_values("height_excess")

    colors = [CATEGORY_COLORS.get(cat, "#999") for cat in biggest_excess["category"]]
    bars = ax.barh(range(len(biggest_excess)), biggest_excess["height_excess"],
                   color=colors, edgecolor="white", height=0.7)

    labels = [f'{row["full_name"]} ({row["country"]})' for _, row in biggest_excess.iterrows()]
    ax.set_yticks(range(len(biggest_excess)))
    ax.set_yticklabels(labels, fontsize=8)

    for i, (_, row) in enumerate(biggest_excess.iterrows()):
        ax.text(row["height_excess"] + 0.3, i,
                f'+{row["height_excess"]:.1f} cm ({row["height_cm"]:.0f} cm)',
                va="center", fontsize=7, fontweight="bold")

    ax.set_xlabel("Height Excess Over Population (cm)")
    ax.set_title("C. Biggest Height Excess Over Population")

    # Common legend
    legend_elements = [Patch(facecolor=CATEGORY_COLORS[c], label=c) for c in CATEGORY_ORDER]
    fig.legend(handles=legend_elements, loc="lower center", ncol=4, fontsize=10,
               bbox_to_anchor=(0.5, -0.02), frameon=True)

    fig.suptitle("The Outlier Gallery: Cricket's Height Extremes",
                 fontsize=15, fontweight="bold", y=1.02)
    plt.tight_layout()
    path = FIGURES_DIR / "fig32_outlier_gallery.png"
    fig.savefig(path, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {path}")


# ===================================================================
# Main
# ===================================================================

def main():
    if not MERGED_CSV.exists():
        print(f"ERROR: Merged CSV not found: {MERGED_CSV}")
        sys.exit(1)

    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(MERGED_CSV)
    print(f"Loaded {len(df)} player-tournament records from {MERGED_CSV}")

    for col in ["height_cm", "tournament_year", "pop_height_birth_cohort",
                 "height_excess", "era", "birth_year", "age_at_tournament",
                 "batting_position"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df_valid = df[df["height_cm"].notna()].copy()
    print(f"Records with valid height: {len(df_valid)}")

    if len(df_valid) == 0:
        print("ERROR: No records with valid height data.")
        sys.exit(1)

    setup_style()

    print("\nGenerating new figures...")

    figures = [
        ("fig12", fig12_height_arms_race),
        ("fig13", fig13_tallest_vs_shortest_xi),
        ("fig14", fig14_batting_position_height_profile),
        ("fig15", fig15_fast_bat_gap),
        ("fig16", fig16_age_height_relationship),
        ("fig17", fig17_wicketkeeper_paradox),
        ("fig18", fig18_team_height_diversity),
        ("fig19", fig19_spin_vs_fast_by_country),
        ("fig20", fig20_career_span_giants),
        ("fig21", fig21_south_asian_catchup),
        ("fig22", fig22_ridgeline_decades),
        ("fig23", fig23_allrounder_effect),
        ("fig24", fig24_team_silhouettes),
        ("fig25", fig25_height_thresholds),
        ("fig26", fig26_nation_clustering),
        ("fig27", fig27_data_quality_mosaic),
        ("fig28", fig28_effect_size_dashboard),
        ("fig29", fig29_height_inequality),
        ("fig30", fig30_generation_game),
        ("fig31", fig31_team_composition_evolution),
        ("fig32", fig32_outlier_gallery),
    ]

    for name, func in figures:
        try:
            func(df_valid)
        except Exception as e:
            print(f"  ERROR in {name}: {e}")
            import traceback
            traceback.print_exc()

    print(f"\nAll new figures saved to: {FIGURES_DIR}")
    print("Done.")


if __name__ == "__main__":
    main()
