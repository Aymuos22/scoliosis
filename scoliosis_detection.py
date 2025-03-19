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
                    {"type": "text", "text": "Analyze this spinal X-ray for scoliosis by assessing spinal curvature, vertebral alignment, and any visible abnormalities. Diagnose 'Scoliosis detected' only if the spine exhibits a clear, well-defined arched curvature rather than a minor deviation. The curvature must form a noticeable C-shape or S-shape, with a Cobb angle of at least 10 degrees and visible vertebral rotation. If the spine is mostly straight or shows slight, irregular, or non-arched deviations, diagnose 'No scoliosis detected.' If the findings are uncertain, borderline, or lack definitive indicators such as rotation and a distinct arch, state 'Inconclusive, further evaluation needed.' Prioritize accuracy and diagnose scoliosis only when a pronounced arched curvature is present. If C-shape or S shape is not visible too much then return no scoliosis"},
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
