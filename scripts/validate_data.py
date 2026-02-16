#!/usr/bin/env python3
"""
validate_data.py - Validate raw tournament JSON files for the cricket
anthropometric research project.

Checks performed:
  - Schema compliance (all required fields present)
  - Category values are valid (WK / BAT / FAST / SPIN)
  - Exactly 1 WK per team
  - Exactly 11 players per team
  - Heights are reasonable (150-220 cm)
  - DOBs are reasonable (player 15-45 years old at tournament)
  - No duplicate player_ids within a tournament
  - Flag values are valid

Usage:
    python scripts/validate_data.py data/raw/*.json
    python scripts/validate_data.py data/raw/*.json --strict

Exit code 0 if all files pass, 1 if any errors found.
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

VALID_CATEGORIES = {"WK", "BAT", "FAST", "SPIN"}
VALID_FLAGS = {
    None,
    "HEIGHT_ESTIMATED",
    "HEIGHT_CONFLICTING",
    "DOB_ESTIMATED",
    "DOB_UNKNOWN",
    "CATEGORY_AMBIGUOUS",
    "LIMITED_APPEARANCES",
    "CAPTAIN",  # present in actual data
}
VALID_FORMATS = {"ODI", "T20"}
VALID_NATIONS = {"AUS", "ENG", "IND", "PAK", "WI", "NZL", "SL", "RSA"}
REQUIRED_TOURNAMENT_FIELDS = {"tournament_id", "format", "year", "host", "winner", "era"}
REQUIRED_PLAYER_FIELDS = {
    "player_id",
    "full_name",
    "category",
    "batting_position",
    "date_of_birth",
    "birth_year",
    "age_at_tournament",
    "height_cm",
    "height_verified",
    "height_source",
    "flag",
    "notes",
}
# pop_height_birth_cohort is optional -- may be filled later by match_population.py

HEIGHT_MIN = 150.0
HEIGHT_MAX = 220.0
AGE_MIN = 15
AGE_MAX = 45


# ---------------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------------

class ValidationResult:
    """Accumulates errors and warnings for a single file."""

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, msg: str):
        self.errors.append(msg)

    def warn(self, msg: str):
        self.warnings.append(msg)

    @property
    def passed(self) -> bool:
        return len(self.errors) == 0

    def summary_line(self) -> str:
        status = "PASS" if self.passed else "FAIL"
        parts = [f"[{status}] {self.filepath}"]
        if self.errors:
            parts.append(f"  {len(self.errors)} error(s)")
        if self.warnings:
            parts.append(f"  {len(self.warnings)} warning(s)")
        return " | ".join(parts)


def validate_file(filepath: str, strict: bool = False) -> ValidationResult:
    """Validate a single tournament JSON file and return results."""

    result = ValidationResult(filepath)

    # ------------------------------------------------------------------
    # 1. Load JSON
    # ------------------------------------------------------------------
    try:
        with open(filepath, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except json.JSONDecodeError as exc:
        result.error(f"Invalid JSON: {exc}")
        return result
    except FileNotFoundError:
        result.error("File not found")
        return result

    # ------------------------------------------------------------------
    # 2. Top-level structure
    # ------------------------------------------------------------------
    if "tournament" not in data:
        result.error("Missing top-level key 'tournament'")
        return result
    if "teams" not in data:
        result.error("Missing top-level key 'teams'")
        return result

    tournament = data["tournament"]

    # Tournament fields
    missing_t = REQUIRED_TOURNAMENT_FIELDS - set(tournament.keys())
    if missing_t:
        result.error(f"Tournament missing fields: {missing_t}")

    tournament_year = tournament.get("year")
    tournament_id = tournament.get("tournament_id", "<unknown>")
    fmt = tournament.get("format")

    if fmt and fmt not in VALID_FORMATS:
        result.error(f"Invalid format '{fmt}'; expected one of {VALID_FORMATS}")

    if tournament_year is not None and not isinstance(tournament_year, int):
        result.error(f"Tournament year must be int, got {type(tournament_year).__name__}")

    # Era validation
    era = tournament.get("era")
    if era is not None and tournament_year is not None:
        expected_era = None
        if 1975 <= tournament_year <= 1987:
            expected_era = 1
        elif 1992 <= tournament_year <= 1999:
            expected_era = 2
        elif 2003 <= tournament_year <= 2012:
            expected_era = 3
        elif 2014 <= tournament_year <= 2026:
            expected_era = 4
        if expected_era is not None and era != expected_era:
            result.warn(
                f"Era mismatch: tournament year {tournament_year} suggests era "
                f"{expected_era}, but era={era}"
            )

    # ------------------------------------------------------------------
    # 3. Teams
    # ------------------------------------------------------------------
    teams = data["teams"]
    if not isinstance(teams, list):
        result.error("'teams' must be a list")
        return result

    if len(teams) == 0:
        result.error("No teams in file")
        return result

    all_player_ids: list[str] = []

    for team_idx, team in enumerate(teams):
        nation = team.get("nation", f"<team-{team_idx}>")

        # Validate nation code
        if nation not in VALID_NATIONS:
            if strict:
                result.error(f"Team '{nation}' is not a valid nation code")
            else:
                result.warn(f"Team '{nation}' is not in the standard 8-nation set")

        playing_xi = team.get("playing_xi")
        if playing_xi is None:
            result.error(f"[{nation}] Missing 'playing_xi'")
            continue
        if not isinstance(playing_xi, list):
            result.error(f"[{nation}] 'playing_xi' must be a list")
            continue

        # ---- 11 players ----
        if len(playing_xi) != 11:
            result.error(
                f"[{nation}] Expected 11 players, found {len(playing_xi)}"
            )

        # Counters
        wk_count = 0
        team_player_ids: list[str] = []

        for p_idx, player in enumerate(playing_xi):
            pid = player.get("player_id", f"<player-{p_idx}>")
            label = f"[{nation}/{pid}]"

            # ---- Required fields ----
            missing_p = REQUIRED_PLAYER_FIELDS - set(player.keys())
            if missing_p:
                result.error(f"{label} Missing fields: {missing_p}")

            # ---- Category ----
            cat = player.get("category")
            if cat not in VALID_CATEGORIES:
                result.error(f"{label} Invalid category '{cat}'")
            if cat == "WK":
                wk_count += 1

            # ---- Height ----
            height = player.get("height_cm")
            if height is not None:
                if not isinstance(height, (int, float)):
                    result.error(f"{label} height_cm must be numeric, got {type(height).__name__}")
                elif height < HEIGHT_MIN or height > HEIGHT_MAX:
                    result.error(
                        f"{label} height_cm={height} out of range "
                        f"[{HEIGHT_MIN}, {HEIGHT_MAX}]"
                    )
            else:
                result.warn(f"{label} height_cm is null/missing")

            # ---- DOB / age ----
            birth_year = player.get("birth_year")
            age = player.get("age_at_tournament")
            dob = player.get("date_of_birth")

            if birth_year is not None and tournament_year is not None:
                approx_age = tournament_year - birth_year
                if approx_age < AGE_MIN or approx_age > AGE_MAX:
                    result.error(
                        f"{label} Approximate age {approx_age} out of "
                        f"range [{AGE_MIN}, {AGE_MAX}]"
                    )

            if dob is not None and dob != "":
                try:
                    datetime.strptime(str(dob), "%Y-%m-%d")
                except ValueError:
                    result.error(f"{label} date_of_birth '{dob}' is not YYYY-MM-DD")

            # ---- Flag ----
            flag = player.get("flag")
            if flag not in VALID_FLAGS:
                if strict:
                    result.error(f"{label} Invalid flag '{flag}'")
                else:
                    result.warn(f"{label} Non-standard flag '{flag}'")

            # ---- Batting position ----
            bp = player.get("batting_position")
            if bp is not None:
                if not isinstance(bp, int) or bp < 1 or bp > 11:
                    result.error(f"{label} batting_position={bp} must be int in [1,11]")

            # ---- height_verified type ----
            hv = player.get("height_verified")
            if hv is not None and not isinstance(hv, bool):
                result.warn(f"{label} height_verified should be bool, got {type(hv).__name__}")

            # ---- Collect player_id for duplicate check ----
            if pid:
                team_player_ids.append(pid)
                all_player_ids.append(pid)

        # ---- Exactly 1 WK per team ----
        if wk_count != 1:
            result.error(
                f"[{nation}] Expected exactly 1 WK, found {wk_count}"
            )

        # ---- Duplicate player_ids within team ----
        seen = set()
        for pid in team_player_ids:
            if pid in seen:
                result.error(f"[{nation}] Duplicate player_id '{pid}'")
            seen.add(pid)

    # ------------------------------------------------------------------
    # 4. Duplicate player_ids across teams (within tournament)
    # ------------------------------------------------------------------
    seen_all = set()
    for pid in all_player_ids:
        if pid in seen_all:
            result.warn(f"Duplicate player_id '{pid}' across teams in tournament")
        seen_all.add(pid)

    return result


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Validate raw tournament JSON files for cricket anthropometric research."
    )
    parser.add_argument(
        "files",
        nargs="+",
        help="Path(s) to tournament JSON files (supports glob).",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        default=False,
        help="Treat warnings as errors (stricter validation).",
    )
    args = parser.parse_args()

    # Resolve file paths (glob may already be expanded by shell)
    filepaths: list[str] = []
    for f in args.files:
        p = Path(f)
        if p.is_file():
            filepaths.append(str(p))
        elif "*" in f or "?" in f:
            matches = sorted(Path(".").glob(f))
            filepaths.extend(str(m) for m in matches if m.is_file())
        else:
            print(f"WARNING: '{f}' is not a file and not a glob pattern; skipping.")

    if not filepaths:
        print("ERROR: No files to validate.")
        sys.exit(1)

    # Run validation
    results: list[ValidationResult] = []
    for fp in filepaths:
        res = validate_file(fp, strict=args.strict)
        results.append(res)

    # --------------- Print results ---------------
    print("=" * 72)
    print("CRICKET DATA VALIDATION REPORT")
    print("=" * 72)
    print(f"Files checked : {len(results)}")
    print(f"Mode          : {'STRICT' if args.strict else 'NORMAL'}")
    print("-" * 72)

    total_errors = 0
    total_warnings = 0

    for res in results:
        total_errors += len(res.errors)
        total_warnings += len(res.warnings)

        print(f"\n{res.summary_line()}")
        for e in res.errors:
            print(f"    ERROR: {e}")
        for w in res.warnings:
            print(f"    WARN : {w}")

    print("\n" + "=" * 72)
    passed = sum(1 for r in results if r.passed)
    failed = len(results) - passed
    print(f"SUMMARY: {passed} passed, {failed} failed")
    print(f"         {total_errors} error(s), {total_warnings} warning(s)")
    print("=" * 72)

    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
