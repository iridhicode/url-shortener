# URL Shortener

A minimal URL shortener API built with FastAPI and SQLite.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Setup](#setup)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Running Tests](#running-tests)

## Features

- Shorten any valid HTTP/HTTPS URL to an 8-character ID
- Redirect via short ID to the original URL
- Input validation rejects non-HTTP schemes
- Collision-safe short ID generation with automatic retry
- Health check endpoint

## Requirements

- Python 3.11+
- pipenv

## Setup

```bash
pipenv install
pipenv shell
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## Usage

**Shorten a URL:**

```bash
curl -X POST http://127.0.0.1:8000/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

**Redirect:**

```bash
curl -L http://127.0.0.1:8000/<short_id>
```

## Running Tests

```bash
pipenv install --dev
pytest tests/ -v
```
