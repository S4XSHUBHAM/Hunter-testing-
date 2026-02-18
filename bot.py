import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from playwright.async_api import async_playwright

BOT_TOKEN = os.environ.get("BOT_TOKEN")
TARGET_LINK = "https://huntermods.in/Getkey.php"

async def get_vplink_url():
    browser = None
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-dev-shm-usage"]
            )
            page = await browser.new_page()
            
            # Step 1: Go to page
            print("Step 1: Navigating to target...")
            response = await page.goto(TARGET_LINK, timeout=60000, wait_until='domcontentloaded')
            print(f"Page status: {response.status if response else 'No response'}")
            
            # Step 2: Check page title/content
            title = await page.title()
            print(f"Page title: {title}")
            
            # Step 3: Find button
            button_exists = await page.locator("button:has-text('GENERATE INSTANT KEY')").count()
            print(f"Button found: {button_exists > 0}")
            
            if button_exists == 0:
                # Try alternative button selectors
                button_exists = await page.locator("button:has-text('GENERATE')").count()
                print(f"Alternative button found: {button_exists > 0}")
            
            # Step 4: Click button
            print("Step 4: Clicking button...")
            await page.click("button:has-text('GENERATE INSTANT KEY')")
            
            # Step 5: Wait for redirect
            print("Step 5: Waiting for redirect...")
            await page.wait_for_timeout(10000)  # 10 seconds wait
            
            # Step 6: Get URL
            final_url = page.url
            print(f"Step 6: Final URL = {final_url}")
            
            # Step 7: Check if redirected
            if final_url != TARGET_LINK:
                print("✓ Redirect successful!")
                await browser.close()
                return final_url
            else:
                print("✗ No redirect occurred")
                await browser.close()
                return None
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        if browser:
            await browser.close()
        return None

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    print(f"Received message: {text}")
    
    if TARGET_LINK in text:
        msg = await update.message.reply_text("🔄 Generating link... (checking...)")
        
        vplink_url = await get_vplink_url()
        
        if vplink_url:
            await msg.edit_text(f"✅ Your link:\n{vplink_url}")
        else:
            await msg.edit_text("❌ Failed to generate link. Check Render logs for details.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot is running...")
    app.run_polling()
