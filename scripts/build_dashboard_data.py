#!/usr/bin/env python3
"""Build dashboard JSON data from processed CSV for the interactive dashboard."""

import csv
import json
import os
import shutil

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, "data", "processed", "all_players.csv")
ANALYSIS_PATH = os.path.join(BASE_DIR, "data", "processed", "analysis_results.json")
FIGURES_SRC = os.path.join(BASE_DIR, "figures")
DOCS_DIR = os.path.join(BASE_DIR, "docs")
DOCS_DATA = os.path.join(DOCS_DIR, "data")
DOCS_FIGURES = os.path.join(DOCS_DIR, "figures")


def read_csv():
    """Read CSV and return list of dicts."""
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def build_column_oriented(rows):
    """Convert row-oriented data to column-oriented JSON for smaller payloads."""
    columns = {
        "player_id": [],
        "full_name": [],
        "country": [],
        "category": [],
        "batting_position": [],
        "birth_year": [],
        "height_cm": [],
        "height_verified": [],
        "pop_height": [],
        "height_excess": [],
        "tournament_id": [],
        "format": [],
        "tournament_year": [],
        "era": [],
        "region": [],
    }
    for r in rows:
        columns["player_id"].append(r["player_id"])
        columns["full_name"].append(r["full_name"])
        columns["country"].append(r["country"])
        columns["category"].append(r["category"])
        columns["batting_position"].append(int(r["batting_position"]))
        columns["birth_year"].append(int(r["birth_year"]))
        columns["height_cm"].append(float(r["height_cm"]))
        columns["height_verified"].append(r["height_verified"] == "True")
        columns["pop_height"].append(float(r["pop_height_birth_cohort"]))
        columns["height_excess"].append(float(r["height_excess"]))
        columns["tournament_id"].append(r["tournament_id"])
        columns["format"].append(r["format"])
        columns["tournament_year"].append(int(r["tournament_year"]))
        columns["era"].append(int(r["era"]))
        columns["region"].append(r["region"])
    return columns


def compute_temporal_stats(rows):
    """Compute mean height per year/category/format for charts."""
    from collections import defaultdict

    buckets = defaultdict(lambda: {"sum": 0, "count": 0, "pop_sum": 0})
    for r in rows:
        year = int(r["tournament_year"])
        cat = r["category"]
        fmt = r["format"]
        h = float(r["height_cm"])
        pop = float(r["pop_height_birth_cohort"])
        # By category
        key = f"{year}|{cat}|ALL"
        buckets[key]["sum"] += h
        buckets[key]["count"] += 1
        buckets[key]["pop_sum"] += pop
        # By format
        key2 = f"{year}|{cat}|{fmt}"
        buckets[key2]["sum"] += h
        buckets[key2]["count"] += 1
        buckets[key2]["pop_sum"] += pop
        # Overall
        key3 = f"{year}|ALL|ALL"
        buckets[key3]["sum"] += h
        buckets[key3]["count"] += 1
        buckets[key3]["pop_sum"] += pop
        key4 = f"{year}|ALL|{fmt}"
        buckets[key4]["sum"] += h
        buckets[key4]["count"] += 1
        buckets[key4]["pop_sum"] += pop

    result = []
    for key, v in sorted(buckets.items()):
        year, cat, fmt = key.split("|")
        result.append({
            "year": int(year),
            "category": cat,
            "format": fmt,
            "mean_height": round(v["sum"] / v["count"], 2),
            "mean_pop": round(v["pop_sum"] / v["count"], 2),
            "count": v["count"],
        })
    return result


def compute_country_stats(rows):
    """Compute mean height per country/category."""
    from collections import defaultdict

    buckets = defaultdict(lambda: {"sum": 0, "count": 0, "excess_sum": 0})
    for r in rows:
        country = r["country"]
        cat = r["category"]
        h = float(r["height_cm"])
        excess = float(r["height_excess"])
        key = f"{country}|{cat}"
        buckets[key]["sum"] += h
        buckets[key]["count"] += 1
        buckets[key]["excess_sum"] += excess
        key2 = f"{country}|ALL"
        buckets[key2]["sum"] += h
        buckets[key2]["count"] += 1
        buckets[key2]["excess_sum"] += excess

    result = []
    for key, v in sorted(buckets.items()):
        country, cat = key.split("|")
        result.append({
            "country": country,
            "category": cat,
            "mean_height": round(v["sum"] / v["count"], 2),
            "mean_excess": round(v["excess_sum"] / v["count"], 2),
            "count": v["count"],
        })
    return result


