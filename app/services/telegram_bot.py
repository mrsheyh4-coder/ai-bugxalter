import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv
from ..agents.orchestrator import BossAgent

load_dotenv()

class TaxTelegramBot:
    """
    AI Buxgalter Telegram Bot.
    Provides mobile access to tax analytics, alerts, and AI chat.
    """
    def __init__(self):
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        self.groq_key = os.getenv("GROQ_API_KEY")
        self.boss_agent = BossAgent(gemini_key=self.gemini_key, groq_key=self.groq_key)

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "Assalomu alaykum! Men AI Buxgalter botiman. 🤖\n\n"
            "Men sizga soliq hisobotlarini tekshirish, yangi stavkalarni aytib berish "
            "va soliq risklarini aniqlashda yordam beraman.\n\n"
            "Boshlash uchun STIRingizni yuboring yoki savol bering."
        )

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_text = update.message.text
        chat_id = str(update.message.chat_id)
        
        # 1. Check if user is entering a 9-digit STIR
        if user_text.isdigit() and len(user_text) == 9:
            context.user_data['pending_stir'] = user_text
            await update.message.reply_text(
                f"STIR {user_text} aniqlandi. ✅\n\n"
                "Xavfsizlik uchun, iltimos, Desktop ilovangizda ko'rsatilgan **6 xonali tasdiqlash kodi**ni kiriting."
            )
            return

        # 2. Check if user is entering a 6-digit verification code
        if user_text.isdigit() and len(user_text) == 6:
            pending_stir = context.user_data.get('pending_stir')
            if not pending_stir:
                await update.message.reply_text("Iltimos, avval STIRingizni kiriting.")
                return
            
            # In a real app, we verify this against the database or cache
            # For the demo, we'll simulate a successful link if the code is correct
            # In production, this would be: if verify_code(pending_stir, user_text):
            await update.message.reply_text(
                f"Tabriklaymiz! 🎉\n\n"
                f"Sizning Telegram hisobingiz STIR {pending_stir} bilan muvaffaqiyatli bog'landi.\n"
                "Endi barcha muhim xabarnomalar shu yerga keladi."
            )
            # Store linking in DB (simulated)
            return

        # 3. General AI Chat
        response = await self.boss_agent.get_tax_consultation(user_text)
        await update.message.reply_text(response['analysis'].get('uzbekistan_law_reference', "Tahlil yakunlandi.") + "\n\n" + response['audit'].get('comments', ""))

    def run(self):
        if not self.token or "your_telegram" in self.token:
            logging.error("Telegram Token topilmadi!")
            return
            
        application = ApplicationBuilder().token(self.token).build()
        
        start_handler = CommandHandler('start', self.start)
        msg_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), self.handle_message)
        
        application.add_handler(start_handler)
        application.add_handler(msg_handler)
        
        print("Telegram Bot ishga tushdi...")
        application.run_polling()

if __name__ == '__main__':
    bot = TaxTelegramBot()
    bot.run()
