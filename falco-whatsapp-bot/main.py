from flask import Flask, request
import openai
import os
import json
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load chatbot logic rules
with open("chatbot_logic.json", "r") as file:
    logic_data = json.load(file)

if isinstance(logic_data, dict) and "key_rules" in logic_data:
    chatbot_rules = logic_data["key_rules"]
else:
    chatbot_rules = logic_data

# Optional: Load activities
with open("activities.json", "r") as f:
    activities_data = json.load(f)

# Checks for logic rule match
def check_logic(message):
    for rule in chatbot_rules.values():
        if any(keyword.lower() in message.lower() for keyword in rule.get("keywords", [])):
            return rule.get("response")
    return None

@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    from_number = request.form.get("From", "")
    message_body = request.form.get("Body", "").strip()

    if not message_body:
        return "No message received", 400

    # Create Twilio MessagingResponse
    twilio_response = MessagingResponse()

    # Check logic rules
    rule_response = check_logic(message_body)
    if rule_response:
        twilio_response.message(rule_response)
        return str(twilio_response)

    # Otherwise use OpenAI
    openai_response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": message_body}],
        temperature=0.7
    )
    reply = openai_response.choices[0].message.content.strip()
    twilio_response.message(reply)
    return str(twilio_response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
