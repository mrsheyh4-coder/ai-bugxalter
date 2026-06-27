# AI Bugxalter

Verified public repository and candidate portfolio project.

## Status

- Repository: public
- Live URL: Vercel deployment records exist, but the checked deployment opens Vercel login and is not verified as a public demo.
- Portfolio category: AI Business Automation, Accounting Workflow, Compliance Assistant, Telegram Integration
- Security cleanup: default JWT secret, default admin password, and local DB password fallback removed on 2026-06-27

## Overview

AI Bugxalter is a backend-focused AI accounting assistant prototype with FastAPI services, user/auth models, tax/compliance endpoints, Gemini/Groq/OpenAI-ready agent modules, Telegram notification hooks, and database initialization scripts.

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL / SQLite-ready local setup
- Pydantic
- Python-Jose JWT
- Passlib / bcrypt
- Google Generative AI
- Groq
- OpenAI-compatible tooling
- Telegram bot integration hooks
- Vercel Python function entrypoint

## Main Features

- Auth and user model foundation
- AI agent orchestration modules
- Tax/compliance API structure
- Risk analyzer and compliance agent
- Telegram notification services
- Database setup scripts
- Vercel serverless routing config

## Local Setup

```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
```

Create `.env` from `.env.example` and set required values:

```bash
SECRET_KEY=your-secure-secret
INITIAL_ADMIN_PASSWORD=your-secure-admin-password
DATABASE_URL=your-database-url
```

## Run

```bash
uvicorn app.main:app --reload
```

## Security Notes

- Do not commit `.env` files.
- `SECRET_KEY`, API keys, Telegram token, and admin password must be configured through environment variables.
- Rotate any real credentials that were used before the 2026-06-27 cleanup.

## Portfolio Use

Use this project only after confirming the final positioning and adding a public demo or screenshots.

Good fit for:

- AI-powered backend prototypes
- Business automation
- Accounting/tax workflows
- Telegram notification flows
- FastAPI service architecture
