#!/usr/bin/env python3
"""
match_population.py - Match cricket players to population height norms.

Reads:
  - data/external/population_heights.csv   (country_code, birth_year, mean_height_cm)
  - data/processed/all_players.csv         (merged player data)

For any player whose pop_height_birth_cohort is missing (NaN), looks up the
population mean height using country + birth_year from the external CSV.

Updates and saves:
  - data/processed/all_players.csv
  - data/processed/all_players.parquet  (if pyarrow/fastparquet available)

Also recomputes height_excess = height_cm - pop_height_birth_cohort.

Usage:
    python scripts/match_population.py
"""

import sys
from pathlib import Path

import pandas as pd
import numpy as np

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
POPULATION_CSV = BASE_DIR / "data" / "external" / "population_heights.csv"
MERGED_CSV = BASE_DIR / "data" / "processed" / "all_players.csv"
PROCESSED_DIR = BASE_DIR / "data" / "processed"


def main():
    # ------------------------------------------------------------------
    # 1. Load population data
    # ------------------------------------------------------------------
    if not POPULATION_CSV.exists():
        print(f"ERROR: Population heights file not found: {POPULATION_CSV}")
        sys.exit(1)

    pop = pd.read_csv(POPULATION_CSV)
    print(f"Loaded population heights: {len(pop)} rows")
    print(f"  Countries: {sorted(pop['country_code'].unique())}")
    print(f"  Birth years: {pop['birth_year'].min()} - {pop['birth_year'].max()}")

    # Build lookup dictionary: (country_code, birth_year) -> mean_height_cm
    pop_lookup = {}
    for _, row in pop.iterrows():
        key = (row["country_code"], int(row["birth_year"]))
        pop_lookup[key] = float(row["mean_height_cm"])

    # ------------------------------------------------------------------
    # 2. Load merged player data
    # ------------------------------------------------------------------
    if not MERGED_CSV.exists():
        print(f"ERROR: Merged player file not found: {MERGED_CSV}")
        print("       Run merge_all_tournaments.py first.")
        sys.exit(1)

    df = pd.read_csv(MERGED_CSV)
    print(f"\nLoaded merged data: {len(df)} player-tournament records")

    initial_missing = df["pop_height_birth_cohort"].isna().sum()
    print(f"Records missing pop_height_birth_cohort: {initial_missing}")

    if initial_missing == 0:
        print("All records already have population height data. Nothing to update.")
        return

    # ------------------------------------------------------------------
    # 3. Fill missing population heights
    # ------------------------------------------------------------------
    filled_count = 0
    not_found_keys = set()

    for idx, row in df.iterrows():
        if pd.isna(row["pop_height_birth_cohort"]):
            country = row.get("country", "")
            by = row.get("birth_year")

            if pd.isna(by):
                continue

            by = int(by)
            key = (country, by)

            if key in pop_lookup:
                df.at[idx, "pop_height_birth_cohort"] = pop_lookup[key]
                filled_count += 1
            else:
                not_found_keys.add(key)
                # Try interpolation: find nearest available birth year
                country_years = {
                    yr: ht for (cc, yr), ht in pop_lookup.items() if cc == country
                }
                if country_years:
                    nearest_year = min(country_years.keys(), key=lambda y: abs(y - by))
                    df.at[idx, "pop_height_birth_cohort"] = country_years[nearest_year]
                    filled_count += 1

    print(f"\nFilled {filled_count} missing population height values")

    if not_found_keys:
        print(f"Could not find exact match for {len(not_found_keys)} (country, birth_year) keys:")
        for k in sorted(not_found_keys)[:20]:
            print(f"    {k}")
        if len(not_found_keys) > 20:
            print(f"    ... and {len(not_found_keys) - 20} more")

    # ------------------------------------------------------------------
    # 4. Recompute height_excess
    # ------------------------------------------------------------------
    df["height_excess"] = np.where(
        df["height_cm"].notna() & df["pop_height_birth_cohort"].notna(),
        df["height_cm"] - df["pop_height_birth_cohort"],
        np.nan,
    )

    # ------------------------------------------------------------------
    # 5. Save updated data
    # ------------------------------------------------------------------
    csv_path = PROCESSED_DIR / "all_players.csv"
    df.to_csv(csv_path, index=False)
    print(f"\nSaved updated CSV: {csv_path}")

    try:
        parquet_path = PROCESSED_DIR / "all_players.parquet"
        df.to_parquet(parquet_path, index=False, engine="pyarrow")
        print(f"Saved updated Parquet: {parquet_path}")
    except ImportError:
        try:
            parquet_path = PROCESSED_DIR / "all_players.parquet"
            df.to_parquet(parquet_path, index=False, engine="fastparquet")
            print(f"Saved updated Parquet: {parquet_path}")
        except ImportError:
            print("WARNING: No Parquet engine available; skipping Parquet output.")

    # ------------------------------------------------------------------
    # 6. Summary
    # ------------------------------------------------------------------
    remaining_missing = df["pop_height_birth_cohort"].isna().sum()
    print(f"\n{'=' * 60}")
    print("POPULATION MATCHING SUMMARY")
    print(f"{'=' * 60}")
    print(f"Total records             : {len(df)}")
    print(f"Initially missing         : {initial_missing}")
    print(f"Successfully filled       : {filled_count}")
    print(f"Still missing             : {remaining_missing}")
    print(f"Height excess computable  : {df['height_excess'].notna().sum()}")

    if df["height_excess"].notna().any():
        print(f"\n--- Height excess by category (cm) ---")
        excess = df.groupby("category")["height_excess"].agg(["mean", "std", "count"])
        print(excess.to_string())

        print(f"\n--- Height excess by country (cm) ---")
        excess_c = df.groupby("country")["height_excess"].agg(["mean", "std", "count"])
        print(excess_c.to_string())

    print("\nDone.")


if __name__ == "__main__":
    main()
