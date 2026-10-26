
"""FastAPI application: load club data, serve the quiz, and return recommendations."""

from pathlib import Path
from typing import Any
import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles


from .quiz import get_question, next_questions
from .profile import profile_from_answers
from .recommender import recommend, SCORE_WEIGHTS

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "UPDATED_cornell_clubs_rich_dataset.xlsx - Clubs.csv"

def load_clubs():
    # Read the required club CSV. startup fails if it is missing or invalid.
    return pd.read_csv(DATA).fillna("")

CLUBS = load_clubs()

app = FastAPI(title="Cornell Club Recommender API", version="1.0.0")
app.mount("/assets", StaticFiles(directory=ROOT / "frontend"), name="assets")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", include_in_schema=False)
def frontend():
    # Serve the single-page quiz UI from the project frontend directory.
    return FileResponse(ROOT / "frontend" / "index.html")

class AnswersRequest(BaseModel):
    # Shared request shape for quiz progression and recommendation endpoints.
    answers: dict[str, Any] = Field(default_factory=dict)
    top_n: int = 10

@app.get("/quiz/start")
def quiz_start():
    # Return the first question, which asks users to choose club categories.
    return {"question": get_question("categories")}

@app.post("/quiz/next")
def quiz_next(req: AnswersRequest):
    # Choose the next unanswered question based on selected categories.
    ids = next_questions(req.answers)
    answered = set(req.answers.keys())
    next_id = next((x for x in ids if x not in answered), None)
    return {"question": get_question(next_id) if next_id else None, "remaining": [x for x in ids if x not in answered]}

@app.post("/recommend")
def get_recommendations(req: AnswersRequest):
    # Convert submitted answers to a profile and rank compatible clubs.
    answers_for_log = dict(req.answers)
    if "free_text" in answers_for_log:
        free_text = str(answers_for_log["free_text"])
        answers_for_log["free_text"] = f"<redacted; {len(free_text)} characters>"
    print("\n=== Quiz recommendation debug ===")
    print(f"Submitted answers: {answers_for_log}")

    profile = profile_from_answers(req.answers)
    print("Normalized profile:")
    for name, value in profile.items():
        if name != "free_text":
            print(f"  {name}: {value}")
    print(
        "Score formula: "
        + " + ".join(f"{weight:.2f} * {name}" for name, weight in SCORE_WEIGHTS.items())
    )

    results = recommend(profile, CLUBS, max(1, min(req.top_n, 50)))
    print(f"Final ranked recommendations (top {len(results)}):")
    for rank, result in enumerate(results, start=1):
        print(
            f"  {rank}. {result['club_name']}: "
            f"score={result['score']:.4f} ({result['match_percent']:.1f}%), "
            f"reasons={result['reasons']}"
        )
    print("=== End recommendation debug ===\n")
    return {"profile": profile, "recommendations": results}

@app.get("/clubs")
def clubs():
    # Expose the loaded source rows for API clients and inspection.
    return CLUBS.fillna("").to_dict(orient="records")

@app.get("/health")
def health():
    # Report service status and number of clubs loaded from the required CSV.
    return {"status": "ok", "clubs_loaded": len(CLUBS), "source": str(DATA)}
