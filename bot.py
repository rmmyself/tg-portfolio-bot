import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.constants import ParseMode
from dotenv import load_dotenv

load_dotenv()

GITHUB_USERNAME = "rmmyself"
GITHUB_URL = f"https://github.com/{GITHUB_USERNAME}"
WEBSITE_ENABLED = False
WEBSITE_URL = "https://yourwebsite.com"

REPOS = [
    {
        "name": "tg-ai-assistant",
        "desc": "Telegram AI bot with conversation memory powered by DeepSeek",
        "tech": ["Python", "DeepSeek API", "python-telegram-bot"],
        "url": f"https://github.com/{GITHUB_USERNAME}/tg-ai-assistant",
    },
    {
        "name": "discord-modbot",
        "desc": "Full-featured Discord moderation bot with slash commands & warning system",
        "tech": ["Python", "discord.py", "Slash Commands"],
        "url": f"https://github.com/{GITHUB_USERNAME}/discord-modbot",
    },
]

def main_keyboard():
    buttons = [
        [
            InlineKeyboardButton("📁  Projects", callback_data="projects"),
            InlineKeyboardButton("👤  About", callback_data="about"),
        ],
        [InlineKeyboardButton("🐙  GitHub Profile", url=GITHUB_URL)],
    ]
    if WEBSITE_ENABLED:
        buttons.append([InlineKeyboardButton("🌐  Website", url=WEBSITE_URL)])
    return InlineKeyboardMarkup(buttons)

def back_keyboard():
    return InlineKeyboardMarkup([[InlineKeyboardButton("← Back", callback_data="home")]])

def projects_keyboard():
    buttons = [[InlineKeyboardButton(f"→  {r['name']}", callback_data=f"repo_{i}")] for i, r in enumerate(REPOS)]
    buttons.append([InlineKeyboardButton("← Back", callback_data="home")])
    return InlineKeyboardMarkup(buttons)

def repo_keyboard(repo):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("View on GitHub →", url=repo["url"])],
        [InlineKeyboardButton("← All Projects", callback_data="projects")],
    ])

WELCOME = """✦ *Hey, I'm Alex* ✦

Bot & automation developer.
I build Telegram bots, Discord bots, and backend tools — clean code, fast delivery, hosted on my own servers.

_Choose a section below_ 👇""".strip()

ABOUT = """👤 *About*

```
Handle  →  rmmyself
Stack   →  Python · APIs · Linux
Focus   →  Bots & automation
Status  →  Open to orders ✅
```

I build bots from scratch — no templates, no bloat. Anything from a simple helper bot to a full platform with payments and admin panel.

*What I offer:*
• Telegram bots (any complexity)
• Discord bots & moderation tools  
• API integrations & automation
• Hosting & 24/7 uptime included

Have a project? Just write me.""".strip()

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME, parse_mode=ParseMode.MARKDOWN, reply_markup=main_keyboard())

async def handle(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    d = q.data

    if d == "home":
        await q.edit_message_text(WELCOME, parse_mode=ParseMode.MARKDOWN, reply_markup=main_keyboard())

    elif d == "about":
        await q.edit_message_text(ABOUT, parse_mode=ParseMode.MARKDOWN, reply_markup=back_keyboard())

    elif d == "projects":
        lines = "\n".join(f"• `{r['name']}` — {r['desc']}" for r in REPOS)
        await q.edit_message_text(
            f"📁 *Projects*\n\n{lines}\n\n_Tap a project for details:_",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=projects_keyboard()
        )

    elif d.startswith("repo_"):
        repo = REPOS[int(d.split("_")[1])]
        tech = " · ".join(f"`{t}`" for t in repo["tech"])
        text = f"*{repo['name']}*\n\n{repo['desc']}\n\n*Stack:* {tech}\n\n🔗 {repo['url']}"
        await q.edit_message_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=repo_keyboard(repo))

def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN not set")
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle))
    print("✅ Portfolio bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
