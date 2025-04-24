
from flask import Flask, request
import openai
import os

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    from_number = request.form.get("From", "")
    message_body = request.form.get("Body", "").strip()

    if not message_body:
        return "No message received", 400

    # Simulate typing delay
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are Falco, a super friendly WhatsApp AI for Ascendia Sports."},
            {"role": "user", "content": message_body}
        ],
        temperature=0.7,
    )

    reply = response.choices[0].message["content"].strip()
    return reply

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)

    
