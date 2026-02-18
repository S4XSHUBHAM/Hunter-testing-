import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from playwright.async_api import async_playwright

BOT_TOKEN = os.environ.get("BOT_TOKEN")
TARGET_LINK = "https://huntermods.in/Getkey.php"

async def get_vplink_url():
    try:
        async with async_playwright() as p:
            # Browser launch
            browser = await p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-dev-shm-usage"]
            )
            
            page = await browser.new_page()
            
            # 1. HunterMods page par jao
            await page.goto(TARGET_LINK, timeout=60000)
            
            # 2. Button click karo - exact text match
            await page.click("button:has-text('GENERATE INSTANT KEY')")
            
            # 3. Redirect hone do (VPLink par pahunchne tak)
            await page.wait_for_timeout(8000)  # 8 second wait
            
            # 4. Final URL lo
            final_url = page.url
            await browser.close()
            
            # 5. Sirf URL return karo, koi condition nahi
            return final_url
            
    except Exception as e:
        print(f"Error: {e}")
        return None

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    
    if TARGET_LINK in text:
        msg = await update.message.reply_text("🔄 Generating link...")
        
        vplink_url = await get_vplink_url()
        
        if vplink_url:
            await msg.edit_text(f"✅ Your link:\n{vplink_url}")
        else:
            await msg.edit_text("❌ Failed to generate link. Try again.")

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot is running...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
