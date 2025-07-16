from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import asyncio
import re
import time

WATCH_DURATION = 60  # seconds

# Your Telegram bot token
BOT_TOKEN = "7562538667:AAGi_PthWGsUDF-69xetHSaV5GhG_DgIcpM"

# Regex to validate Terabox video link
TERABOX_REGEX = r'https?://(www\.)?(terabox|4funbox)\.com/s/[a-zA-Z0-9]+'

# Function to simulate watching video
def watch_terabox_video(url: str):
    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = uc.Chrome(options=options)
    driver.get(url)
    time.sleep(10)  # Wait for page load

    try:
        # Click Play
        play_button = driver.find_element(By.XPATH, '//button[contains(@class,"play-button")]')
        play_button.click()
    except:
        pass

    time.sleep(WATCH_DURATION)
    driver.quit()


# Handle any incoming message
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text
    chat_id = update.effective_chat.id

    match = re.search(TERABOX_REGEX, msg)
    if match:
        video_url = match.group(0)
        await update.message.reply_text("🎬 Watching your video...")

        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, watch_terabox_video, video_url)

        await update.message.reply_text("✅ Done watching the video!")
    else:
        await update.message.reply_text("❌ Please send a valid Terabox video link.")


# Run the bot
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("🤖 Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()