# ClubQuest Application API Reference

This document describes the API served by `backend/main.py`. For installation, running the app, features, scoring, data requirements, and deployment, use the [root README](../README.md).

- [Local setup](../README.md#run-locally)
- [Integration test instructions and coverage](../README.md#run-the-integration-tests)
- [Recommendation workflow and scoring](../README.md#how-it-works)
- [Required dataset](../README.md#required-dataset)
- [Deployment settings](../README.md#deployment)

## API routes

All routes are relative to the app's origin. The frontend calls these routes on the same origin.

| Method | Route         | Purpose                                                                    |
| ------ | ------------- | -------------------------------------------------------------------------- |
| GET    | `/`           | Serve the frontend homepage.                                               |
| GET    | `/assets/...` | Serve files from the frontend folder, including JavaScript and CSS.        |
| GET    | `/quiz/start` | Return the opening category question.                                      |
| POST   | `/quiz/next`  | Return the next question and remaining question IDs for submitted answers. |
| POST   | `/recommend`  | Build a profile and return club recommendations.                           |
| GET    | `/clubs`      | Return the loaded club dataset as a JSON array.                            |
| GET    | `/health`     | Return service status, loaded club count, and dataset path.                |
| GET    | `/docs`       | Display interactive API documentation.                                     |

## Quiz requests and responses

`GET /quiz/start` returns an object with a `question` field. Each question includes `id`, `question`, `type`, `max_selections`, and `options`; each option has an `id` and a `label`.

Send answers to `POST /quiz/next` as JSON, using question IDs as keys and option IDs as values. Multiple-choice answers use arrays; single-choice and text answers use strings.

```json
{
  "answers": {
    "categories": ["music"]
  }
}
```

The response contains:

- `question`: the next question object, or `null` when the quiz is complete.
- `remaining`: unanswered question IDs in their planned order.

## Recommendation requests and responses

Send an `answers` object to `POST /recommend`, with an optional `top_n`. This minimal example omits the additional preferences normally collected by the browser quiz:

```json
{
  "answers": {
    "categories": ["music"],
    "music": ["a_cappella"],
    "time": "flexible"
  },
  "top_n": 12
}
```

`top_n` defaults to 10 and is clamped to 1–50. Fewer clubs may be returned if fewer meet the filters.

The response contains the normalized `profile` and a `recommendations` array. Each recommendation includes:

- `club_id`, `club_name`, `category`, and `subcategory`.
- `summary`: the club's short description.
- `score`: the weighted compatibility score on a 0–1 scale.
- `match_percent`: the score expressed on a 0–100 scale.
- `reasons`: human-readable match explanations.

For the CSV schema and algorithm walkthrough, see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).
