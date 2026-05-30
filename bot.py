import os
import sqlite3
import yaml
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode

# ── Load config ────────────────────────────────────────────────────────────
with open("config.yaml", "r", encoding="utf-8") as f:
    cfg = yaml.safe_load(f)

BOT_TOKEN = cfg["bot_token"]
ADMIN_ID = int(cfg["admin_id"])
DEV = cfg["developer"]
LINKS = cfg["links"]
REPOS = cfg["repos"]
SERVICES = cfg["services"]

# ── Database ───────────────────────────────────────────────────────────────
def init_db():
    con = sqlite3.connect("users.db")
    con.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, lang TEXT)")
    con.execute("""CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        username TEXT,
        text TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )""")
    con.commit()
    con.close()

def get_lang(user_id):
    con = sqlite3.connect("users.db")
    row = con.execute("SELECT lang FROM users WHERE user_id=?", (user_id,)).fetchone()
    con.close()
    return row[0] if row else None

def set_lang(user_id, lang):
    con = sqlite3.connect("users.db")
    con.execute("INSERT INTO users(user_id,lang) VALUES(?,?) ON CONFLICT(user_id) DO UPDATE SET lang=?", (user_id, lang, lang))
    con.commit()
    con.close()

def save_order(user_id, username, text):
    con = sqlite3.connect("users.db")
    cur = con.execute("INSERT INTO orders(user_id,username,text) VALUES(?,?,?)", (user_id, username, text))
    oid = cur.lastrowid
    con.commit()
    con.close()
    return oid

# ── Build texts from config ────────────────────────────────────────────────
def welcome(lang):
    name = DEV[f"name_{lang}"]
    return (
        f"✦ *{'Привет, я' if lang=='ru' else 'Hey, I am'} {name}* ✦\n\n"
        f"{DEV[f'about_{lang}'].strip()}\n\n"
        f"_{'Выбери раздел' if lang=='ru' else 'Choose a section'}_ 👇"
    )

def about(lang):
    services = "\n".join(f"• {s}" for s in SERVICES[lang])
    cta = "Есть проект? Нажми *«Сделать заказ»* 👇" if lang == "ru" else "Have a project? Hit *«Place an order»* 👇"
    return (
        f"👤 *{'О себе' if lang=='ru' else 'About'}*\n\n"
        f"```\n"
        f"{'Ник' if lang=='ru' else 'Handle'}     →  {DEV['handle']}\n"
        f"{'Стек' if lang=='ru' else 'Stack'}    →  {DEV['stack']}\n"
        f"{'Фокус' if lang=='ru' else 'Focus'}   →  {DEV[f'focus_{lang}']}\n"
        f"{'Статус' if lang=='ru' else 'Status'}  →  {DEV[f'status_{lang}']}\n"
        f"```\n\n"
        f"{DEV[f'about_{lang}'].strip()}\n\n"
        f"*{'Что предлагаю' if lang=='ru' else 'What I offer'}:*\n{services}\n\n"
        f"{cta}"
    )

def projects_text(lang):
    header = "📁 *Проекты*" if lang == "ru" else "📁 *Projects*"
    lines = "\n".join(f"• `{r['name']}` — {r[f'desc_{lang}']}" for r in REPOS)
    hint = "_Выберите проект для подробностей:_" if lang == "ru" else "_Tap a project for details:_"
    return f"{header}\n\n{lines}\n\n{hint}"

def repo_text(lang, repo):
    label = "Стек" if lang == "ru" else "Stack"
    return f"*{repo['name']}*\n\n{repo[f'desc_{lang}']}\n\n*{label}:* `{repo['tech']}`\n\n🔗 {repo['url']}"

def order_prompt(lang):
    if lang == "ru":
        return "📝 *Оформление заказа*\n\nОпиши свой проект:\n• Что должен делать бот?\n• Какие функции нужны?\n• Сроки и бюджет (если есть)\n\n_Напиши всё в одном сообщении:_"
    return "📝 *Place an order*\n\nDescribe your project:\n• What should the bot do?\n• What features do you need?\n• Timeline and budget (if any)\n\n_Write everything in one message:_"

def order_received(lang):
    if lang == "ru":
        return "✅ *Заказ принят!*\n\nЯ получил твоё ТЗ и скоро свяжусь с тобой.\nОбычно отвечаю в течение нескольких часов."
    return "✅ *Order received!*\n\nI got your brief and will get back to you soon.\nUsually reply within a few hours."

def reply_text(lang, text):
    label = "Ответ от разработчика" if lang == "ru" else "Reply from developer"
    return f"💬 *{label}:*\n\n{text}"

# ── Keyboards ──────────────────────────────────────────────────────────────
def lang_kb():
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("🇷🇺  Русский", callback_data="lang_ru"),
        InlineKeyboardButton("🇬🇧  English", callback_data="lang_en"),
    ]])

def main_kb(lang):
    p = "📁  Проекты" if lang == "ru" else "📁  Projects"
    a = "👤  О себе" if lang == "ru" else "👤  About"
    o = "📝  Сделать заказ" if lang == "ru" else "📝  Place an order"
    cl = "🌐 Change language" if lang == "ru" else "🌐 Сменить язык"
    rows = [
        [InlineKeyboardButton(p, callback_data="projects"), InlineKeyboardButton(a, callback_data="about")],
        [InlineKeyboardButton(o, callback_data="order")],
        [InlineKeyboardButton("🐙  GitHub", url=LINKS["github"])],
        [InlineKeyboardButton(cl, callback_data="choose_lang")],
    ]
    if LINKS["website_enabled"]:
        rows.insert(3, [InlineKeyboardButton("🌐  Website", url=LINKS["website"])])
    return InlineKeyboardMarkup(rows)

