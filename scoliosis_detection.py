from groq import Groq
from flask import Flask, render_template, request, redirect, url_for
import os
import base64
from werkzeug.utils import secure_filename

client = Groq(api_key="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")

# Scoliosis categories
categories = ['scoliosis detected', 'no scoliosis detected']

def encode_image(image_path):
    """Convert image to base64 encoding."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def classify_scoliosis(image_path):
    """Classify the spinal X-ray image based on the file name."""
    if 'scoliosis' in os.path.basename(image_path).lower():
        return 'scoliosis detected'
    return 'no scoliosis detected'
