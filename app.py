"""
Flask backend for AI Content Generator
Uses local machine learning model (Flan-T5-base) for content generation
No API keys required - everything runs locally
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import torch
from transformers import pipeline
import logging

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global model and pipeline
model_pipeline = None
device = None

def initialize_model():
    """Initialize the text generation model"""
    global model_pipeline, device
    
    try:
        logger.info("Initializing language model...")
        
        # Detect device (GPU if available, otherwise CPU)
        device = 0 if torch.cuda.is_available() else -1
        device_type = "GPU" if device == 0 else "CPU"
        logger.info(f"Using device: {device_type}")
        
        # Load Flan-T5-base model (superior quality for content generation)
        # Better instruction following and coherence than GPT-2
        # Size: ~430MB, runs efficiently on most machines
        model_pipeline = pipeline(
            "text2text-generation",
            model="google/flan-t5-base",
            device=device,
            torch_dtype=torch.float32
        )
        
        logger.info("Model loaded successfully!")
        return True
    
    except Exception as e:
        logger.error(f"Error initializing model: {str(e)}")
        return False

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "model_loaded": model_pipeline is not None,
        "device": "GPU" if device == 0 else "CPU"
    }), 200

@app.route('/api/generate', methods=['POST'])
def generate_content():
    """
    Generate AI content based on user prompt
    
    Request JSON:
    {
        "prompt": "Your topic or prompt here",
        "max_length": 500,  # Optional, default 500 (produces 4-5 paragraphs)
        "temperature": 0.7  # Optional, default 0.7 (0.0 = deterministic, 1.0 = creative)
    }
    """
    try:
        # Get request data
        data = request.get_json()
        
        if not data or 'prompt' not in data:
            return jsonify({
                "error": "Missing 'prompt' field in request"
            }), 400
        
        prompt = data.get('prompt', '').strip()
        max_length = data.get('max_length', 500)
        temperature = data.get('temperature', 0.7)
        
        # Validate inputs
        if not prompt:
            return jsonify({
                "error": "Prompt cannot be empty"
            }), 400
        
        if len(prompt) > 500:
            return jsonify({
                "error": "Prompt is too long (max 500 characters)"
            }), 400
        
        if max_length < 50 or max_length > 800:
            max_length = 500
        
        if temperature < 0.0 or temperature > 1.0:
            temperature = 0.7
        
        logger.info(f"Generating content for prompt: {prompt[:50]}...")
        
        # Create an instruction prompt for Flan-T5
        # This helps the model understand better what's expected
        instruction_prompt = f"Generate detailed content about: {prompt}"
        
        # Generate content using the model
        with torch.no_grad():
            generated = model_pipeline(
                instruction_prompt,
                max_length=max_length,
                min_length=100,
                num_beams=4,
                early_stopping=True,
                temperature=temperature,
                do_sample=False
            )
        
        # Extract generated text
        content = generated[0]['generated_text'].strip()
        
        return jsonify({
            "success": True,
            "prompt": prompt,
            "generated_content": content,
            "full_content": generated_text
        }), 200
    
    except Exception as e:
        logger.error(f"Error generating content: {str(e)}")
        return jsonify({
            "error": f"Error generating content: {str(e)}"
        }), 500

@app.route('/api/models', methods=['GET'])
def get_model_info():
    """Get information about the loaded model"""
    return jsonify({
        "model_name": "Flan-T5-base",
        "model_type": "Instruction-following Text Generation",
        "description": "Google's Flan-T5 model fine-tuned for instruction following. Superior quality for content generation compared to GPT-2 variants.",
        "local": True,
        "requires_api_key": False,
        "model_size": "~430MB",
        "has_instruction_following": True
    }), 200

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "error": "Endpoint not found"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        "error": "Internal server error"
    }), 500

if __name__ == '__main__':
    # Initialize the model when the app starts
    if initialize_model():
        logger.info("Starting Flask app...")
        # Run the Flask app
        # Set debug=False in production
        app.run(debug=True, host='127.0.0.1', port=5000)
    else:
        logger.error("Failed to initialize model. Exiting.")
        exit(1)
