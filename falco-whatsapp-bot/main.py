from flask import Flask, request
import openai
import os
import json

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load chatbot logic rules (rules for how to respond)
with open("chatbot_logic.json", "r") as file:
    chatbot_rules = json.load(file)

# Load activities data (activity details with location and URL)
with open("activities.json", "r") as f:
    activities_data = json.load(f)

# Function to check if the incoming message matches a rule in the logic file
def check_logic(message):
    for rule in chatbot_rules["key_rules"].values():
        if any(keyword.lower() in message.lower() for keyword in rule.split()):
            return rule
    return None

# Function to find the matching activity and location from activities.json
def find_activity_location(message):
    for activity in activities_data:
        if activity['name'].lower() in message.lower():
            return activity
    return None

# The main system prompt to build with chatbot rules
def build_system_prompt():
    prompt = "You are a helpful assistant for Ascendia Sports.\n\n"
    for key, rule in chatbot_rules["key_rules"].items():
        prompt += f"- {rule}\n"
    return prompt

@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    from_number = request.form.get("From", "")
    message_body = request.form.get("Body", "").strip()

    if not message_body:
        return "No message received", 400

    # Check if the message matches any predefined logic
    rule_response = check_logic(message_body)
    if rule_response:
        return rule_response

    # Try to match the activity and location
    activity_info = find_activity_location(message_body)
    if activity_info:
        return f"Here's the link for {activity_info['name']}: {activity_info['url']}"

    # If the activity or location is unclear, ask the user for more information
    return "Can you please tell me which activity and location you're interested in?"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
