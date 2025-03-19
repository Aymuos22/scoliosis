
from flask import Flask, render_template, request, redirect, url_for
import os
import base64
from werkzeug.utils import secure_filename

from scoliosis_detection import classify_scoliosis

# Initialize Flask application
app = Flask(__name__)

# Configuration for file uploads
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER




@app.route('/')
def home():
    """Render the home page."""
    return render_template('home.html')

@app.route('/scoliosis-classify', methods=['GET', 'POST'])
def scoliosis_classify():
    """Handle image upload and classification for scoliosis detection."""
    if request.method == 'POST':
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

    return render_template('scoliosis_classify.html')  # Ensure this handles GET requests


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
