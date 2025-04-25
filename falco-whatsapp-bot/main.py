from flask import Flask, request
import openai
import os
import json
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load activities (optional)
with open("activities.json", "r") as f:
    activities_data = json.load(f)

@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    message_body = request.form.get("Body", "").strip()

    if not message_body:
        return "No message received", 400

    # Create Twilio response
    twilio_response = MessagingResponse()

    # Otherwise use OpenAI
    openai_response = openai.chat.completions.create(
        model="gpt-4o",  # <- FIXED here
        messages=[{"role": "user", "content": message_body}],
        temperature=0.7
    )
    reply = openai_response.choices[0].message.content.strip()
    twilio_response.message(reply)
    return str(twilio_response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
