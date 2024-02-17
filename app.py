from flask import Flask, request, jsonify, send_from_directory
import os
import requests
from dotenv import load_dotenv
import fitz  # PyMuPDF

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__, static_folder='public')

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_URL = "https://api.openai.com/v1/completions"

# Serve the main page
@app.route('/')
def index():
    return send_from_directory('public', 'index.html')

# Serve static files (CSS, JS)
@app.route('/public/<path:path>')
def send_public(path):
    return send_from_directory('public', path)

# Extract text from PDF (you might want to cache this result)
def extract_text_from_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""

# Endpoint to handle chat requests
@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    user_query = data['query']
    
    # Optional: Enhance the query with information from a PDF
    pdf_text = extract_text_from_pdf('path/to/your/abc.pdf')  # Adjust path as needed
    
    # Construct the prompt
    context = "You are a personal accountant. Provide professional, accurate, and helpful financial advice."
    prompt = f"{context}\n\nQuestion: {user_query}"
    
    response = requests.post(
        OPENAI_URL,
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "text-davinci-003",  # Update to the latest model as needed
            "prompt": prompt,
            "temperature": 0.5,
            "max_tokens": 150,
        },
    )

    if response.status_code == 200:
        return jsonify({"response": response.json()['choices'][0]['text'].strip()})
    else:
        return jsonify({"error": "Failed to fetch response from OpenAI API"}), 500

if __name__ == '__main__':
    app.run(debug=True)
