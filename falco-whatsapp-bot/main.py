from flask import Flask, request
import openai
import os
import json

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load chatbot logic rules
with open("chatbot_logic.json", "r") as file:
    chatbot_rules = json.load(file)

# Load activities data
with open("activities.json", "r") as f:
    activities_data = json.load(f)

# Match user message to logic rules
def check_logic(message):
    for rule in chatbot_rules:
        if any(keyword.lower() in message.lower() for keyword in rule["keywords"]):
            return rule["response"]
    return None

# Format relevant activities if a keyword like "bungee" or "paragliding" is detected
def find_matching_activities(message):
    results = []
    for activity in activities_data:
        if any(word.lower() in activity["title"].lower() for word in message.split()):
            results.append(activity)
    return results[:3]  # Limit to top 3 matches for now

@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    from_number = request.form.get("From", "")
    message_body = request.form.get("Body", "").strip()

    if not message_body:
        return "No message received", 400

    # First: apply logic rules
    rule_response = check_logic(message_body)
    if rule_response:
        return rule_response

    # Second: search for activities
    matched = find_matching_activities(message_body)
    if matched:
        response_lines = ["Here are some matching adventures:"]
        for activity in matched:
            response_lines.append(f"- {activity['title']}: {activity['url']}")
        return "\n".join(response_lines)

    # Fallback: ask OpenAI if no rule or activity match
    openai_response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": message_body},
        ],
        temperature=0.7
    )
    return openai_response.choices[0].message.content.strip()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
