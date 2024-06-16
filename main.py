import os
import signal
import email
import requests
from aiosmtpd.controller import Controller
from email import utils

PROGRAM_NAME = "Smtp2Webhook"

WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "")
HOSTNAME = os.environ.get("HOSTNAME", "0.0.0.0")
PORT = os.environ.get("PORT", 8025)

MSG_USERNAME = os.environ.get("MSG_USERNAME", PROGRAM_NAME)


if WEBHOOK_URL == "":
  print("WEBHOOK_URL must be set!")
  exit(1)
else:
  print(f"Forwarding messages to: {WEBHOOK_URL}")


class Smtp2WebhookHandler:
  async def handle_DATA(self, server, session, envelope):
    print(f"Message from {envelope.mail_from}")
    print(f"Message for {envelope.rcpt_tos}")
    print("Message data:")
    msg = email.message_from_bytes(envelope.original_content)
    print(msg)
    print('\nEnd of message')

    print("Forwarding to discord")
    discord_msg = {
        "username": MSG_USERNAME,
        # "content": "\u200b",
        "embeds": [
            {
                "title": msg["Subject"],
                "fields": [
                    {
                        "name": "From:",
                        "value": msg["From"],
                        "inline": "true"
                    },
                    {
                        "name": "To:",
                        "value": "\n".join([address for (_, address) in [utils.parseaddr(x) for x in msg["To"].split(",")]]),
                        "inline": "true"
                    },
                    {
                        "name": "Body",
                        "value": "\n".join([x.get_payload() for x in msg.walk() if x.get_content_type() == "text/plain"])
                    }
                ],
                "footer": {
                    "text": f"Forwarded by {PROGRAM_NAME}"
                },
                "timestamp": utils.parsedate_to_datetime(msg["Date"]).isoformat()
            }
        ]
    }
    resp = requests.post(url=WEBHOOK_URL, json=discord_msg)
    print(f"Discord responded with: {resp.status_code} {resp.content}")
    return "250 Message accepted for delivery"


def signal_handler(sig, frame):
  print(f"CTRL+C received, closing {PROGRAM_NAME}...")
  controller.stop()
  exit(0)


signal.signal(signal.SIGINT, signal_handler)

controller = Controller(Smtp2WebhookHandler(), hostname=HOSTNAME, port=PORT)
controller.start()
print(f"{PROGRAM_NAME} is running, press CTRL+C to stop the server")
signal.pause()