def back_kb(lang):
    t = "← Назад" if lang == "ru" else "← Back"
    return InlineKeyboardMarkup([[InlineKeyboardButton(t, callback_data="home")]])

def projects_kb(lang):
    rows = [[InlineKeyboardButton(f"→  {r['name']}", callback_data=f"repo_{i}")] for i, r in enumerate(REPOS)]
    t = "← Назад" if lang == "ru" else "← Back"
    rows.append([InlineKeyboardButton(t, callback_data="home")])
    return InlineKeyboardMarkup(rows)

def repo_kb(lang, repo):
    t = "Смотреть на GitHub →" if lang == "ru" else "View on GitHub →"
    b = "← Все проекты" if lang == "ru" else "← All Projects"
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t, url=repo["url"])],
        [InlineKeyboardButton(b, callback_data="projects")],
    ])

def cancel_kb(lang):
    t = "✕ Отмена" if lang == "ru" else "✕ Cancel"
    return InlineKeyboardMarkup([[InlineKeyboardButton(t, callback_data="cancel_order")]])

def admin_kb(user_id):
    return InlineKeyboardMarkup([[InlineKeyboardButton("💬 Ответить", callback_data=f"reply_{user_id}")]])

# ── Handlers ───────────────────────────────────────────────────────────────
async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    lang = get_lang(uid)
    if not lang:
        await update.message.reply_text("🌐 Choose your language / Выберите язык:", reply_markup=lang_kb())
        return
    await update.message.reply_text(welcome(lang), parse_mode=ParseMode.MARKDOWN, reply_markup=main_kb(lang))

async def btn(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    d = q.data
    uid = q.from_user.id
    lang = get_lang(uid) or "en"

    if d.startswith("lang_"):
        lang = d.split("_")[1]
        set_lang(uid, lang)
        await q.edit_message_text(welcome(lang), parse_mode=ParseMode.MARKDOWN, reply_markup=main_kb(lang))

    elif d == "choose_lang":
        await q.edit_message_text("🌐 Choose your language / Выберите язык:", reply_markup=lang_kb())

    elif d == "home":
        await q.edit_message_text(welcome(lang), parse_mode=ParseMode.MARKDOWN, reply_markup=main_kb(lang))

    elif d == "about":
        await q.edit_message_text(about(lang), parse_mode=ParseMode.MARKDOWN, reply_markup=back_kb(lang))

    elif d == "projects":
        await q.edit_message_text(projects_text(lang), parse_mode=ParseMode.MARKDOWN, reply_markup=projects_kb(lang))

    elif d.startswith("repo_"):
        repo = REPOS[int(d.split("_")[1])]
        await q.edit_message_text(repo_text(lang, repo), parse_mode=ParseMode.MARKDOWN, reply_markup=repo_kb(lang, repo))

    elif d == "order":
        ctx.user_data["waiting_tz"] = True
        await q.edit_message_text(order_prompt(lang), parse_mode=ParseMode.MARKDOWN, reply_markup=cancel_kb(lang))

    elif d == "cancel_order":
        ctx.user_data.pop("waiting_tz", None)
        ctx.user_data.pop("replying_to", None)
        cancel_text = "Отменено." if lang == "ru" else "Cancelled."
        await q.edit_message_text(cancel_text)
        await q.message.reply_text(welcome(lang), parse_mode=ParseMode.MARKDOWN, reply_markup=main_kb(lang))

    elif d.startswith("reply_") and uid == ADMIN_ID:
        ctx.user_data["replying_to"] = int(d.split("_")[1])
        await q.message.reply_text("✏️ Напиши ответ клиенту:")

async def msg(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    text = update.message.text
    lang = get_lang(uid) or "en"

    if uid == ADMIN_ID and ctx.user_data.get("replying_to"):
        target = ctx.user_data.pop("replying_to")
        client_lang = get_lang(target) or "en"
        try:
            await ctx.bot.send_message(target, reply_text(client_lang, text), parse_mode=ParseMode.MARKDOWN)
            await update.message.reply_text("✅ Ответ отправлен.")
        except Exception:
            await update.message.reply_text("❌ Не удалось отправить.")
        return

    if ctx.user_data.get("waiting_tz"):
        ctx.user_data.pop("waiting_tz")
        uname = update.effective_user.username or update.effective_user.first_name or str(uid)
        oid = save_order(uid, uname, text)
        await update.message.reply_text(order_received(lang), parse_mode=ParseMode.MARKDOWN, reply_markup=main_kb(lang))
        if ADMIN_ID:
            await ctx.bot.send_message(
                ADMIN_ID,
                f"🔔 *Новый заказ #{oid}*\n\n👤 @{uname} (`{uid}`)\n\n📋 *ТЗ:*\n{text}",
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=admin_kb(uid)
            )
        return

    await update.message.reply_text(welcome(lang), parse_mode=ParseMode.MARKDOWN, reply_markup=main_kb(lang))

def main():
    init_db()
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(btn))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, msg))
    print("✅ Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
