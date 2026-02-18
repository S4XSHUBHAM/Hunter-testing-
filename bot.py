import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from playwright.async_api import async_playwright

BOT_TOKEN = "8563186624:AAE0ugYSB5CYDnQ51cAQGOgnpKaSDO0olA8"
TARGET_LINK = "https://huntermods.in/Getkey.php"

async def capture_url_on_click():
    """Button click ke turant baad URL capture karo"""
    try:
        async with async_playwright() as p:
            # Browser launch
            browser = await p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-dev-shm-usage"]
            )
            
            page = await browser.new_page()
            
            # Navigate to target
            await page.goto(TARGET_LINK, timeout=60000, wait_until='domcontentloaded')
            
            # Take current URL before click
            before_click_url = page.url
            print(f"📌 Before click: {before_click_url}")
            
            # Method 1: Try exact button text
            button_found = False
            
            # Try multiple selectors
            selectors = [
                "button:has-text('GENERATE INSTANT KEY')",
                "button:has-text('GENERATE')",
                "button:has-text('INSTANT')",
                "button.btn",
                ".btn-primary",
                "button[type='submit']",
                "button"
            ]
            
            for selector in selectors:
                try:
                    if await page.locator(selector).count() > 0:
                        await page.click(selector)
                        print(f"✅ Clicked with: {selector}")
                        button_found = True
                        break
                except:
                    continue
            
            # Method 2: If above fails, try JavaScript click
            if not button_found:
                print("⚠️ Trying JavaScript click...")
                await page.evaluate("""
                    () => {
                        const buttons = document.querySelectorAll('button');
                        for(let btn of buttons) {
                            if(btn.textContent.includes('GENERATE') || 
                               btn.textContent.includes('INSTANT') ||
                               btn.textContent.includes('KEY')) {
                                btn.click();
                                return true;
                            }
                        }
                        return false;
                    }
                """)
            
            # IMPORTANT: Thoda sa wait karo redirect capture karne ke liye
            await page.wait_for_timeout(3000)  # 3 seconds wait
            
            # Capture URL after click
            after_click_url = page.url
            print(f"📌 After click: {after_click_url}")
            
            await browser.close()
            
            # Agar URL change hua hai to return karo
            if after_click_url != before_click_url:
                return after_click_url
            return after_click_url  # Agar change na bhi ho to bhi return karo
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Send the HunterMods link:\n"
        f"`{TARGET_LINK}`",
        parse_mode='Markdown'
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    
    if TARGET_LINK in text:
        msg = await update.message.reply_text("🔄 Clicking button and capturing URL...")
        
        captured_url = await capture_url_on_click()
        
        if captured_url:
            await msg.edit_text(f"✅ URL after click:\n`{captured_url}`", parse_mode='Markdown')
        else:
            await msg.edit_text("❌ Failed to capture URL")
    else:
        await update.message.reply_text(f"Send exact link: `{TARGET_LINK}`", parse_mode='Markdown')

# 🔥 SIMPLE AND CORRECT WAY TO RUN
if __name__ == "__main__":
    print("🤖 Bot starting...")
    
    # Direct application banayo
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Handlers add karo
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("✅ Bot is ready! Send /start")
    
    # SIRF ye line - asyncio.run() nahi, direct run_polling()
    app.run_polling()
