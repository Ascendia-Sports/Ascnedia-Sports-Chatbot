from flask import Flask, request, Response
from twilio.twiml.messaging_response import MessagingResponse
import openai
import os
import time

app = Flask(__name__)

# Set your OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set your Assistant ID
ASSISTANT_ID = "asst_9CH7xxf8x8vPr7m0Jbgr1bcS"

@app.route("/whatsapp/", methods=["POST"])
def whatsapp_webhook():
    from_number = request.form.get("From", "")
    message_body = request.form.get("Body", "").strip()

    if not message_body:
        return Response("No message received", status=400)

    try:
        # Create a new thread and run the assistant
        response = openai.beta.threads.create_and_run(
            assistant_id=ASSISTANT_ID,
            thread={"messages": [{"role": "user", "content": message_body}]}
        )

        run_id = response["id"]
        thread_id = response["thread_id"]

        # Poll until the run is completed
        while True:
            run_status = openai.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
            if run_status.status == "completed":
                break
            time.sleep(0.5)  # Avoid excessive polling

        # Retrieve the assistant's reply
        messages = openai.beta.threads.messages.list(thread_id=thread_id)
        assistant_reply = messages.data[0].content[0].text.value.strip()

        # Create a TwiML response
        resp = MessagingResponse()
        resp.message(assistant_reply)
        return Response(str(resp), mimetype="application/xml")

    except Exception as e:
        # Handle exceptions and respond with an error message
        resp = MessagingResponse()
        resp.message(f"Sorry, something went wrong: {str(e)}")
        return Response(str(resp), mimetype="application/xml", status=500)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
