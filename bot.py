import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from playwright.async_api import async_playwright

# Naya token - isko bar-bar change mat karo, bas Render pe service delete karo
BOT_TOKEN = "8563186624:AAE0ugYSB5CYDnQ51cAQGOgnpKaSDO0olA8"
TARGET_LINK = "https://huntermods.in/Getkey.php"

async def capture_url():
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-dev-shm-usage"]
            )
            page = await browser.new_page()
            
            # Page load
            await page.goto(TARGET_LINK, timeout=60000)
            
            # Button click - exact text match
            await page.click("button:has-text('GENERATE INSTANT KEY')")
            
            # Thoda wait karo redirect ke liye
            await page.wait_for_timeout(5000)
            
            # URL capture
            final_url = page.url
            await browser.close()
            return final_url if final_url != TARGET_LINK else None
            
    except Exception as e:
        print(f"Error: {e}")
        return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Send this link:\n`{TARGET_LINK}`", parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if TARGET_LINK in update.message.text:
        msg = await update.message.reply_text("🔄 Generating...")
        url = await capture_url()
        if url:
            await msg.edit_text(f"✅ {url}")
        else:
            await msg.edit_text("❌ Failed")

if __name__ == "__main__":
    print("🤖 Bot starting...")
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ Bot is running!")
    app.run_polling()
