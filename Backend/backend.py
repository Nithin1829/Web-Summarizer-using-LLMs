from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

# Setup Flask
app = Flask(__name__)
CORS(app)

# Root health check route
@app.route("/", methods=["GET"])
def home():
    return "✅ Flask backend is running!"

# Scraper class
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

# Message builder (takes plain text, not Website)
def message_for(text):
    return [
        {
            "role": "system",
            "content": "You are a helpful assistant that summarizes website content clearly and concisely."
        },
        {
            "role": "user",
            "content": f"Summarize the following web page:\n\n{text}"
        }
    ]

# Main summarize endpoint
@app.route("/summarize", methods=["POST"])
def summarize():
    try:
        data = request.get_json()
        url = data.get("url")

        website = Website(url)
        text = website.text

        # Truncate to 24,000 characters (~8,000 tokens)
        if len(text) > 24000:
            text = text[:24000]

        messages = message_for(text)

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # You can change this to "gpt-4o" if needed
            messages=messages
        )

        summary = response.choices[0].message.content
        return jsonify({"summary": summary})

    except Exception as e:
        print("❌ Error:", e)
        return jsonify({"error": str(e)}), 500

# Run the app
if __name__ == "__main__":
    app.run(debug=True, port=5000)

