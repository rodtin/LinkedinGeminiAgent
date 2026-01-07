import os
import asyncio
import schedule
import time
import threading
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# Import engines
from news_engine import run_daily_search
from content_engine import generate_draft

# Import existing application (needs refactoring of post_linkedin.py for clean import)
import sys
# Add parent dir to path so we can import Application
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Application import post_linkedin

# Load env from Docker path or local
load_dotenv(dotenv_path="../Application/.env.docker")
load_dotenv(dotenv_path="../Application/.env") # Fallback/Override

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TARGET_CHAT_ID = None # Will store after first interaction or hardcode if known

# State
current_report_path = None
current_draft_path = None
current_draft_text = None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global TARGET_CHAT_ID
    TARGET_CHAT_ID = update.effective_chat.id
    await update.message.reply_text(f"👋 Operations Online.\nChat ID: {TARGET_CHAT_ID}\n\nI will run daily at 08:00 AM.\nUse /search <trends> to trigger manually.")

async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    topics = context.args
    if not topics:
        await update.message.reply_text("Usage: /search telecom, ai, cloud")
        return

    await update.message.reply_text(f"🔎 Starting Deep Dive on: {topics}...")
    
    # Run in thread to not block bot
    loop = asyncio.get_event_loop()
    try:
        report_path = await loop.run_in_executor(None, run_daily_search, topics)
        
        global current_report_path
        current_report_path = report_path
        
        with open(report_path, "r", encoding="utf-8") as f:
            content = f.read(4000) # Truncate for Telegram limit
            
        await update.message.reply_text(f"✅ **Report Ready!**\n\n{content}...\n\n(Full report saved to disk)")
        await update.message.reply_text("To draft a post, reply with:\n'Draft <selection> [mode]'\n\nExamples:\n- `Draft Story 1`\n- `Draft AI-RAN direct`\n- `Draft Story 3 strategist`")
        
    except Exception as e:
        await update.message.reply_text(f"❌ Error during search: {e}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    global current_draft_path, current_draft_text
    
    if text.lower().startswith("draft "):
        # Parse command: Draft <selection> [mode] [lens]
        parts = text.split(" ")
        selection = parts[1] if len(parts) > 1 else "General"
        mode = "persona"
        lens = "all"
        
        if "direct" in text.lower(): mode = "direct"
        if "strategist" in text.lower(): lens = "strategist"
        # ... other lenses logic ...

        if not current_report_path:
            await update.message.reply_text("⚠️ No report available. Run /search first.")
            return

        await update.message.reply_text(f"✍️ Drafting post for '{selection}' (Mode: {mode}, Lens: {lens})...")
        
        try:
            loop = asyncio.get_event_loop()
            path, content = await loop.run_in_executor(None, generate_draft, current_report_path, selection, mode, lens)
            
            current_draft_path = path
            current_draft_text = content
            
            await update.message.reply_text(f"📝 **Draft Preview:**\n\n{content}")
            await update.message.reply_text("Reply 'APPROVE' to publish to LinkedIn, or reply with feedback/edits.")
            
        except Exception as e:
            await update.message.reply_text(f"❌ Drafting failed: {e}")
            
    elif text.upper() == "APPROVE":
        if not current_draft_path:
            await update.message.reply_text("⚠️ No active draft to approve.")
            return
            
        await update.message.reply_text("🚀 Publishing to LinkedIn...")
        try:
            # Call the post_linkedin module
            # We need to set the env vars for it if they aren't loaded in that module's context
            # (Done via dotenv above, but good to be sure)
            
            # Since post_linkedin.py prints to stdout, capture it? 
            # Ideally refactor post_linkedin to return status.
            
            loop = asyncio.get_event_loop()
            # Run the post function
            await loop.run_in_executor(None, post_linkedin.post_to_linkedin, current_draft_path)
            
            await update.message.reply_text(f"✅ **Published!**\nFiled archived as POSTED_...")
            current_draft_path = None
            
        except Exception as e:
            await update.message.reply_text(f"❌ Publishing failed: {e}")
            
    else:
        # Assume it's feedback? Or just chat.
        await update.message.reply_text("I didn't understand. Use /search, 'Draft ...' or 'APPROVE'.")

# Scheduler Logic
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(60)

def daily_job():
    # How to send message from thread?
    # Need access to bot application to send message to TARGET_CHAT_ID
    # For now, simplistic implementation: complex in async.
    # Better: Use JobQueue from python-telegram-bot
    pass

if __name__ == '__main__':
    if not TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN not found.")
        exit(1)
        
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("search", search_command))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Bot is polling...")
    app.run_polling()
