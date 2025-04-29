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
        return "No message received", 400

    try:
        # Call the assistant via OpenAI API
        response = openai.beta.threads.create_and_run(
            assistant_id=ASSISTANT_ID,
            thread={"messages": [{"role": "user", "content": message_body}]}
        )

        # Wait for completion
        run_id = response["id"]
        thread_id = response["thread_id"]

        while True:
            run_status = openai.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
            if run_status.status == "completed":
                break
            time.sleep(0.5)  # Avoid hammering the API

        # Get the assistant's reply
        messages = openai.beta.threads.messages.list(thread_id=thread_id)
        assistant_reply = messages.data[0].content[0].text.value.strip()

        # Respond via WhatsApp
        resp = MessagingResponse()
        resp.message(assistant_reply)
        return str(resp), 200

    except Exception as e:
        resp = MessagingResponse()
        resp.message(f"Sorry, something went wrong: {str(e)}")
        return str(resp), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
