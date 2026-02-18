# Installation and Setup Guide

## Quick Setup (3 Steps)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

**Note:** First run will download Flan-T5-base model (~430MB)

### Step 2: Start Flask Backend
```bash
python app.py
```

### Step 3: Open Frontend
- **Option A:** Double-click `index.html`
- **Option B:** Open http://localhost:8000 (after running `python -m http.server 8000`)

## System Requirements

- Python 3.8+
- 2GB+ RAM
- ~2GB disk space (for model download on first run)
- Windows, macOS, or Linux

## Troubleshooting

### ModuleNotFoundError: No module named 'torch'
```bash
pip install --upgrade pip
pip install torch transformers flask flask-cors
```

### "Cannot connect to Flask backend"
1. Verify Flask is running: `python app.py`
2. Check output shows "Running on http://127.0.0.1:5000"
3. Open http://127.0.0.1:5000/api/health in browser

### Model not downloading
- Check internet connection
- First download is ~350MB
- PyTorch will cache it afterward

## File Structure

```
Ai-content/
├── index.html           # Frontend UI
├── app.py              # Flask backend  
├── requirements.txt    # Python dependencies
├── README.md           # Main documentation
└── SETUP.md            # This file
```

## Performance Tips

- **Model Quality:** Flan-T5-base is superior to DistilGPT-2/GPT-2 for content quality
- Longer `max_length` generates more content but takes more time
- Default is now 500 (4-5 paragraphs) - reduce to 300-350 for faster generation
- Use temperature 0.3-0.5 for factual/informational content
- Use temperature 0.8-1.0 for creative content
- GPU significantly faster than CPU (2-3x speed improvement)

## Creating an Alternative Setup

To use Python's http.server instead of opening HTML directly:

**Terminal 1:**
```bash
python app.py
```

**Terminal 2:**
```bash
python -m http.server 8000
```

Then visit: http://localhost:8000

## API Testing (Optional)

Test the backend with curl:

```bash
curl -X POST http://127.0.0.1:5000/api/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Tell me a story", "max_length": 200}'
```

Check health:
```bash
curl http://127.0.0.1:5000/api/health
```
