from flask import Flask, request
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
VERIFY_TOKEN = "brideside123"
PIPEDRIVE_API_TOKEN = os.getenv("PIPEDRIVE_API_TOKEN")

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        return "Invalid verify token", 403

    if request.method == "POST":
        data = request.json
        print("Received data:", data)

        try:
            msg = data['entry'][0]['messaging'][0]['message']['text']
            user = data['entry'][0]['messaging'][0]['sender']['id']
            create_lead_in_pipedrive(f"user_{user}", msg)
        except Exception as e:
            print("Error:", e)

        return "OK", 200

def create_lead_in_pipedrive(name, message):
    person_data = {
        "name": name,
        "email": f"{name}@dm.com"
    }
    person_resp = requests.post(
        f"https://api.pipedrive.com/v1/persons?api_token={PIPEDRIVE_API_TOKEN}",
        json=person_data
    )
    person_id = person_resp.json().get("data", {}).get("id")

    if person_id:
        lead_data = {
            "title": f"IG DM from {name}",
            "person_id": person_id
        }
        requests.post(
            f"https://api.pipedrive.com/v1/leads?api_token={PIPEDRIVE_API_TOKEN}",
            json=lead_data
        )

if __name__ == "__main__":
    app.run(port=5000)
