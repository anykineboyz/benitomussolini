from flask import Flask, request
import requests
import os
import re
import random

app = Flask(__name__)

# -----------------------------
# CONFIG
# -----------------------------

BOT_ID = os.environ.get("BOT_ID")

# -----------------------------
# NIKO BANNED WORDS
# -----------------------------

NIKO_ONLY_BANNED_WORDS = [
    "eva",
    "rene",
    "brendon",
    "drill sergeant",
    "clanker",
    "shh",
    "hehe",
    "haha",
    "die",
    "kill",
    "stupid",
    "dumb",
    "mom",
    "dad",
    "shhh",
    "idiot",
    "ass",
    "shut",
    "uncle",
    "aunty",
    "what",
    "no",
    "stop",
    "fine",
    "I",
    "breyden",
    "ej",
    "sidney",
]

# -----------------------------
# STORAGE
# -----------------------------

niko_message_count = 0

# -----------------------------
# SEND MESSAGE
# -----------------------------

def send_message(text):

    if not BOT_ID:
        print("BOT_ID missing")
        return

    try:
        requests.post(
            "https://api.groupme.com/v3/bots/post",
            json={
                "bot_id": BOT_ID,
                "text": text
            },
            timeout=10
        )

    except Exception as error:
        print("Error sending GroupMe message:", error)

# -----------------------------
# WEBHOOK
# -----------------------------

@app.route("/", methods=["POST"])
def webhook():

    global niko_message_count

    data = request.json

    if not data:
        return "ok", 200

    # Ignore bot messages
    if data.get("sender_type") == "bot":
        return "ok", 200

    name = data.get(
        "name",
        "Unknown"
    )

    name_lower = name.lower()

    message = data.get(
        "text",
        ""
    ).strip()

    message_lower = message.lower()

    # -----------------------------
    # ONLY WATCH NIKO
    # -----------------------------

    if "niko" not in name_lower:
        return "ok", 200

    # -----------------------------
    # COUNT NIKO'S MESSAGES
    # -----------------------------

    niko_message_count += 1

    # -----------------------------
    # BANNED WORD CHECK
    # -----------------------------

    for word in NIKO_ONLY_BANNED_WORDS:

        if re.search(
            rf"\b{re.escape(word)}\b",
            message_lower
        ):

            send_message(
                "NIKO, BASTA! GUARDA COME PARLI!"
            )

            break

    # -----------------------------
    # EVERY 3RD MESSAGE
    # -----------------------------

    if niko_message_count % 4 == 0:

        italian_rage_messages = [

            "NIKO!!! ZITTO!!! 🤌",

            "SILENZIO, NIKO!!!",

            "NIKO, SHUSH!!! STAI ZITTO!!!",

            "BASTA!!! NIKO, SILENZIO!!!",

            "NIKO!!! PER FAVORE, ZITTO!!! 😭",

            "SILENZIO!!! NON PARLARE PIÙ!!!",

            "NIKO!!! MA QUANTO PARLI?! ZITTO!!!",

            "BASTA PARLARE, NIKO!!! SILENZIO!!!",

            "NIKO!!! CHIUDI LA BOCCA E FAI SILENZIO!!!",

            "ZITTO!!! ZITTO!!! ZITTO!!! 😭",

            "NIKO, PER L'AMOR DI DIO, SILENZIO!!!",

            "NON VOGLIO SENTIRE UN'ALTRA PAROLA, NIKO!!!",

            "NIKO!!! BASTA CON QUESTI MESSAGGI!!! SILENZIO!!!",

            "SILENZIO, RAGAZZO!!! NON PARLARE!!!",

            "NIKO!!! SMETTILA DI PARLARE!!!",

            "MA NIKO!!! ANCORA?! ZITTO!!!",

            "SILENZIO ASSOLUTO, NIKO!!!",

            "NIKO!!! FAI SILENZIO IMMEDIATAMENTE!!!",

            "BASTA NIKO!!! NON UNA PAROLA DI PIÙ!!!",

            "NIKO!!! ZITTO E CALMATI!!! 🤌"

        ]

        send_message(
            random.choice(
                italian_rage_messages
            )
        )

    return "ok", 200


# -----------------------------
# RUN
# -----------------------------

if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )

    app.run(
        host="0.0.0.0",
        port=port
    )
