import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from playwright.async_api import async_playwright

TOKEN = "8563186624:AAF-ib-iPgcWnVt6Fcgj7QsegGeUM57p3sc"
TARGET = "https://huntermods.in/Getkey.php"


async def bypass_huntermods():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )
        page = await browser.new_page()

        vplink = None

        async def handle_response(response):
            nonlocal vplink
            url = response.url
            if "vplink" in url or "vplinks" in url:
                vplink = url

        page.on("response", handle_response)

        await page.goto(TARGET, timeout=60000)
        await page.wait_for_timeout(5000)

        # try clicking button if exists
        try:
            await page.click("button", timeout=3000)
            await page.wait_for_timeout(5000)
        except:
            pass

        await browser.close()

        if not vplink:
            raise Exception("VPlink not found")

        return vplink


async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if TARGET in text:
        msg = await update.message.reply_text("⏳ Processing...")
        try:
            link = await bypass_huntermods()
            await msg.edit_text(link)
        except Exception as e:
            await msg.edit_text("❌ Error generating link")


def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handler))
    app.run_polling()


if __name__ == "__main__":
    main()
