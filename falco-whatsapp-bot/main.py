from flask import Flask, request
import openai
import os
import json
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load chatbot logic rules
with open("chatbot_logic.json", "r") as file:
    chatbot_rules = json.load(file)["key_rules"]

# Load activities if needed
with open("activities.json", "r") as f:
    activities_data = json.load(f)

# Rule checker
def check_logic(message):
    for rule in chatbot_rules.values():
        if any(keyword.lower() in message.lower() for keyword in rule.split()):
            return rule
    return None

@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    message_body = request.form.get("Body", "").strip()
    if not message_body:
        return "No message", 400

    # Logic response first
    logic_response = check_logic(message_body)

    # If no match, fallback to OpenAI
    if not logic_response:
        completion = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": message_body}],
            temperature=0.7
        )
        logic_response = completion.choices[0].message.content.strip()

    # Format Twilio response
    twiml = MessagingResponse()
    twiml.message(logic_response)
    return str(twiml)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
