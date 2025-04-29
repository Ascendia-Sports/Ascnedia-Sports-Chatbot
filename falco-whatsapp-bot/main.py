from flask import Flask, request, Response

app = Flask(__name__)

@app.route("/whatsapp/", methods=["POST"])
def whatsapp_webhook():
    return Response(
        '<?xml version="1.0" encoding="UTF-8"?><Response><Message>✅ Webhook reached! No OpenAI involved.</Message></Response>',
        mimetype="application/xml"
    )
