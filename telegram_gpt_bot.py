import logging
import threading
import asyncio
import tkinter as tk
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI, OpenAIError

# --- Токени ---
TELEGRAM_BOT_TOKEN = "your_telegram_bot_token"
OPENAI_API_KEY = "your_openrouter_api_key"

# --- OpenRouter клієнт ---
client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

# --- GUI для логів ---
class LogWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Telegram GPT Логи")
        self.root.geometry("700x500")
        self.text = tk.Text(self.root, wrap="word", state="disabled", bg="#1e1e1e", fg="#00ff00", font=("Consolas", 11))
        self.text.pack(fill="both", expand=True)

    def log(self, message: str):
        self.text.config(state="normal")
        self.text.insert(tk.END, message + "\n")
        self.text.see(tk.END)
        self.text.config(state="disabled")

    def start(self):
        self.root.mainloop()

log_window = LogWindow()

# --- Обробка команд ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Привіт! Я бот GPT. Напиши щось або скористайся командою /code для генерації коду.")

# --- Основна логіка відповіді ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.strip()
    user_name = update.effective_user.username or update.effective_user.first_name

    log_window.log(f"[{user_name}] написав: {user_text}")

    # --- Логіка генерації коду ---
    is_code_request = user_text.lower().startswith("напиши код") or user_text.lower().startswith("/code")

    prompt = user_text
    if is_code_request:
        prompt = f"Напиши код: {user_text.replace('/code', '').strip()}"

    try:
        response = client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300 if is_code_request else 150,  # Більше для коду
            temperature=0.5
        )
        answer = response.choices[0].message.content
    except OpenAIError as e:
        error_text = f"❌ Помилка API: {e}"
        log_window.log(error_text)
        await update.message.reply_text("⚠️ Сталася помилка при зверненні до GPT. Спробуйте пізніше.")
        return

    log_window.log(f"[GPT] відповів: {answer}")
    await update.message.reply_text(answer)

# --- Запуск бота у потоці ---
def run_bot():
    asyncio.set_event_loop(asyncio.new_event_loop())
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ Бот запущений...")
    app.run_polling()

# --- Старт ---
if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    log_window.start()
