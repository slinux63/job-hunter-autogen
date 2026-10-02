# job-hunter-autogen

A local AI job-hunting assistant built with Python, AutoGen-inspired agent orchestration, and a local LM Studio model.

What this starter project does:
- collects public job offers from a few public search sources
- analyzes a CV/profile against each offer
- scores each role by fit and relevance
- stores the result in SQLite
- generates a daily digest of the best opportunities
- runs fully on your local machine with a local LLM

Important note:
- Direct scraping of LinkedIn is not recommended due to platform policies.
- This project prefers public job listings and supported job boards.

## Architecture

```text
job_hunter/
├── __init__.py
├── __main__.py
├── agents.py
├── config.py
├── db.py
├── main.py
├── sources.py
├── templates/
│   └── cv_template.md
└── __pycache__/
```

## Prerequisites

- Python 3.10+
- LM Studio installed and running
- a local model loaded in LM Studio
- internet access for public source checks

## Local LM Studio setup

1. Install LM Studio.
2. Download a local model such as Mistral or Llama.
3. Open the LM Studio server tab.
4. Enable the local OpenAI-compatible API server.
5. Keep the default base URL as:

```bash
http://localhost:1234/v1
```

## Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Environment

Create a `.env` file from the example:

```bash
cp .env.example .env
```

Then adjust the values if needed:

```bash
LMSTUDIO_BASE_URL=http://localhost:1234/v1
LMSTUDIO_MODEL=mistral
JOB_KEYWORDS=python backend
JOB_LOCATION=Paris
DB_PATH=data/job_hunter.db
CV_PATH=data/cv.md
MAX_RESULTS=10
```

## Run the project

```bash
python -m job_hunter
```

or:

```bash
python -m job_hunter.main --keywords "python backend" --location "Paris" --limit 10
```

## What the script does

- loads the CV from `data/cv.md`
- searches public job sources
- normalizes and stores offers
- computes a match score
- saves the daily summary to SQLite
- prints a JSON digest in the terminal

## Example output

```json
{
  "jobs": [
    {
      "title": "Python backend developer",
      "company": "Example Company",
      "match_score": 88,
      "action": "Apply now"
    }
  ],
  "digest": "# Daily job digest"
}
```

## Good next steps

- add a proper Greenhouse / Lever adapter
- add recruiter outreach generation
- save interview notes and follow-ups
- add a lightweight web dashboard
- switch from SQLite to PostgreSQL for larger data sets

## Notes

This is a starter project designed to help you prototype a local recruiting agent in a privacy-friendly way. It is intentionally simple and easy to extend.
