# Cornell Club Recommender

An adaptive quiz + explainable content-based club recommender.

## Run

```bash
cd club_recommender
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

Then open `http://127.0.0.1:8000` in a browser.

For the API docs:
`http://127.0.0.1:8000/docs`

## Data

The recommender loads the supplied club database from `data/`:

```text
data/UPDATED_cornell_clubs_rich_dataset.xlsx - Clubs.csv
```

The recommender supports the fields from the club schema discussed in the project:

- category
- subcategory
- summary
- description
- typical_meeting
- interest_tags
- skills_gained
- vibe_tags
- vibe_social
- vibe_competitive
- vibe_creative
- vibe_relaxed
- vibe_physical
- vibe_intellectual
- vibe_performance
- vibe_service
- commitment_level
- hours_per_week_min
- hours_per_week_max
- beginner_friendly
- audition_required
- application_required
- meeting_days
- and related metadata

If that CSV is missing, the app falls back to a small demo dataset.

## Architecture

1. `quiz.py` defines the adaptive question graph.
2. `profile.py` converts answers into a normalized user profile.
3. `recommender.py` scores every club.
4. Hard constraints remove clearly incompatible clubs.
5. Results include explanations for why each club matched.

The quiz and recommender are intentionally separate so the question flow can change without rewriting the ranking algorithm.
