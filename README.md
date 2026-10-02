# job-hunter-autogen

A local AI job-hunting assistant that searches public job offers, compares them with your CV, scores the fit, and generates a daily digest.

## Features
- local model via LM Studio
- public job gathering
- CV/job matching
- SQLite storage
- daily digest output

## Setup

1. Install LM Studio and start a local LLM.
2. Enable Local API server on `http://localhost:1234/v1`.
3. Install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

4. Copy `.env.example` to `.env` if needed.

## Run

```bash
python -m job_hunter --keywords "python backend" --location "Paris" --limit 10
```

## Notes
This is a starter project. For LinkedIn, prefer public sources and compliant workflows.
