import os
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext
from solana.rpc.api import Client

# Инициализация Flask-приложения
app = Flask(__name__)

# Обработчик для GET-запросов
@app.route('/')
def wake_up():
    return "Bot is awake!", 200

# Обработчик команды /start
async def start_command(update: Update, context: CallbackContext):
    await update.message.reply_text("Привет! Я бот для анализа токенов Solana. Используй /help, чтобы узнать доступные команды.")

# Обработчик команды /help
async def help_command(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "Доступные команды:\n"
        "/start - Начать работу с ботом\n"
        "/analyze <адрес токена> - Проанализировать токен\n"
        "/balance <адрес кошелька> - Проверить баланс кошелька\n"
        "/help - Показать это сообщение"
    )

# Обработчик команды /balance
async def balance_command(update: Update, context: CallbackContext):
    wallet_address = context.args[0] if context.args else None
    if wallet_address:
        client = Client("https://api.mainnet-beta.solana.com")
        try:
            balance = client.get_balance(wallet_address)["result"]["value"]
            await update.message.reply_text(f"Баланс кошелька {wallock_address}: {balance / 1e9} SOL")
        except Exception as e:
            await update.message.reply_text(f"Ошибка: {e}")
    else:
        await update.message.reply_text("Пожалуйста, укажи адрес кошелька. Например: /balance <адрес кошелька>")

# Основная функция для запуска бота и Flask-сервера
def main():
    # Инициализация Telegram бота
    application = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()

    # Регистрация обработчиков команд
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("balance", balance_command))

    # Запуск Flask-сервера для обработки GET-запросов
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 5000)))

    # Запуск Telegram бота
    application.run_polling()

if __name__ == "__main__":
    main()