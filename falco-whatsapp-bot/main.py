from flask import Flask, request
import openai
import os
import json

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load chatbot logic rules (e.g., refunds, payment info, etc.)
with open("chatbot_logic.json", "r") as file:
    chatbot_rules = json.load(file)

# Optional: Load activities data (for future advanced matching or links)
with open("activities.json", "r") as f:
    activities_data = json.load(f)

# Checks if incoming message matches a rule in the logic file
def check_logic(message):
    for rule in chatbot_rules:
        if any(keyword.lower() in message.lower() for keyword in rule["keywords"]):
            return rule["response"]
    return None

@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    from_number = request.form.get("From", "")
    message_body = request.form.get("Body", "").strip()

    if not message_body:
        return "No message received", 400

    # Check for predefined logic match
    rule_response = check_logic(message_body)
    if rule_response:
        return rule_response

    # Otherwise, let OpenAI handle it
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": message_body},
        ],
        temperature=0.7
    )
    reply = response.choices[0].message["content"].strip()
    return reply

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
