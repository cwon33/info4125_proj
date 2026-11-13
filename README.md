# Cornell Club Recommender

ClubQuest is an adaptive quiz and explainable content-based recommender that helps Cornell students discover clubs based on their interests, preferred experience, availability, and time commitment.

[Visit the deployed ClubQuest site](https://cornell-clubquest.onrender.com/)

## Features

- An adaptive quiz that asks follow-up questions for the selected club categories.
- Personalized club recommendations with match scores and explanations.
- A searchable club directory with category and beginner-friendly filters.
- Club detail panels with meeting, membership, and dues information from the dataset.
- Saved clubs stored in the current browser, with no account required.
- A responsive Cornell-inspired frontend built with HTML, CSS, and JavaScript.

## Run locally

Use Python 3.11 or 3.12. The commands below are for macOS/Linux and must be run from the **repository root**, the directory containing this README and `club_recommender/`.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r club_recommender/requirements.txt
.venv/bin/python -m uvicorn backend.main:app --app-dir club_recommender --reload
```

On Windows PowerShell, use:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r club_recommender/requirements.txt
.\.venv\Scripts\python.exe -m uvicorn backend.main:app --app-dir club_recommender --reload
```

Open [the local app](http://127.0.0.1:8000) or [the optional API documentation](http://127.0.0.1:8000/docs). Keep the server running while using the app; press `Ctrl+C` to stop it.

Each contributor creates their own `.venv`. Commit dependency files and setup instructions, but do not commit the virtual environment or installed packages.

## Run the integration tests

From the **repository root**, install the test dependencies and run the suite:

```bash
.venv/bin/python -m pip install -r club_recommender/requirements-dev.txt
.venv/bin/python -m unittest discover -s club_recommender/tests -v
```

On Windows, replace `.venv/bin/python` with `.\.venv\Scripts\python.exe` in both commands. `requirements-dev.txt` includes the application dependencies plus the HTTP client used by FastAPI's test client. Python's `unittest` is included with Python.

The suite in [test_integration.py](club_recommender/tests/test_integration.py) contains three integration tests:

1. **App and dataset loading:** checks that the homepage, JavaScript, and CSS are served successfully, the dataset is nonempty, the reported club count matches the dataset, and club IDs are unique.
2. **Adaptive quiz flow:** checks that changing selected categories changes the next and remaining questions.
3. **Completed quiz and recommendations:** submits sample answers and checks that the quiz is complete, returned clubs exist in the dataset and selected category/subcategory, scores are between 0 and 100, and explanations are present. It also checks that the sample private note and the old `Normalized profile` debug heading are not printed.

These tests use an in-process version of the app and its local dataset; you do not need to start Uvicorn or access the deployed site. They do not automate browser interactions or measure how useful recommendations are to real students.

## How it works

1. [quiz.py](club_recommender/backend/quiz.py) defines questions and selects category-specific follow-ups.
2. [profile.py](club_recommender/backend/profile.py) translates answer IDs into dataset categories, subcategories, interests, and preferences.
3. [recommender.py](club_recommender/backend/recommender.py) filters incompatible clubs, calculates weighted compatibility scores, and generates explanations. Results balance the selected categories, so they may not appear in descending score order.
4. [main.py](club_recommender/backend/main.py) loads the CSV, exposes the API routes, serves the homepage, and serves frontend files under `/assets`.
5. [app.js](club_recommender/frontend/app.js) connects the quiz, directory, saved clubs, and recommendation cards to those API routes.

`SCORE_WEIGHTS` remains in `recommender.py`: interests contribute 40%, vibe 30%, logistics 15%, and time commitment 15%. These are compatibility scores, not probabilities. The optional free-text answer does not affect scoring in the current version.

The recommendation endpoint no longer prints submitted answers or normalized student profiles. The recommender still prints individual club-score diagnostics. Quiz answers are held in browser memory and submitted to the API; the app does not save them to a database. Saved club IDs are stored in browser local storage and do not sync between devices.

See [the architecture documentation](club_recommender/docs/ARCHITECTURE.md) for the data schema and algorithm workflow, and [the application README](club_recommender/README.md) for API routes, request formats, and response fields.

## Required dataset

Keep this file in its original location:

```text
club_recommender/data/UPDATED_cornell_clubs_rich_dataset.xlsx - Clubs.csv
```

The app loads it at startup and fails if it is missing or invalid. Club details come from the project dataset and should be confirmed with each organization before relying on current schedules, dues, or recruitment information.

## Deployment

[render.yaml](render.yaml) configures the frontend and Python API as one Render web service:

| Setting        | Value                                                  |
| -------------- | ------------------------------------------------------ |
| Root directory | `club_recommender`                                     |
| Build command  | `pip install -r requirements.txt`                      |
| Start command  | `uvicorn backend.main:app --host 0.0.0.0 --port $PORT` |
| Health check   | `/health`                                              |
| Python version | `3.12.8`                                               |

Local edits affect the hosted app only after they are committed, pushed to its deployment branch, and deployed successfully.

## Project files

```text
info4125_proj/
├── README.md
├── render.yaml
└── club_recommender/
    ├── README.md
    ├── requirements.txt
    ├── requirements-dev.txt
    ├── backend/
    │   ├── __init__.py
    │   ├── main.py
    │   ├── quiz.py
    │   ├── profile.py
    │   └── recommender.py
    ├── frontend/
    │   ├── index.html
    │   ├── styles.css
    │   └── app.js
    ├── data/
    │   └── UPDATED_cornell_clubs_rich_dataset.xlsx - Clubs.csv
    ├── docs/
    │   └── ARCHITECTURE.md
    └── tests/
        └── test_integration.py
```
