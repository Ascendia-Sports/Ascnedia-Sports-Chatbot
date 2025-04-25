from flask import Flask, request
import openai
import os
import json

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load chatbot logic and activities into memory
with open("chatbot_logic.json", "r") as f:
    chatbot_logic = json.load(f)

with open("activities.json", "r") as f:
    activities_data = json.load(f)

# Helper function: Build the system prompt
def build_system_prompt():
    prompt = (
        "You are an Ascendia Sports WhatsApp support agent.\n"
        "Answer customers naturally based on the following rules and activities.\n\n"
        "Important Rules:\n"
    )
    for key, rule in chatbot_logic["key_rules"].items():
        prompt += f"- {rule}\n"

    prompt += "\nAvailable Activities:\n"
    for activity in activities_data:
        prompt += f"- {activity['title']} in {activity['location']} (${activity['price']} {activity['currency']})\n"

    prompt += (
        "\nOnly provide information based on the rules and activities above.\n"
        "Keep replies short, human-like, and natural. Avoid using emojis.\n"
        "If you don't know the answer, tell the customer to email contact@ascendia-sports.com.\n"
    )
    return prompt

@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    from_number = request.form.get("From", "")
    message_body = request.form.get("Body", "").strip()

    if not message_body:
        return "No message received", 400

    system_prompt = build_system_prompt()

    # Use OpenAI to create a response
    openai_response = openai.chat.completions.create(
        model="gpt-3.5-turbo",  # safer to use 3.5 unless you upgrade to GPT-4 access
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message_body},
        ],
        temperature=0.5
    )

    reply = openai_response.choices[0].message.content.strip()
    return reply

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
