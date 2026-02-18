# AI Content Generator

## Overview
A fully local AI content generator web application using Flask backend and Google's Flan-T5-base model. No API keys required - everything runs locally using Hugging Face Transformers.

## Project Architecture
- **app.py** - Flask backend serving both the HTML frontend and the API endpoints
- **index.html** - Frontend with Tailwind CSS, calls `/api/generate` for content generation
- **requirements.txt** - Python dependencies

## Key Endpoints
- `GET /` - Serves the frontend HTML
- `GET /api/health` - Health check
- `POST /api/generate` - Generate AI content (accepts prompt, max_length, temperature)
- `GET /api/models` - Model info

## Tech Stack
- Python 3.11
- Flask (web framework)
- PyTorch (CPU-only, ML backend)
- Transformers (Hugging Face, model loading)
- Tailwind CSS (via CDN, frontend styling)

## Running
The app runs on port 5000. On first start, it downloads the Flan-T5-base model (~430MB) which may take a minute.
