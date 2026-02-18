import os
import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    filters,
)
from playwright.async_api import async_playwright

BOT_TOKEN = os.environ.get("BOT_TOKEN")  # Render ENV me set karo

TARGET_LINK = "https://huntermods.in/Getkey.php"


async def generate_vplink():
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,  # Render ke liye TRUE (limitation)
                args=[
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-blink-features=AutomationControlled"
                ]
            )

            context = await browser.new_context(
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                )
            )

            page = await context.new_page()
            await page.goto(TARGET_LINK, timeout=60000)

            # button wait + click
            await page.wait_for_selector("button", timeout=15000)
            await page.click("button")

            # redirect ka wait
            await page.wait_for_timeout(8000)

            final_url = page.url
            await browser.close()

            if "vplink" in final_url.lower():
                return final_url
            else:
                return None

    except Exception as e:
        print("Playwright error:", e)
        return None


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if TARGET_LINK in text:
        msg = await update.message.reply_text("🔄 Generating link, please wait...")

        link = await generate_vplink()

        if link:
            await msg.edit_text(f"✅ Your link:\n{link}")
        else:
            await msg.edit_text(
                "❌ Error generating link\n\n"
                "⚠️ Note: Render / headless environment me "
                "HunterMods bypass block hota hai."
            )


async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    print("Bot started...")
    await app.run_polling()


if __name__ == "__main__":
    asyncio.run(main())
