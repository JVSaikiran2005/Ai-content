"""
Flask backend for AI Content Generator
Uses local machine learning model (Flan-T5-base) for content generation
No API keys required - everything runs locally
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import logging
import os

app = Flask(__name__, static_folder='.')
CORS(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

model = None
tokenizer = None
device_type = "CPU"

@app.after_request
def add_cache_control(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

def initialize_model():
    global model, tokenizer, device_type

    try:
        logger.info("Initializing language model...")

        dev = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        device_type = "GPU" if torch.cuda.is_available() else "CPU"
        logger.info(f"Using device: {device_type}")

        model_name = "google/flan-t5-base"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name, torch_dtype=torch.float32)
        model.to(dev)
        model.eval()

        logger.info("Model loaded successfully!")
        return True

    except Exception as e:
        logger.error(f"Error initializing model: {str(e)}")
        return False

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "model_loaded": model is not None,
        "device": device_type
    }), 200

@app.route('/api/generate', methods=['POST'])
def generate_content():
    try:
        data = request.get_json()

        if not data or 'prompt' not in data:
            return jsonify({"error": "Missing 'prompt' field in request"}), 400

        prompt = data.get('prompt', '').strip()
        max_length = data.get('max_length', 500)
        temperature = data.get('temperature', 0.7)

        if not prompt:
            return jsonify({"error": "Prompt cannot be empty"}), 400

        if len(prompt) > 500:
            return jsonify({"error": "Prompt is too long (max 500 characters)"}), 400

        if max_length < 50 or max_length > 800:
            max_length = 500

        if temperature < 0.1 or temperature > 1.0:
            temperature = 0.7

        logger.info(f"Generating content for prompt: {prompt[:50]}...")

        instruction_prompt = f"Generate detailed content about: {prompt}"

        inputs = tokenizer(instruction_prompt, return_tensors="pt", max_length=512, truncation=True)
        inputs = {k: v.to(model.device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_length=max_length,
                min_length=150,
                num_beams=5,
                no_repeat_ngram_size=3,
                length_penalty=2.0,
                early_stopping=True,
                temperature=0.85,
                do_sample=True,
                top_p=0.92,
                top_k=50
            )

        content = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

        return jsonify({
            "success": True,
            "prompt": prompt,
            "generated_content": content
        }), 200

    except Exception as e:
        logger.error(f"Error generating content: {str(e)}")
        return jsonify({"error": f"Error generating content: {str(e)}"}), 500

@app.route('/api/models', methods=['GET'])
def get_model_info():
    return jsonify({
        "model_name": "Flan-T5-base",
        "model_type": "Instruction-following Text Generation",
        "description": "Google's Flan-T5 model fine-tuned for instruction following.",
        "local": True,
        "requires_api_key": False,
        "model_size": "~430MB",
        "has_instruction_following": True
    }), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    if initialize_model():
        logger.info("Starting Flask app...")
        app.run(debug=False, host='0.0.0.0', port=5000)
    else:
        logger.error("Failed to initialize model. Exiting.")
        exit(1)
