#!/usr/bin/env python3
"""
merge_all_tournaments.py - Load all tournament JSONs from data/raw/,
flatten into a single DataFrame, compute derived columns, and save to
data/processed/all_players.csv and data/processed/all_players.parquet.

Derived columns added:
  - height_excess  = height_cm - pop_height_birth_cohort
  - region         (South Asian / Oceanian / Caribbean / European / African)

Usage:
    python scripts/merge_all_tournaments.py
"""

import json
import sys
from pathlib import Path

import pandas as pd
import numpy as np

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

REGION_MAP = {
    "IND": "South Asian",
    "PAK": "South Asian",
    "SL": "South Asian",
    "AUS": "Oceanian",
    "NZL": "Oceanian",
    "WI": "Caribbean",
    "ENG": "European",
    "RSA": "African",
}

OUTPUT_COLUMNS = [
    "player_id",
    "full_name",
    "country",
    "category",
    "batting_position",
    "date_of_birth",
    "birth_year",
    "age_at_tournament",
    "height_cm",
    "height_verified",
    "height_source",
    "pop_height_birth_cohort",
    "flag",
    "notes",
    "tournament_id",
    "format",
    "tournament_year",
    "era",
    "height_excess",
    "region",
]


# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------

def load_tournament(filepath: Path) -> list[dict]:
    """Load a single tournament JSON and return a flat list of player dicts."""
    with open(filepath, "r", encoding="utf-8") as fh:
        data = json.load(fh)

    tournament = data.get("tournament", {})
    t_id = tournament.get("tournament_id", filepath.stem)
    t_format = tournament.get("format", "")
    t_year = tournament.get("year")
    t_era = tournament.get("era")

    rows = []
    for team in data.get("teams", []):
        nation = team.get("nation", "")
        for player in team.get("playing_xi", []):
            row = {
                "player_id": player.get("player_id"),
                "full_name": player.get("full_name"),
                "country": nation,
                "category": player.get("category"),
                "batting_position": player.get("batting_position"),
                "date_of_birth": player.get("date_of_birth"),
                "birth_year": player.get("birth_year"),
                "age_at_tournament": player.get("age_at_tournament"),
                "height_cm": player.get("height_cm"),
                "height_verified": player.get("height_verified"),
                "height_source": player.get("height_source"),
                "pop_height_birth_cohort": player.get("pop_height_birth_cohort"),
                "flag": player.get("flag"),
                "notes": player.get("notes", ""),
                "tournament_id": t_id,
                "format": t_format,
                "tournament_year": t_year,
                "era": t_era,
            }
            rows.append(row)

    return rows


def main():
    # Ensure output directory exists
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    # Discover JSON files
    json_files = sorted(RAW_DIR.glob("*.json"))
    if not json_files:
        print(f"ERROR: No JSON files found in {RAW_DIR}")
        sys.exit(1)

    print(f"Found {len(json_files)} tournament file(s) in {RAW_DIR}")

    # Load all tournaments
    all_rows: list[dict] = []
    for jf in json_files:
        rows = load_tournament(jf)
        print(f"  {jf.name}: {len(rows)} player-tournament records")
        all_rows.extend(rows)

    if not all_rows:
        print("ERROR: No player records extracted.")
        sys.exit(1)

    df = pd.DataFrame(all_rows)

    # ------------------------------------------------------------------
    # Derived columns
    # ------------------------------------------------------------------

    # height_excess
    df["height_excess"] = np.where(
        df["height_cm"].notna() & df["pop_height_birth_cohort"].notna(),
        df["height_cm"] - df["pop_height_birth_cohort"],
        np.nan,
    )

    # region
    df["region"] = df["country"].map(REGION_MAP).fillna("Unknown")

    # Ensure column order (add any missing columns as NaN)
    for col in OUTPUT_COLUMNS:
        if col not in df.columns:
            df[col] = np.nan
    df = df[OUTPUT_COLUMNS]

    # ------------------------------------------------------------------
    # Save
    # ------------------------------------------------------------------
    csv_path = PROCESSED_DIR / "all_players.csv"
    df.to_csv(csv_path, index=False)
    print(f"\nSaved CSV  : {csv_path}")

    try:
        parquet_path = PROCESSED_DIR / "all_players.parquet"
        df.to_parquet(parquet_path, index=False, engine="pyarrow")
        print(f"Saved Parquet: {parquet_path}")
    except ImportError:
        try:
            parquet_path = PROCESSED_DIR / "all_players.parquet"
            df.to_parquet(parquet_path, index=False, engine="fastparquet")
            print(f"Saved Parquet: {parquet_path}")
        except ImportError:
            print("WARNING: Neither pyarrow nor fastparquet installed; skipping Parquet output.")

    # ------------------------------------------------------------------
    # Summary statistics
    # ------------------------------------------------------------------
    print("\n" + "=" * 72)
    print("MERGE SUMMARY")
    print("=" * 72)
    print(f"Total player-tournament records : {len(df)}")
    print(f"Unique players (by player_id)   : {df['player_id'].nunique()}")
    print(f"Tournaments                     : {df['tournament_id'].nunique()}")
    print(f"Nations                         : {df['country'].nunique()}")
    print(f"Height data available           : {df['height_cm'].notna().sum()} / {len(df)}")
    print(f"Pop height available            : {df['pop_height_birth_cohort'].notna().sum()} / {len(df)}")

    print(f"\n--- Records by category ---")
    print(df["category"].value_counts().to_string())

    print(f"\n--- Records by country ---")
    print(df["country"].value_counts().to_string())

    print(f"\n--- Records by region ---")
    print(df["region"].value_counts().to_string())

    print(f"\n--- Records by format ---")
    print(df["format"].value_counts().to_string())

    print(f"\n--- Records by era ---")
    print(df["era"].value_counts().sort_index().to_string())

    print(f"\n--- Height summary (cm) ---")
    height_stats = df.groupby("category")["height_cm"].describe()
    print(height_stats.to_string())

    if df["height_excess"].notna().any():
        print(f"\n--- Height excess over population (cm) ---")
        excess_stats = df.groupby("category")["height_excess"].describe()
        print(excess_stats.to_string())

    print("\n--- Tournament coverage ---")
    coverage = (
        df.groupby(["tournament_id", "format", "tournament_year"])
        .agg(
            n_teams=("country", "nunique"),
            n_players=("player_id", "count"),
        )
        .reset_index()
        .sort_values("tournament_year")
    )
    print(coverage.to_string(index=False))

    print("\nDone.")


if __name__ == "__main__":
    main()
