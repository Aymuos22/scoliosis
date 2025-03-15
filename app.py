from flask import Flask, render_template, request, redirect, url_for
import os
import base64
from werkzeug.utils import secure_filename
from groq import Groq

# Initialize Flask application
app = Flask(__name__)

# Configuration for file uploads
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Groq API client
client = Groq(api_key="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")

# Scoliosis categories
categories = ['scoliosis detected', 'no scoliosis detected']

def encode_image(image_path):
    """Convert image to base64 encoding."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def classify_scoliosis(image_path):
    """Classify the spinal X-ray image using the Groq API."""
    base64_image = encode_image(image_path)
    
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Detect if scoliosis is present in this spinal X-ray. Possible outputs: scoliosis detected, no scoliosis detected."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}   
                ],
            }
        ],
        model="llama-3.2-11b-vision-preview",
    )
    
    response_text = chat_completion.choices[0].message.content.lower()
    for category in categories:
        if category in response_text:
            return category
    return "Unknown"

@app.route('/')
def home():
    """Render the scoliosis classification page."""
    return render_template('scoliosis_classify.html')

@app.route('/scoliosis-classify', methods=['POST'])
def scoliosis_classify():
    """Handle image upload and classification for scoliosis detection."""
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # Perform classification
    predicted_category = classify_scoliosis(file_path)

    return render_template('scoliosis_classify.html', prediction=predicted_category)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
