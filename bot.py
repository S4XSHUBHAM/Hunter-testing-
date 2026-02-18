import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from playwright.async_api import async_playwright

BOT_TOKEN = os.environ.get("BOT_TOKEN")
TARGET_LINK = "https://huntermods.in/Getkey.php"

# Playwright function (same as above)
async def get_vplink_url():
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-dev-shm-usage"]
            )
            page = await browser.new_page()
            
            await page.goto(TARGET_LINK, timeout=60000)
            await page.click("button:has-text('GENERATE INSTANT KEY')")
            await page.wait_for_timeout(8000)
            
            final_url = page.url
            await browser.close()
            return final_url
    except Exception as e:
        print(f"Error: {e}")
        return None

# Message handler (same as above)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    
    if TARGET_LINK in text:
        msg = await update.message.reply_text("🔄 Generating link...")
        
        vplink_url = await get_vplink_url()
        
        if vplink_url:
            await msg.edit_text(f"✅ Your link:\n{vplink_url}")
        else:
            await msg.edit_text("❌ Failed to generate link. Try again.")

# Simple main function
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot is running...")
    app.run_polling()  # directly call karo
