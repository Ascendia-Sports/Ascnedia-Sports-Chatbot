from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    resp = MessagingResponse()
    resp.message("Hi! You reached the webhook 🎯")
    return str(resp), 200

if __name__ == "__main__":
    app.run(debug=True)
