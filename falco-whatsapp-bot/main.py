from flask import Flask, request, Response
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/whatsapp/", methods=["POST"])
def whatsapp_webhook():
    resp = MessagingResponse()
    resp.message("✅ Webhook reached! No OpenAI involved.")
    return Response(str(resp), mimetype="application/xml")

if __name__ == "__main__":
    app.run()
