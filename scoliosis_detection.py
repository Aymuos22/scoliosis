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


    response_text = chat_completion.choices[0].message.content.lower()
    for category in categories:
        if category in response_text:
            return category
    return "Unknown"
def classify_scoliosis(image_path):
    """Classify the spinal X-ray image using the Groq API."""
    base64_image = encode_image(image_path)
    
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text":"classify scoliosis in this image amd return scoliosis or no scoliosis detected."},
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
    return "No Scoliosis Detected"
