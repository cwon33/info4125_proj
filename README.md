# Cornell Club Recommender

An adaptive quiz and explainable content based recommender for Cornell clubs.

## Run locally

Run these commands from this directory:

```bash
pip install -r requirements.txt
cd club_recommender
uvicorn backend.main:app --reload
```

Open <http://127.0.0.1:8000> for the quiz or <http://127.0.0.1:8000/docs> for the API documentation (not required to open).

The CSV at `data/UPDATED_cornell_clubs_rich_dataset.xlsx - Clubs.csv` is required. The server reads it at startup and exits with a file error if its missing. Keep this file where it is currently when running the app.

## How it works

1. `backend/quiz.py` defines questions and chooses follow-up questions based on selected categories.
2. `backend/profile.py` translates answer IDs to the category and subcategory labels used by the club data.
3. `backend/recommender.py` filters incompatible clubs, scores interests, vibe, logistics, and time commitment, then adds match explanations.
4. `backend/main.py` loads the CSV, provides the API routes, and serves `frontend/index.html`.


See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for the data schema and also end-to-end workflow walkthrough.

## Project files

- `backend/main.py`: FastAPI entry point and API routes.
- `backend/quiz.py`: quiz question catalog and adaptive flow.
- `backend/profile.py`: answer-to-profile conversion.
- `backend/recommender.py`: eligibility filters, ranking, and explanations.
- `backend/__init__.py`: marks the backend as an importable Python package.
- `frontend/index.html`: browser UI served by the API.
- `data/UPDATED_cornell_clubs_rich_dataset.xlsx - Clubs.csv`: required source club database.
- `requirements.txt`: Python dependencies.
