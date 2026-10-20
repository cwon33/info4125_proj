"""Content-based scoring, hard filters, and human-readable match explanations."""

import re
from typing import Any
import pandas as pd

VIBES = ["social", "competitive", "creative", "relaxed", "physical", "intellectual", "performance", "service"]
SCORE_WEIGHTS = {
    "interest": 0.40,
    "vibe": 0.30,
    "logistics": 0.15,
    "commitment": 0.15,
}

def split_values(x: Any) -> set[str]:
    # Split list-like CSV fields into normalized tokens.
    if x is None or (isinstance(x, float) and pd.isna(x)):
        return set()
    return {v.strip().lower() for v in re.split(r"[,;|]", str(x)) if v.strip()}

def truthy(x: Any) -> bool:
    # Interpret common CSV representations of true as a boolean.
    return str(x).strip().lower() in {"true", "1", "yes", "y"}

def num(x: Any, default=0.0) -> float:
    # Convert a value to float, returning a safe default for bad/missing data.
    try:
        return float(x)
    except Exception:
        return default

def club_text(row: pd.Series) -> str:
    # Combine descriptive fields for simple interest substring matching.
    fields = ["club_name", "category", "subcategory", "summary", "description",
              "interest_tags", "skills_gained", "good_for", "match_text", "vibe_tags"]
    return " ".join(str(row.get(f, "")) for f in fields).lower()

def interest_score(profile: dict, row: pd.Series) -> float:
    # Score how many selected interests appear in the club's descriptive text.
    interests = [x.lower() for x in profile["interests"]]
    if not interests:
        return 0.0
    text = club_text(row)
    hits = sum(1 for i in interests if i in text)
    return min(1.0, hits / max(1, min(len(interests), 4)))

def vibe_score(profile: dict, row: pd.Series) -> float:
    # Compare requested vibe dimensions with numeric values or fallback tags.
    requested = profile["vibe"]
    if not requested:
        return 0.0
    vals = {v: num(row.get("vibe_" + v, 0)) for v in VIBES}
    if all(v == 0 for v in vals.values()):
        tags = split_values(row.get("vibe_tags"))
        return sum(1 for v in requested if v in tags) / len(requested)
    return sum(min(1, vals.get(v, 0)) for v in requested) / len(requested)

def logistics_score(profile: dict, row: pd.Series) -> float:
    # Score selected meeting days and preferred club size.
    score = 0.0
    checks = 0
    if profile["days"]:
        checks += 1
        club_days = split_values(row.get("meeting_days"))
        score += 1.0 if not club_days or any(d.lower() in club_days for d in profile["days"]) else 0.0
    if profile["size"] and profile["size"] != "any":
        checks += 1
        score += 1.0 if str(row.get("size_bucket", "")).lower() == profile["size"] else 0.0
    return score / checks if checks else 0.5

def commitment_score(profile: dict, row: pd.Series) -> float:
    # Give full credit when weekly time ranges overlap.
    low, high = profile["time_range"]
    club_low = num(row.get("hours_per_week_min"), 0)
    club_high = num(row.get("hours_per_week_max"), club_low)
    if club_low <= high and club_high >= low:
        return 1.0
    return 0.0

def hard_filter(profile: dict, row: pd.Series) -> bool:
    # Exclude clubs outside chosen categories or hard eligibility preferences.
    selected_categories = {
        str(category).strip().casefold()
        for category in profile.get("categories", [])
    }
    club_category = str(row.get("category", "")).strip().casefold()
    if selected_categories and club_category not in selected_categories:
        return False

    selected_subcategories = profile.get("category_subcategories", {}).get(
        row.get("category", ""), []
    )
    club_subcategory = str(row.get("subcategory", "")).strip().casefold()
    if selected_subcategories and club_subcategory not in {
        str(subcategory).strip().casefold()
        for subcategory in selected_subcategories
    }:
        return False

    req = profile["requirements"]
    if req == "avoid" and (truthy(row.get("audition_required")) or truthy(row.get("application_required"))):
        return False

    beginner = profile["beginner"]
    if beginner == "very" and str(row.get("beginner_friendly", "")).lower() in {"false", "no", "0"}:
        return False

    return True

def explanations(profile: dict, row: pd.Series, parts: dict) -> list[str]:
    # Turn strong score components and goals into concise match reasons.
    reasons = []
    if parts["interest"] >= 0.5:
        reasons.append("matches your interests")
    if parts["vibe"] >= 0.7:
        reasons.append("fits your preferred vibe")
    if parts["logistics"] >= 0.8:
        reasons.append("fits your availability/preferences")
    if parts["commitment"] >= 0.8:
        reasons.append("fits your preferred time commitment")
    if profile["beginner"] == "very" and truthy(row.get("beginner_friendly")):
        reasons.append("beginner-friendly")
    if profile["goals"].get("meet_people") and num(row.get("vibe_social")) >= 0.7:
        reasons.append("good for meeting people")
    if profile["goals"].get("active") and num(row.get("vibe_physical")) >= 0.7:
        reasons.append("active/physical")
    if profile["goals"].get("give_back") and num(row.get("vibe_service")) >= 0.7:
        reasons.append("service-oriented")
    return reasons[:4] or ["broad match with your preferences"]

def recommend(profile: dict, df: pd.DataFrame, top_n: int = 10) -> list[dict]:
    # Score eligible clubs, balance selected categories, and return top results.
    results = []
    for _, row in df.iterrows():
        if not hard_filter(profile, row):
            continue

        parts = {
            "interest": interest_score(profile, row),
            "vibe": vibe_score(profile, row),
            "logistics": logistics_score(profile, row),
            "commitment": commitment_score(profile, row),
        }

        contributions = {
            name: value * SCORE_WEIGHTS[name]
            for name, value in parts.items()
        }
        score = sum(contributions.values())

        breakdown = " ".join(
            f"{name}={parts[name]:.3f} x {SCORE_WEIGHTS[name]:.2f}"
            f" = {contributions[name]:.3f}"
            for name in SCORE_WEIGHTS
        )
        print(
            f"[recommendation score] {row.get('club_name', '')}: "
            f"{breakdown}; final={score:.4f} ({score * 100:.1f}%)"
        )

        results.append({
            "club_id": str(row.get("club_id", "")),
            "club_name": str(row.get("club_name", "")),
            "category": str(row.get("category", "")),
            "subcategory": str(row.get("subcategory", "")),
            "summary": str(row.get("summary", "")),
            "score": round(float(score), 4),
            "match_percent": round(float(score) * 100, 1),
            "reasons": explanations(profile, row, parts),
        })

    results.sort(key=lambda x: x["score"], reverse=True)

    selected_categories = profile.get("categories", [])
    if not selected_categories:
        return results[:top_n]

    category_results = {}
    for result in results:
        category = str(result["category"]).strip().casefold()
        category_results.setdefault(category, []).append(result)

    balanced_results = []
    normalized_categories = [
        str(category).strip().casefold() for category in selected_categories
    ]
    while len(balanced_results) < top_n:
        added_result = False
        for category in normalized_categories:
            available = category_results.get(category, [])
            if available:
                balanced_results.append(available.pop(0))
                added_result = True
                if len(balanced_results) == top_n:
                    break
        if not added_result:
            break

    return balanced_results
