from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import requests

# Токен бота
BOT_TOKEN = "7794847751:AAEaY5MTQIFvGCev6xn69iDEF22Fwx-Mp90"

# Обработчик для команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Привет! Я SolMaxBot, готов помочь с анализом токенов 🚀.")

# Обработчик для команды /analyze
async def analyze(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        # Получаем адрес токена из сообщения пользователя
        token_address = context.args[0] if context.args else None
        if not token_address:
            await update.message.reply_text("Пожалуйста, укажи адрес токена. Например: /analyze <адрес токена>")
            return

        # Запрос к API DexScreener
        url = f"https://api.dexscreener.io/latest/dex/tokens/{token_address}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            # Пример вывода данных
            pair = data['pairs'][0]  # Берем первую пару
            message = (
                f"📊 Анализ токена:\n"
                f"Название: {pair['baseToken']['name']} ({pair['baseToken']['symbol']})\n"
                f"Цена: ${pair['priceUsd']}\n"
                f"Объем торгов (24ч): ${pair['volume']['h24']}\n"
                f"Ликвидность: ${pair['liquidity']['usd']}"
            )
            await update.message.reply_text(message)
        else:
            await update.message.reply_text("Не удалось получить данные о токене. Проверь адрес и попробуй снова.")
    except Exception as e:
        await update.message.reply_text(f"Произошла ошибка: {e}")

# Обработчик для команды /balance
async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Баланс вашего кошелька: 0 SOL (тестовые данные).")

# Основная функция для запуска бота
def main() -> None:
    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()

    # Регистрация команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("analyze", analyze))
    application.add_handler(CommandHandler("balance", balance))

    # Запуск бота
    print("Bot is running... Press Ctrl+C to stop.")
    application.run_polling()

if __name__ == "__main__":
    main()