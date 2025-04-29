from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
import os
import time

app = Flask(__name__)

# Set your OpenAI API key (from Render environment variable)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set your assistant ID (from the OpenAI assistant dashboard)
ASSISTANT_ID = "asst_9CH7xxf8x8vPr7m0Jbgr1bcS"

@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    from_number = request.form.get("From", "")
    message_body = request.form.get("Body", "").strip()

    if not message_body:
        resp = MessagingResponse()
        resp.message("Sorry, I didn’t catch that.")
        return str(resp), 200

    try:
        # Create and run thread with assistant
        thread = openai.beta.threads.create()
        run = openai.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=ASSISTANT_ID,
            instructions="Answer like a friendly adventure sports concierge."
        )
        openai.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=message_body
        )

        # Poll until run is complete
        while True:
            status = openai.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            if status.status == "completed":
                break
            time.sleep(1)

        # Fetch latest assistant message
        messages = openai.beta.threads.messages.list(thread_id=thread.id)
        reply = messages.data[0].content[0].text.value.strip()

        # Return via Twilio MessagingResponse
        resp = MessagingResponse()
        resp.message(reply)
        return str(resp), 200

    except Exception as e:
        resp = MessagingResponse()
        resp.message(f"Sorry, something went wrong: {str(e)}")
        return str(resp), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
