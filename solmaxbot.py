from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import os

# Обработчик команды /start
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Привет! Я бот SolMaxBot. Используй /help, чтобы узнать доступные команды.")

# Обработчик команды /analyze
async def analyze(update: Update, context: CallbackContext):
    token_address = context.args[0] if context.args else None
    if token_address:
        await update.message.reply_text(f"Анализирую токен: {token_address}")
    else:
        await update.message.reply_text("Пожалуйста, укажи адрес токена. Например: /analyze <адрес токена>")

# Обработчик команды /help
async def help_command(update: Update, context: CallbackContext):
    help_text = """
Доступные команды:
/start - Начать работу с ботом
/analyze <адрес токена> - Проанализировать токен
/balance <адрес кошелька> - Проверить баланс кошелька
/help - Показать это сообщение
    """
    await update.message.reply_text(help_text)

# Основная функция
def main():
    # Создаем приложение с использованием токена из переменной окружения
    application = Application.builder().token(os.getenv("BOT_TOKEN")).build()

    # Регистрируем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("analyze", analyze))
    application.add_handler(CommandHandler("help", help_command))

    # Настройка вебхуков
    webhook_url = "https://solmaxbot.onrender.com/"  # Убедись, что URL правильный
    application.run_webhook(
        listen="0.0.0.0",  # Слушаем все входящие соединения
        port=int(os.getenv("PORT", 5000)),  # Используем порт из переменной окружения
        webhook_url=webhook_url  # URL для вебхуков
    )

# Запуск бота
if __name__ == "__main__":
    main()