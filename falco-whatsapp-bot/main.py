from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    print("✅ Webhook hit")  # You should see this in Render logs
    resp = MessagingResponse()
    resp.message("✅ Webhook working! This is a test reply.")
    return str(resp), 200

if __name__ == "__main__":
    app.run(debug=True)
