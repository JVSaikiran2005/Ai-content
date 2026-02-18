# AI Content Generator - Local Edition

🎉 **A fully local AI content generator** with no API keys required! This web application uses a **Flask backend** and **Flan-T5-base** machine learning model to generate high-quality content on various topics.

## ✨ Features

* **🚀 Fully Local:** No external APIs, no API keys needed. Everything runs on your machine!
* **🤖 Advanced ML Model:** Uses **Flan-T5-base** (Google's instruction-following model) - superior quality
* **⚡ High Quality:** Better coherence and instruction following than simpler models
* **📚 Instruction Follow:** Understands natural language prompts effectively
* **⚡ Fast Performance:** Works on CPU and GPU (automatic detection)
* **🎨 Beautiful Interface:** Clean, responsive design built with **Tailwind CSS**
* **✅ Error Handling:** Clear visual feedback during content generation
* **📱 Mobile Responsive:** Works seamlessly on desktop and mobile devices

## 🛠️ Technology Stack

**Frontend:**
* HTML5, CSS (via Tailwind CSS CDN)
* Vanilla JavaScript for DOM manipulation

**Backend:**
* Flask 3.0.0
* Python 3.8+ 
* PyTorch & Transformers (Hugging Face)
* **Flan-T5-base ML Model** (Google's instruction-following model)

## 📋 Prerequisites

Before running this project, ensure you have:

1. **Python 3.8 or higher** installed ([Download Python](https://www.python.org/downloads/))
2. **pip** (usually comes with Python)
3. **A WebSocket-enabled browser** (Chrome, Firefox, Edge, Safari - all modern browsers)
4. **~2GB free disk space** (for downloading the ML model on first run)

**System Requirements:**
* Minimum 2GB RAM (4GB+ recommended)
* Works on Windows, macOS, and Linux
* Optional: GPU (NVIDIA CUDA) for faster generation, but CPU is sufficient

## ⚙️ Setup and Installation

### Step 1: Install Python Dependencies

Navigate to the project directory in your terminal and install the required packages:

```bash
pip install -r requirements.txt
```

This will install:
- **Flask**: Web framework for the backend
- **Flask-CORS**: Enable cross-origin requests
- **PyTorch**: Deep learning library
- **Transformers**: Hugging Face transformers library with pre-trained models
- **NumPy**: Numerical computing

**First-time setup note:** When you run the Flask app for the first time, it will automatically download the Flan-T5-base model (~430MB). This is a one-time download.

### Step 2: Start the Flask Backend

In the project directory, run the Flask application:

```bash
python app.py
```

You should see output like:
```
Initializing language model...
Using device: CPU  (or GPU if available)
Model loaded successfully!
 * Running on http://127.0.0.1:5000
```

**Keep this terminal window open while using the application.**

### Step 3: Run the Frontend

Once the Flask backend is running, open `index.html` in your web browser:

1. **Option A - Direct Open:** Double-click `index.html` in your file explorer
2. **Option B - Local Server (Recommended):** 
   - Install a simple server, or use Python's built-in server in a NEW terminal:
   ```bash
   # Windows
   python -m http.server 8000
   
   # macOS/Linux
   python3 -m http.server 8000
   ```
   - Then open http://localhost:8000 in your browser

3. **Option C - VS Code Live Server:**
   - Install the "Live Server" extension
   - Right-click `index.html` and select "Open with Live Server"

## 📖 How to Use

1. Open the application in your browser
2. Type your prompt in the text area (e.g., "Write a short story about a robot")
3. Click "Generate Content" button
4. Wait for the AI to generate content (usually 5-30 seconds depending on your system)
5. Read the generated content displayed below

### Example Prompts

- "Write a blog post about renewable energy"
- "Create a short story about time travel"
- "Explain quantum computing in simple terms"
- "Write a poem about the night sky"
- "Describe a futuristic city"

## 🔧 Advanced Configuration

### Model Parameters (in `app.py`)

You can adjust the generation behavior by modifying the parameters in the `/api/generate` endpoint:

```python
- max_length: Maximum length of generated text (default: 500, range: 100-800)
- min_length: Minimum length to generate (default: 100)
- temperature: Creativity level (default: 0.7)
  * 0.0 = More deterministic/consistent
  * 0.7 = Good balance
  * 1.0 = More random/creative
- num_beams: Beam search for better quality (default: 4)
```

### Alternative Models

You can use other Hugging Face models by modifying the code in `app.py` around line 45:

**Current model (Recommended for quality):**
```python
model_pipeline = pipeline(
    "text2text-generation",
    model="google/flan-t5-base",
    device=device
)
```

**Other options:**
```python
# Flan-T5-large (highest quality, but larger/slower - ~800MB)
model_pipeline = pipeline("text2text-generation", model="google/flan-t5-large", device=device)

# GPT-2 (smaller, faster, but lower quality)
model_pipeline = pipeline("text-generation", model="gpt2", device=device)

# GPT-Neo (good balance between quality and size)
model_pipeline = pipeline("text-generation", model="EleutherAI/gpt-neo-125M", device=device)
```

## 🚀 API Endpoints

The Flask backend provides these REST APIs:

### 1. Health Check
```
GET http://127.0.0.1:5000/api/health
```

### 2. Generate Content
```
POST http://127.0.0.1:5000/api/generate
Content-Type: application/json

{
  "prompt": "Your topic here",
  "max_length": 250,
  "temperature": 0.8
}
```

### 3. Model Info
```
GET http://127.0.0.1:5000/api/models
```

## 🐛 Troubleshooting

### Issue: "Cannot connect to the Flask backend"
- Ensure Flask is running: `python app.py`
- Check that it shows "Running on http://127.0.0.1:5000"

### Issue: "No module named 'torch'" 
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Issue: Model download is slow
- First download is ~350MB and takes a few minutes
- Model will be cached after first run

## 📊 Performance Notes

Expected generation times:
- CPU (Intel i5): 10-30 seconds
- CPU (Intel i7): 5-15 seconds  
- GPU (NVIDIA): 2-5 seconds

## 📁 File Structure
