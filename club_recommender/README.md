# Cornell Club Recommender

A V1 adaptive quiz + explainable content-based club recommender.

## Run

```bash
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

Then open `http://127.0.0.1:8000` in a browser.

For the API docs:
`http://127.0.0.1:8000/docs`

## Data

The recommender loads the supplied club database from the project root:

```text
UPDATED_cornell_clubs_rich_dataset.xlsx - Clubs.csv
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

## Deploy to Vercel

The FastAPI app serves the frontend and API from the same domain. Vercel uses `index.py` as its Python entrypoint.

### Deploy from this folder with the Vercel CLI

1. Install Node.js if needed, then install and sign in to the Vercel CLI:

	```bash
	npm install --global vercel
	vercel login
	```

2. From this project folder, run:

	```bash
	vercel
	```

	Follow the prompts to create a Vercel project. To publish the production site, run `vercel --prod`.

3. Open the `https://...vercel.app` URL printed by the CLI. The quiz is at the root URL, and the API docs are at `/docs`.

Alternatively, choose **Add New → Project** in the Vercel dashboard, import the repository, and set **Root Directory** to `club_recommender` before deploying. Each later push to the connected branch will redeploy the site.

The supplied CSV is included in this project, so Vercel will load its club data after deployment.
