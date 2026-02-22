#!/usr/bin/env python3
"""
correct_heights.py - Apply verified height corrections to all raw JSON files.

Based on multi-source verification (ESPN Cricinfo, Wikipedia, ICC, Wisden,
cricket databases) conducted 2026-02-21.

Each correction is documented with sources and confidence level.
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"

# Height corrections: player_id_prefix -> (corrected_height, note)
# player_id_prefix matches the start of player_id across tournament files
CORRECTIONS = {
    # === INDIA ===
    "r-sharma-": (175.0, "Corrected from 177; sources: Wikipedia 174cm, ESPN 175cm, Sportskeeda 175cm (5'9\")"),
    "s-gill-": (178.0, "Corrected from 175; sources: Wikipedia 178cm, ESPN 178cm, multiple cricket sites (5'10\")"),
    "j-bumrah-": (178.0, "Corrected from 175; sources: Wikipedia 178cm, ESPN 178cm, BCCI 178cm (5'10\")"),
    "m-shami-": (173.0, "Corrected from 180; sources: Wikipedia 173cm, ESPN 173cm, all sources unanimous (5'8\")"),

    # === AUSTRALIA ===
    "g-maxwell-": (182.0, "Corrected from 180; sources: Wikipedia 182cm, Sportskeeda 182cm (6'0\")"),
    "m-marsh-1": (193.0, "Corrected from 195; sources: Wikipedia 193cm, SportsYaari 193cm (6'4\")"),
    "t-head-": (179.0, "Corrected from 182; sources: cricket.com.au 179cm, SportsUnfold 179cm (5'10\")"),
    "m-labuschagne-": (180.0, "Corrected from 177; sources: Wikipedia 180cm, CelebsAgeWiki 180cm (5'11\")"),

    # === WEST INDIES ===
    "c-lloyd-": (196.0, "Corrected from 191; sources: Wikipedia 196cm (6'5\"), ESPN 193-196cm"),
    "m-marshall-": (180.0, "Corrected from 175; sources: Wikipedia 180cm, Sportskeeda 180cm (5'11\")"),
    "m-holding-": (192.0, "Corrected from 191; sources: Wikipedia 192cm (6'4\")"),
    "c-walsh-": (198.0, "Corrected from 196; sources: Wikipedia 198cm, Cricket Hall of Fame 198cm (6'6\")"),
    "b-lara-": (173.0, "Corrected from 175 (some entries); sources: Wikipedia 173cm, CelebHeights 173cm (5'8\")"),
    "c-gayle-": (188.0, "Corrected from 191; sources: Wikipedia 188cm, BodySize 188cm (6'2\")"),

    # === PAKISTAN ===
    "s-afridi-1": (180.0, "Corrected from 183; sources: Wikipedia 180cm (5'11\") - Shahid Afridi"),
    "shoaib-akhtar-": (183.0, "Corrected from 185/188; sources: Wikipedia 183cm, BodySize 183cm (6'0\")"),
    "shaheen-": (198.0, "Corrected from 196; sources: Wikipedia 198cm, StarsUnfolded 198cm (6'6\")"),

    # === NEW ZEALAND ===
    "k-williamson-": (173.0, "Corrected from 176/180; sources: Wikipedia 173cm, IPL 173cm (5'8\")"),
    "t-boult-": (180.0, "Corrected from 183; sources: Wikipedia 180cm, StarsUnfolded 180cm (5'11\")"),
    "r-hadlee-": (185.0, "Corrected from 183; sources: Wikipedia 185cm (6'1\")"),

    # === SRI LANKA ===
    "m-muralitharan-": (170.0, "Corrected from 175; sources: Wikipedia 170cm, ESPN 170cm (5'7\")"),
    "l-malinga-": (173.0, "Corrected from 175; sources: Wikipedia 170-173cm, consensus 173cm (5'8\")"),
}

# Special handling: Imran Khan - standardize across tournaments
IMRAN_CORRECTION = (183.0, "Standardized to 183cm; sources: Wikipedia 183cm, StarsUnfolded 183cm (6'0\")")

# Special handling: Shahid Afridi has a different player_id pattern
SHAHID_NAMES = ["Shahid Afridi"]
SHOAIB_NAMES = ["Shoaib Akhtar"]
SHAHEEN_NAMES = ["Shaheen Shah Afridi", "Shaheen Afridi"]


def match_player(player, corrections):
    """Check if a player matches any correction rule."""
    pid = player.get("player_id", "")
    name = player.get("full_name", "")

    # Direct player_id prefix match
    for prefix, (height, note) in corrections.items():
        if pid.startswith(prefix):
            return height, note

    # Name-based matches for tricky IDs
    if name == "Imran Khan":
        return IMRAN_CORRECTION
    if name in SHAHID_NAMES:
        return (180.0, "Corrected from 183; sources: Wikipedia 180cm (5'11\") - Shahid Afridi")
    if name in SHOAIB_NAMES:
        return (183.0, "Corrected from 185/188; sources: Wikipedia 183cm, BodySize 183cm (6'0\")")
    if name in SHAHEEN_NAMES:
        return (198.0, "Corrected from 196; sources: Wikipedia 198cm, StarsUnfolded 198cm (6'6\")")

    return None


def process_file(filepath):
    """Process a single tournament JSON file and apply corrections."""
    with open(filepath, 'r') as f:
        data = json.load(f)

    changes = []
    for team in data.get("teams", []):
        for player in team.get("playing_xi", []):
            result = match_player(player, CORRECTIONS)
            if result:
                new_height, note = result
                old_height = player["height_cm"]
                if abs(old_height - new_height) > 0.1:  # Only change if different
                    player["height_cm"] = new_height
                    # Update verification info
                    if player.get("flag") in [None, "HEIGHT_ESTIMATED"]:
                        player["flag"] = "HEIGHT_CONFLICTING" if abs(old_height - new_height) >= 5 else player.get("flag")
                    old_notes = player.get("notes", "")
                    player["notes"] = f"{old_notes}; VERIFIED: {note}" if old_notes else f"VERIFIED: {note}"
                    player["height_source"] = "multi_source_verified"
                    changes.append({
                        "file": filepath.name,
                        "player": player["full_name"],
                        "nation": team["nation"],
                        "old": old_height,
                        "new": new_height,
                        "delta": new_height - old_height,
                    })

    if changes:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    return changes


def main():
    all_changes = []
    json_files = sorted(RAW_DIR.glob("*.json"))

    print(f"Processing {len(json_files)} tournament files...")
    for fp in json_files:
        changes = process_file(fp)
        all_changes.extend(changes)
        if changes:
            print(f"  {fp.name}: {len(changes)} corrections")
            for c in changes:
                print(f"    {c['player']} ({c['nation']}): {c['old']} -> {c['new']} ({c['delta']:+.0f} cm)")

    print(f"\nTotal corrections applied: {len(all_changes)}")
    print(f"Unique players corrected: {len(set(c['player'] for c in all_changes))}")

    # Summary by direction
    increases = [c for c in all_changes if c['delta'] > 0]
    decreases = [c for c in all_changes if c['delta'] < 0]
    print(f"  Height increases: {len(increases)} (avg {sum(c['delta'] for c in increases)/max(len(increases),1):+.1f} cm)")
    print(f"  Height decreases: {len(decreases)} (avg {sum(c['delta'] for c in decreases)/max(len(decreases),1):+.1f} cm)")
    mean_delta = sum(c['delta'] for c in all_changes) / max(len(all_changes), 1)
    print(f"  Net mean change: {mean_delta:+.2f} cm")

    # Save correction log
    log_path = BASE_DIR / "data" / "processed" / "height_corrections_log.json"
    with open(log_path, 'w') as f:
        json.dump(all_changes, f, indent=2)
    print(f"\nCorrection log saved to: {log_path}")


if __name__ == "__main__":
    main()
