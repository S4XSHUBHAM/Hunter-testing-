import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from playwright.async_api import async_playwright

BOT_TOKEN = "8563186624:AAE0ugYSB5CYDnQ51cAQGOgnpKaSDO0olA8"
TARGET_LINK = "https://huntermods.in/Getkey.php"

async def capture_url_after_click():
    print("=" * 50)
    print("DEBUG: Function started")
    
    try:
        async with async_playwright() as p:
            print("DEBUG: Playwright started")
            
            # Browser launch
            browser = await p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-dev-shm-usage"]
            )
            print("DEBUG: Browser launched")
            
            page = await browser.new_page()
            print("DEBUG: New page created")
            
            # Go to page
            print(f"DEBUG: Navigating to {TARGET_LINK}")
            await page.goto(TARGET_LINK, timeout=60000)
            print(f"DEBUG: Page loaded, current URL: {page.url}")
            
            # Get page title
            title = await page.title()
            print(f"DEBUG: Page title: {title}")
            
            # Check if page loaded properly
            content = await page.content()
            print(f"DEBUG: Page content length: {len(content)} characters")
            
            # Find all buttons
            buttons = await page.locator("button").all()
            print(f"DEBUG: Total buttons found: {len(buttons)}")
            
            for i, button in enumerate(buttons):
                text = await button.text_content()
                print(f"DEBUG: Button {i+1} text: '{text}'")
            
            # Try to click button
            print("DEBUG: Attempting to click button...")
            
            button_selectors = [
                "button:has-text('GENERATE INSTANT KEY')",
                "button:has-text('GENERATE')",
                "button:has-text('INSTANT')",
                "button.btn",
                ".btn",
                "button"
            ]
            
            button_clicked = False
            for selector in button_selectors:
                try:
                    count = await page.locator(selector).count()
                    print(f"DEBUG: Selector '{selector}' found {count} elements")
                    
                    if count > 0:
                        await page.click(selector)
                        button_clicked = True
                        print(f"✅ Button clicked with selector: {selector}")
                        break
                except Exception as e:
                    print(f"DEBUG: Selector '{selector}' error: {str(e)}")
                    continue
            
            if not button_clicked:
                print("❌ No button could be clicked")
                
                # Try JavaScript click as last resort
                print("DEBUG: Trying JavaScript click...")
                try:
                    await page.evaluate("""
                        () => {
                            const buttons = document.querySelectorAll('button');
                            for(let btn of buttons) {
                                if(btn.textContent.includes('GENERATE') || btn.textContent.includes('INSTANT')) {
                                    btn.click();
                                    return true;
                                }
                            }
                            return false;
                        }
                    """)
                    print("DEBUG: JavaScript click attempted")
                    button_clicked = True
                except Exception as e:
                    print(f"DEBUG: JavaScript click error: {str(e)}")
            
            # Wait and capture URL
            print("DEBUG: Waiting 5 seconds for any redirect...")
            await page.wait_for_timeout(5000)
            
            current_url = page.url
            print(f"📌 Final URL: {current_url}")
            
            await browser.close()
            print("DEBUG: Browser closed")
            
            print("=" * 50)
            
            if current_url and current_url != TARGET_LINK:
                return current_url
            elif "vplink" in current_url.lower():
                return current_url
            else:
                print("DEBUG: URL didn't change or no VPLink detected")
                return None
            
    except Exception as e:
        print(f"❌ CRITICAL ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Send me the HunterMods link!\n"
        f"`{TARGET_LINK}`",
        parse_mode='Markdown'
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    print(f"📩 Received message: {text}")
    
    if TARGET_LINK in text:
        msg = await update.message.reply_text("🔄 Processing... Check Render logs for details.")
        
        captured_url = await capture_url_after_click()
        
        if captured_url:
            await msg.edit_text(f"✅ Success! URL:\n`{captured_url}`", parse_mode='Markdown')
        else:
            await msg.edit_text(
                "❌ Failed.\n\n"
                "Check Render logs:\n"
                "1. Go to Render Dashboard\n"
                "2. Click on your service\n"
                "3. Click 'Logs' tab\n"
                "4. See DEBUG messages"
            )
    else:
        await update.message.reply_text(f"Send exact link: `{TARGET_LINK}`", parse_mode='Markdown')

if __name__ == "__main__":
    print("🚀 BOT STARTING WITH DEBUG MODE")
    print(f"🤖 Token: {BOT_TOKEN[:10]}...")
    print(f"🎯 Target: {TARGET_LINK}")
    
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("✅ Bot configured, starting polling...")
    app.run_polling()
