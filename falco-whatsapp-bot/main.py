from flask import Flask, request
import openai
import os
import json

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load chatbot logic rules from dictionary under "key_rules"
with open("chatbot_logic.json", "r") as file:
    logic_data = json.load(file)
    chatbot_rules = logic_data["key_rules"]

# Optional: Load activities data (if you're using it in the future)
with open("activities.json", "r") as f:
    activities_data = json.load(f)

# Rule-checking logic
def check_logic(message):
    for rule_id, rule_text in chatbot_rules.items():
        if any(word in message.lower() for word in rule_text.lower().split()):
            return rule_text
    return None

@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    from_number = request.form.get("From", "")
    message_body = request.form.get("Body", "").strip()

    if not message_body:
        return "No message received", 400

    rule_response = check_logic(message_body)
    if rule_response:
        return rule_response

    # OpenAI fallback
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": message_body}],
        temperature=0.7
    )
    reply = response.choices[0].message["content"].strip()
    return reply

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
