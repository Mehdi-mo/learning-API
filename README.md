# learning API

Practice files from working through my "APIs from zero" notes.
FastAPI and Pydantic, one file per part.

| File | Part | What it covers |
|---|---|---|
| `part6_requests.py` | 6 | calling the GitHub API with `requests` |
| `part7_8_parameters.py` | 7-8 | first FastAPI app, path and query parameters |
| `part9_body.py` | 9 | request body, Pydantic model, validation |
| `part10_crud.py` | 10 | full CRUD: POST, GET, PATCH, PUT, DELETE |
| `part11_model_api.py` | 11 | model API: /health, /predict, /predict/batch |

## Run

Set up the environment:

    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    pip install -r requirements.txt

Start any of the API files:

    uvicorn part10_crud:app --reload

Then open http://127.0.0.1:8000/docs to try the endpoints.

The `requests` file is a plain script, so run that one with:

    python part6_requests.py

## Note

The CRUD file keeps items in a dict in memory, so everything is lost when the
server restarts. That is on purpose — it keeps the example about the endpoints
rather than about a database.