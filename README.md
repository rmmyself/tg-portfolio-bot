<div align="center">

```
╔═══════════════════════════════════════╗
║                                       ║
║   ✦  T G   P O R T F O L I O  ✦     ║
║         B O T                        ║
╚═══════════════════════════════════════╝
```

**A sleek Telegram portfolio bot that showcases your GitHub projects with style.**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-26A5E4?style=for-the-badge&logo=telegram&logoColor=white)](https://core.telegram.org/bots)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge)](LICENSE)

</div>

---

## ✦ What it does

A personal portfolio bot for Telegram. Visitors tap `/start` and get an interactive menu to explore your projects, read your stack and bio, and jump straight to your GitHub repos — all without leaving Telegram.

```
/start
  ├── 📁 Projects
  │     ├── → tg-ai-assistant   (link to GitHub)
  │     └── → discord-modbot    (link to GitHub)
  ├── 👤 About
  └── 🐙 GitHub Profile
       (🌐 Website — toggle on/off in config)
```

---

## ✦ Features

| Feature | Details |
|---|---|
| 🗂 Project showcase | Each repo gets its own card with description, tech stack & GitHub link |
| 👤 About section | Bio, stack, availability status |
| 🐙 GitHub link | Direct link to your profile |
| 🌐 Website toggle | Enable/disable website button in one line |
| ✏️ Easy to edit | Add new repos in 5 lines of Python |
| 💬 Inline navigation | No page reloads — smooth button-based UX |

---

## ✦ Setup

**1. Clone**
```bash
git clone https://github.com/rmmyself/tg-portfolio-bot
cd tg-portfolio-bot
```

**2. Install**
```bash
pip install -r requirements.txt
```

**3. Configure**
```bash
cp .env.example .env
```

Edit `.env`:
```env
TELEGRAM_BOT_TOKEN=your_token_here
```

**4. Customize** — open `bot.py` and edit:
```python
GITHUB_USERNAME = "your_username"   # your GitHub handle
WEBSITE_ENABLED = False             # set True to show website button
WEBSITE_URL = "https://yoursite.com"

REPOS = [
    {
        "name": "your-repo-name",
        "desc": "Short description",
        "tech": ["Python", "FastAPI"],
        "url": "https://github.com/you/your-repo",
    },
    # add more repos here...
]
```

**5. Run**
```bash
python bot.py
```

---

## ✦ Deploy (systemd)

```ini
[Unit]
Description=Telegram Portfolio Bot
After=network.target

[Service]
WorkingDirectory=/path/to/tg-portfolio-bot
ExecStart=/usr/bin/python3 bot.py
Restart=always
EnvironmentFile=/path/to/tg-portfolio-bot/.env

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable portfolio-bot
sudo systemctl start portfolio-bot
```

---

## ✦ Stack

- [python-telegram-bot 21](https://github.com/python-telegram-bot/python-telegram-bot)
- Python 3.10+

---

<div align="center">

**Built by [rmmyself](https://github.com/rmmyself)**

*Open to bot development orders — DM on Telegram*

</div>