def build_analysis_stats(rows):
    """Build pre-computed stats for dashboard callouts."""
    with open(ANALYSIS_PATH, "r") as f:
        analysis = json.load(f)

    overall = analysis["table2_descriptive"]["overall"]
    excess = analysis["table2_descriptive"]["excess_by_category"]

    # Overall mean excess across all categories
    total_excess = sum(
        excess["mean"][c] * excess["count"][c] for c in excess["count"]
    )
    total_n = sum(excess["count"].values())
    mean_excess = round(total_excess / total_n, 1)

    stats = {
        "n_observations": overall["n"],
        "n_players": overall["n_unique_players"],
        "n_tournaments": overall["n_tournaments"],
        "mean_excess": mean_excess,
        "mean_height": overall["mean_height"],
        "category_means": analysis["table2_descriptive"]["by_category"]["mean"],
        "category_counts": analysis["table2_descriptive"]["by_category"]["count"],
        "category_excess": excess["mean"],
        "breakpoint_bat": analysis["table7_breakpoint"]["BAT"],
        "format_comparison": analysis["table10_sensitivity"]["format_comparison"],
        "fast_vs_bat": analysis["table10_sensitivity"]["fast_vs_bat"],
        "bat_unadjusted_slope": analysis["table3_unadjusted"]["BAT"]["coefficients"]["tournament_year"]["estimate"],
        "bat_adjusted_slope": analysis["table4_adjusted"]["BAT"]["coefficients"]["tournament_year"]["estimate"],
        "country_slopes": {},
    }
    for country, data in analysis["table5_country"].items():
        stats["country_slopes"][country] = {
            "slope": data["coefficients"]["tournament_year"]["estimate"],
            "p_value": data["coefficients"]["tournament_year"]["p_value"],
            "n": data["n"],
        }

    return stats


def copy_figures():
    """Copy figure PNGs to docs/figures/."""
    os.makedirs(DOCS_FIGURES, exist_ok=True)
    for fname in sorted(os.listdir(FIGURES_SRC)):
        if fname.endswith(".png"):
            src = os.path.join(FIGURES_SRC, fname)
            dst = os.path.join(DOCS_FIGURES, fname)
            shutil.copy2(src, dst)
            print(f"  Copied {fname}")


def main():
    print("Building dashboard data...")
    rows = read_csv()
    print(f"  Read {len(rows)} rows from CSV")

    # Create output dirs
    os.makedirs(DOCS_DATA, exist_ok=True)

    # Column-oriented player data
    columns = build_column_oriented(rows)
    out_path = os.path.join(DOCS_DATA, "dashboard-data.json")
    with open(out_path, "w") as f:
        json.dump(columns, f, separators=(",", ":"))
    size_kb = os.path.getsize(out_path) / 1024
    print(f"  Wrote dashboard-data.json ({size_kb:.0f} KB)")

    # Temporal stats for charts
    temporal = compute_temporal_stats(rows)
    out_path = os.path.join(DOCS_DATA, "temporal-stats.json")
    with open(out_path, "w") as f:
        json.dump(temporal, f, separators=(",", ":"))
    print(f"  Wrote temporal-stats.json")

    # Country stats
    country = compute_country_stats(rows)
    out_path = os.path.join(DOCS_DATA, "country-stats.json")
    with open(out_path, "w") as f:
        json.dump(country, f, separators=(",", ":"))
    print(f"  Wrote country-stats.json")

    # Analysis stats for callouts
    stats = build_analysis_stats(rows)
    out_path = os.path.join(DOCS_DATA, "analysis-stats.json")
    with open(out_path, "w") as f:
        json.dump(stats, f, indent=2)
    print(f"  Wrote analysis-stats.json")

    # Copy figures
    print("Copying figures...")
    copy_figures()

    print("Done!")


if __name__ == "__main__":
    main()
