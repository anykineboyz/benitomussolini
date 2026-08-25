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
    "fine"
]

# -----------------------------
# STORAGE
# -----------------------------

niko_message_count = 0

# -----------------------------
# UNCLE SAM MESSAGES
# -----------------------------

uncle_sam_messages = [

    "Niko, please calm down. The American people are watching. 🇺🇸",

    "Niko, this is your friendly reminder from Uncle Sam: stop yapping ",

    "Niko, the Department of GroupMe Affairs has received several complaints about you.",

    "Niko, please remain calm. We are currently monitoring the situation.",

    "Uncle Sam says: Niko, put the phone down. You've done enough.",

    "Niko, your recent activity has raised some concerns at the federal level ",

    "Niko, we regret to inform you that your yapping privileges are under review.",

    "Attention Niko: the United States has had enough of this nonsense 🇺🇸",

    "Niko, this is your second warning from the completely real Department of Yapping.",

    "Niko, the government has reviewed your messages. We are disappointed.",

    "Uncle Sam has entered the chat. Niko, you need to relax.",

    "Niko, please stop before we have to involve the Department of Homeland Yapping.",

    "Niko, your message count has been classified as excessive.",

    "The United States respectfully asks Niko to shut it down for a minute.",

    "Niko, we have been informed of your activities. Unfortunately, we cannot ignore them any longer.",

    "Niko, the Constitution does not protect this level of yapping ",

    "Uncle Sam says you've had enough screen time, Niko.",

    "Niko, this is a courtesy notification. Please stop being a menace.",

    "Niko, your yapping has officially become a national security concern 🇺🇸",

    "Niko, the American people would like some peace and quiet.",

    "Niko, please cooperate with federal authorities and stop sending so many messages.",

    "We have reviewed the evidence, Niko. You are, in fact, yapping.",

    "Niko, Uncle Sam is disappointed. Please do better.",

    "Niko, you have been placed on the federal watchlist for excessive GroupMe activity ",

    "Niko, this is not a drill. Actually, it kind of is. Just stop talking.",

    "The Department of Homeland Yapping has officially opened a case on Niko.",

    "Niko, you have 10 seconds to explain yourself. Actually, never mind. Be quiet.",

    "Niko, America needs you to chill out 🇺🇸",

    "Your cooperation is appreciated, Niko. Your silence would be appreciated even more.",

    "Niko, we fought for freedom, not for you to send 47 messages in a row "

]
]

# -----------------------------
# SEND MESSAGE
# -----------------------------

def send_message(text):

    if not BOT_ID:
        print("BOT_ID missing")
        return

    try:
        response = requests.post(
            "https://api.groupme.com/v3/bots/post",
            json={
                "bot_id": BOT_ID,
                "text": text
            },
            timeout=10
        )

        print(
            "GroupMe response:",
            response.status_code
        )

    except Exception as error:
        print(
            "Error sending GroupMe message:",
            error
        )

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

    if "niko" not in name_lower and "itachi" not in name_lower:
        return "ok", 200

    # -----------------------------
    # COUNT NIKO'S MESSAGES
    # -----------------------------

    niko_message_count += 1

    print(
        f"Niko message #{niko_message_count}"
    )

    # -----------------------------
    # NIKO BANNED WORD CHECK
    # -----------------------------

    for word in NIKO_ONLY_BANNED_WORDS:

        if re.search(
            rf"\b{re.escape(word)}\b",
            message_lower
        ):

            send_message(
                "NIKO. THIS LANGUAGE HAS BEEN NOTED. PLEASE COMPLY WITH GROUP CHAT REGULATIONS."
            )

            break

    # -----------------------------
    # EVERY 8TH MESSAGE
    # -----------------------------

    if niko_message_count % 8 == 0:

        send_message(
            random.choice(
                uncle_sam_messages
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
