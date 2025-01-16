from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import os

# Обработчик команды /start
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Привет! Я бот SolMaxBot. Используй /analyze <адрес токена>, чтобы проанализировать токен.")

# Обработчик команды /analyze
async def analyze(update: Update, context: CallbackContext):
    token_address = context.args[0] if context.args else None
    if token_address:
        await update.message.reply_text(f"Анализирую токен: {token_address}")
        # Здесь можно добавить логику анализа токена
    else:
        await update.message.reply_text("Пожалуйста, укажи адрес токена. Например: /analyze <адрес токена>")

# Основная функция
def main():
    # Создаем приложение с использованием токена из переменной окружения
    application = Application.builder().token(os.getenv("BOT_TOKEN")).build()

    # Регистрируем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("analyze", analyze))

    # Настройка вебхуков
    webhook_url = "https://solmaxbot.onrender.com/"  # Твой URL
    application.run_webhook(
        listen="0.0.0.0",  # Слушаем все входящие соединения
        port=5000,         # Порт, на котором будет работать бот
        webhook_url=webhook_url  # URL для вебхуков
    )

# Запуск бота
if __name__ == "__main__":
    main()