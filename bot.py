import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from playwright.async_api import async_playwright

BOT_TOKEN = "8563186624:AAE0ugYSB5CYDnQ51cAQGOgnpKaSDO0olA8"
TARGET_LINK = "https://huntermods.in/Getkey.php"

async def capture_url_on_click():
    try:
        async with async_playwright() as p:
            # Browser launch
            browser = await p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-dev-shm-usage"]
            )
            
            page = await browser.new_page()
            
            print("🔍 Opening HunterMods page...")
            await page.goto(TARGET_LINK, timeout=60000)
            
            # Page load complete hone do
            await page.wait_for_load_state("networkidle")
            
            # Network requests monitor karo
            async def handle_response(response):
                if "vplink" in response.url.lower() or "redirect" in response.url.lower():
                    print(f"📡 Network response URL: {response.url}")
            
            page.on("response", handle_response)
            
            # Button click se pehle ka URL
            print(f"📌 URL before click: {page.url}")
            
            # Button click karo
            print("🖱️ Clicking GENERATE INSTANT KEY button...")
            
            # Button click
            button_selectors = [
                "button:has-text('GENERATE INSTANT KEY')",
                "button:has-text('GENERATE')",
                "button.btn",
                ".btn",
                "button"
            ]
            
            for selector in button_selectors:
                try:
                    if await page.locator(selector).count() > 0:
                        await page.click(selector)
                        print(f"✅ Button clicked with selector: {selector}")
                        break
                except:
                    continue
            
            # IMPORTANT: Button click ke turant baad URL capture
            await page.wait_for_timeout(2000)  # 2 second wait for any immediate redirect
            
            # Jo bhi current URL ho, capture karo
            current_url = page.url
            print(f"📌 URL after click: {current_url}")
            
            # Browser band karo
            await browser.close()
            
            # Agar current URL same nahi hai original se, to return karo
            if current_url != TARGET_LINK:
                return current_url
            else:
                return None
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome! Send me this link:\n"
        f"`{TARGET_LINK}`\n\n"
        "I'll capture the URL after button click.",
        parse_mode='Markdown'
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    
    if TARGET_LINK in text:
        msg = await update.message.reply_text("🔄 Capturing URL after button click...")
        
        captured_url = await capture_url_on_click()
        
        if captured_url:
            await msg.edit_text(
                f"✅ URL captured after click:\n`{captured_url}`\n\n"
                f"🔗 Original: `{TARGET_LINK}`",
                parse_mode='Markdown'
            )
        else:
            await msg.edit_text("❌ Failed to capture URL. No redirect occurred.")
    else:
        await update.message.reply_text(f"Please send the exact link: `{TARGET_LINK}`", parse_mode='Markdown')

async def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🤖 Bot starting...")
    print("✅ Bot is ready!")
    
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
