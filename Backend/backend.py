from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
from dotenv import load_dotenv
import os
import subprocess

# Load .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

# Setup Flask
app = Flask(__name__)
CORS(app)


class Website:
    def __init__(self, url):
        self.url = url
        self.text = self.extract_text()

    def extract_text(self):
        try:
            response = requests.get(self.url)
            soup = BeautifulSoup(response.text, 'html.parser')
            for tag in soup(['script', 'style', 'nav', 'footer', 'header']):
                tag.decompose()
            return soup.get_text(separator=' ', strip=True)
        except Exception as e:
            return f"Failed to extract text from URL: {e}"

def build_prompt(text):
    return f"Summarize the following web page:{text}"

@app.route("/summarize", methods=["POST"])
def summarize():
    try:
        data = request.get_json()
        url = data.get("url")

        website = Website(url)
        text = website.text

        # Truncate to 6,000 characters (~2,000 tokens)
        if len(text) > 6000:
            text = text[:6000]

        prompt = build_prompt(text)

        # OpenAI API summary
        messages = [
            {"role": "system", "content": "You are a helpful assistant that summarizes website content clearly and concisely."},
            {"role": "user", "content": prompt}
        ]

        openai_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        openai_summary = openai_response.choices[0].message.content

        # Ollama local model summary
        ollama_response = subprocess.run(
            ["ollama", "run", "llama3", prompt],
            capture_output=True,
            text=True
        )
        ollama_summary = ollama_response.stdout.strip()

        return jsonify({
            "openai_summary": openai_summary,
            "ollama_summary": ollama_summary
        })

    except Exception as e:
        print("❌ Error:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
