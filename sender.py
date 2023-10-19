import os, asyncio, emoji
from pyrogram import Client
from datetime import datetime
# take environment variables from .env
from dotenv import load_dotenv
load_dotenv() 


# Telegram data
session_name = os.getenv('SESSION_NAME') # str
api_id = os.getenv('API_ID') # int
api_hash = os.getenv('API_HASH') # str
bot_token = os.getenv('BOT_TOKEN') # str

def send_messages(recipients, messages, channel_name):
    # If there are new messages send them
    if len(messages) > 0:
        # convert str with recipients in to list
        recipients = recipients.split(" ")

        try:
            app = Client(
                session_name,
                api_id = api_id,
                api_hash = api_hash,
                bot_token = bot_token
            )


            for recipient in recipients:
                recipient = int(recipient)
                async def main():
                    async with app:
                        for message in messages:
                            await app.send_message(
                                recipient,
                                message, 
                                disable_web_page_preview=True
                            )

                        now = datetime.now()
                        last_check = now.strftime("%H:%M / %d.%m.%Y")
                        time_icon = emoji.emojize(":hourglass_not_done:")

                        await app.set_chat_description(
                            recipient,
                            f"{channel_name}\nLast update: {last_check}"
                        )
                app.run(main())

        except Exception as e:
            print(e)

    else:
        try:
            app = Client(
                session_name,
                api_id = api_id,
                api_hash = api_hash,
                bot_token = bot_token
            )

            now = datetime.now()
            last_check = now.strftime("%H:%M / %d.%m.%Y")
            time_icon = emoji.emojize(":hourglass_not_done:")

            for recipient in recipients:
                async def main():
                    async with app:
                        await app.set_chat_description(
                            recipient,
                            f"{channel_name}\nLast update: {last_check}"
                        )
                app.run(main())

        except Exception as e:
            print(e)
