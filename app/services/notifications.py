import httpx
import os
from dotenv import load_dotenv

load_dotenv()

class TelegramService:
    def __init__(self):
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.base_url = f"https://api.telegram.org/bot{self.token}"

    async def send_message(self, chat_id: str, text: str):
        if not self.token:
            print("Telegram token not set, skipping message.")
            return
            
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/sendMessage",
                    json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
                )
                return response.json()
            except Exception as e:
                print(f"Failed to send Telegram message: {e}")
                return None

    async def send_alert(self, chat_id: str, company_name: str, alert_type: str, message: str):
        text = f"🚨 *{alert_type} ALERT* for {company_name}\n\n{message}"
        return await self.send_message(chat_id, text)

notification_service = TelegramService()
