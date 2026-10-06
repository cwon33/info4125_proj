
from pathlib import Path
from typing import Any
import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from fastapi.responses import FileResponse

from .quiz import get_question, next_questions, QUESTIONS
from .profile import profile_from_answers
from .recommender import recommend

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "UPDATED_cornell_clubs_rich_dataset.xlsx - Clubs.csv"

DEMO = pd.DataFrame([
    {"club_id":"demo1","club_name":"Cornell Robotics Club","category":"Tech & Making","subcategory":"Gadgets & Computing","summary":"Build robots and work on hands-on engineering projects.","interest_tags":"robotics,engineering,computing","skills_gained":"programming,hardware","vibe_social":0.7,"vibe_competitive":0.8,"vibe_creative":0.7,"vibe_relaxed":0.2,"vibe_physical":0.5,"vibe_intellectual":0.9,"vibe_performance":0.1,"vibe_service":0.2,"beginner_friendly":True,"hours_per_week_min":2,"hours_per_week_max":6,"size_bucket":"large","meeting_days":"tuesday,thursday"},
    {"club_id":"demo2","club_name":"Cornell Hiking Club","category":"Outdoors, Nature & Animals","subcategory":"Hiking & Camping","summary":"Explore Ithaca and the surrounding area through hikes and outdoor trips.","interest_tags":"hiking,nature,outdoors","skills_gained":"navigation,outdoor skills","vibe_social":0.9,"vibe_competitive":0.2,"vibe_creative":0.2,"vibe_relaxed":0.8,"vibe_physical":0.9,"vibe_intellectual":0.3,"vibe_performance":0.0,"vibe_service":0.2,"beginner_friendly":True,"hours_per_week_min":2,"hours_per_week_max":4,"size_bucket":"large","meeting_days":"saturday,sunday"},
    {"club_id":"demo3","club_name":"Cornell Improv","category":"Theatre, Comedy & Storytelling","subcategory":"Improv & Sketch Comedy","summary":"Practice improv, perform, and meet people through comedy.","interest_tags":"improv,comedy,performance,theatre","skills_gained":"public speaking,performance","vibe_social":0.9,"vibe_competitive":0.3,"vibe_creative":1.0,"vibe_relaxed":0.5,"vibe_physical":0.3,"vibe_intellectual":0.6,"vibe_performance":1.0,"vibe_service":0.1,"beginner_friendly":True,"hours_per_week_min":2,"hours_per_week_max":5,"size_bucket":"medium","meeting_days":"monday,wednesday"},
    {"club_id":"demo4","club_name":"Cornell Food Club","category":"Food & Drink","subcategory":"Baking & Cooking","summary":"Cook, bake, share food, and explore food culture with other students.","interest_tags":"cooking,baking,food,social","skills_gained":"cooking,food","vibe_social":0.9,"vibe_competitive":0.1,"vibe_creative":0.7,"vibe_relaxed":0.8,"vibe_physical":0.1,"vibe_intellectual":0.4,"vibe_performance":0.0,"vibe_service":0.2,"beginner_friendly":True,"hours_per_week_min":1,"hours_per_week_max":3,"size_bucket":"medium","meeting_days":"friday,saturday"},
    {"club_id":"demo5","club_name":"Cornell Service Collective","category":"Service & Volunteering","subcategory":"Youth & Education Service","summary":"Volunteer with local community organizations and education programs.","interest_tags":"service,volunteering,education,community","skills_gained":"leadership,service","vibe_social":0.8,"vibe_competitive":0.1,"vibe_creative":0.4,"vibe_relaxed":0.5,"vibe_physical":0.2,"vibe_intellectual":0.5,"vibe_performance":0.1,"vibe_service":1.0,"beginner_friendly":True,"hours_per_week_min":1,"hours_per_week_max":4,"size_bucket":"large","meeting_days":"wednesday,saturday"},
])

def load_clubs():
    if DATA.exists():
        return pd.read_csv(DATA).fillna("")
    return DEMO

CLUBS = load_clubs()

app = FastAPI(title="Cornell Club Recommender API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", include_in_schema=False)
def frontend():
    return FileResponse(ROOT / "frontend" / "index.html")

class AnswersRequest(BaseModel):
    answers: dict[str, Any] = Field(default_factory=dict)
    top_n: int = 10

@app.get("/quiz/start")
def quiz_start():
    return {"question": get_question("categories")}

@app.post("/quiz/next")
def quiz_next(req: AnswersRequest):
    ids = next_questions(req.answers)
    answered = set(req.answers.keys())
    next_id = next((x for x in ids if x not in answered), None)
    return {"question": get_question(next_id) if next_id else None, "remaining": [x for x in ids if x not in answered]}

@app.post("/recommend")
def get_recommendations(req: AnswersRequest):
    profile = profile_from_answers(req.answers)
    results = recommend(profile, CLUBS, max(1, min(req.top_n, 50)))
    return {"profile": profile, "recommendations": results}

@app.get("/clubs")
def clubs():
    return CLUBS.fillna("").to_dict(orient="records")

@app.get("/health")
def health():
    return {"status": "ok", "clubs_loaded": len(CLUBS), "source": str(DATA) if DATA.exists() else "demo"}
