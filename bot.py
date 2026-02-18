import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from playwright.sync_api import sync_playwright

# Render ENV variable se token lo (secure)
BOT_TOKEN = os.environ.get("8563186624:AAF-ib-iPgcWnVt6Fcgj7QsegGeUM57p3sc")


def huntermods_bypass():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-blink-features=AutomationControlled"
            ]
        )

        page = browser.new_page()
        page.goto("https://huntermods.in/Getkey.php", timeout=60000)

        page.wait_for_selector("text=Generate Key", timeout=15000)
        page.click("text=Generate Key")

        page.wait_for_timeout(4000)

        vplink = page.url
        browser.close()
        return vplink


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome!\n\n"
        "🔑 Key generate karne ke liye command use karo:\n"
        "/key"
    )


async def key_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = await update.message.reply_text("⏳ Generate ho rahi hai, wait karo...")

    try:
        link = huntermods_bypass()
        await msg.edit_text(f"✅ **VPLINK FOUND**\n\n{link}", parse_mode="Markdown")
    except Exception as e:
        await msg.edit_text(f"❌ Error:\n{e}")


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("key", key_command))

    print("🤖 Bot running on Render...")
    app.run_polling()


if __name__ == "__main__":
    main()