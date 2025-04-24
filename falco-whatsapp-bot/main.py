from flask import Flask, request
import openai
import os

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    # Get the incoming message from the user
    from_number = request.form.get("From", "")
    message_body = request.form.get("Body", "").strip()

    # If there's no message body, return an error
    if not message_body:
        return "No message received", 400

    # Simulate typing delay and process the user’s message with OpenAI
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Or any other model you'd like to use
        messages=[
            {"role": "user", "content": message_body},  # Just the user's input
        ],
        temperature=0.7,  # Controls response creativity
    )

    # Get the reply from the OpenAI API
    reply = response.choices[0].message["content"].strip()

    return reply

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
