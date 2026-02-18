# Configuration reference for the AI Content Generator

## Flask Backend Configuration

The Flask backend is configured in `app.py`. Key settings:

### Model Selection
- **Current Model:** DistilGPT-2 (lightweight, ~350MB download)
- **Location:** Line 76 in `app.py`
- **Default:** Works on CPU and GPU

### API Configuration
- **Host:** 127.0.0.1 (localhost)
- **Port:** 5000
- **Debug Mode:** Enabled (change to False in production)
- **CORS:** Enabled for all origins

### Generation Parameters
- **Default Max Length:** 200 tokens
- **Temperature:** 0.7 (balanced creativity)
- **Top-P Sampling:** 0.95
- **Do Sample:** True

## Frontend Configuration

The frontend is configured in `index.html`. Key settings:

### API Connection
- **Backend URL:** http://127.0.0.1:5000/api
- **Location:** Line 171 in `index.html`
- **Auto-Detection:** Checks backend health on page load

### Generation Settings
- **Default Max Length:** 250 tokens
- **Default Temperature:** 0.8
- **Response Type:** JSON

## Python Environment Requirements

### Minimum Versions
- Python: 3.8+
- Flask: 3.0.0
- PyTorch: 2.1.0
- Transformers: 4.35.0

### Hardware Recommendations
- **Minimum RAM:** 2GB
- **Recommended RAM:** 4GB+
- **Storage:** 2GB free (for model cache)
- **GPU:** Optional (NVIDIA CUDA supported)

## Device Configuration

The system automatically detects GPU availability:
```python
device = 0 if torch.cuda.is_available() else -1
# 0 = GPU, -1 = CPU
```

## Model Details

### DistilGPT-2
- **Size:** ~350MB
- **Download:** First run only, then cached
- **Parameters:** 82M
- **Speed:** ~10-30s on CPU, ~2-5s on GPU
- **Quality:** Good for creative writing and content generation

## Port Configuration

If port 5000 is already in use, modify line 238 in `app.py`:
```python
# Default
app.run(debug=True, host='127.0.0.1', port=5000)

# Alternative ports
app.run(debug=True, host='127.0.0.1', port=8080)
app.run(debug=True, host='127.0.0.1', port=3000)
```

## CORS Settings

To restrict to specific origins, modify line 10 in `app.py`:
```python
# Current: Allow all
CORS(app)

# Restricted example
CORS(app, origins=["http://localhost:8000"])
```

## Environment Variables (Optional)

You can set these in your system or terminal:
- `FLASK_ENV`: "development" or "production"
- `FLASK_DEBUG`: "1" or "0"
- `TORCH_HOME`: Custom cache location for models

Example:
```bash
# Windows PowerShell
$env:FLASK_ENV = "development"
$env:FLASK_DEBUG = "1"

# Windows Command Prompt
set FLASK_ENV=development
set FLASK_DEBUG=1

# macOS/Linux
export FLASK_ENV=development
export FLASK_DEBUG=1
```

## Logging Configuration

Logging is configured in `app.py` line 18-19:
```python
logging.basicConfig(level=logging.INFO)
```

Change to DEBUG for more verbose output:
```python
logging.basicConfig(level=logging.DEBUG)
```

## Performance Tuning

### For Slower Machines
1. Reduce `max_length` to 150-200
2. Use temperature 0.7 or lower
3. Close other applications
4. Use smaller model (e.g., distilgpt2)

### For Faster Generation
1. Use GPU if available
2. Increase max_length (200-300)
3. Use temperature 0.8-0.9 for variety
4. Increase top_p to 0.98

## Security Considerations

- Backend runs on localhost only (not internet-accessible)
- No sensitive data transmission
- No external API calls
- Model runs locally (no cloud services)

## Deployment Considerations

For production deployment:
1. Set `debug=False` in app.py line 238
2. Use WSGI server (e.g., Gunicorn)
3. Add authentication if needed
4. Set proper CORS origins
5. Use HTTPS
6. Add rate limiting

Example with Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 127.0.0.1:5000 app:app
```
