import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters,
)
from playwright.async_api import async_playwright

TOKEN = "8563186624:AAF-ib-iPgcWnVt6Fcgj7QsegGeUM57p3sc"
TARGET_LINK = "https://huntermods.in/Getkey.php"


async def bypass_huntermods():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-blink-features=AutomationControlled"
            ]
        )

        page = await browser.new_page()
        await page.goto(TARGET_LINK, timeout=60000)

        await page.wait_for_selector("text=Generate Key", timeout=20000)
        await page.click("text=Generate Key")

        await page.wait_for_timeout(4000)

        vplink = page.url
        await browser.close()
        return vplink


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if TARGET_LINK in text:
        msg = await update.message.reply_text("⏳ Processing...")
        try:
            vplink = await bypass_huntermods()
            await msg.edit_text(vplink)
        except Exception as e:
            await msg.edit_text("❌ Error generating link")


def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()


if __name__ == "__main__":
    main()
