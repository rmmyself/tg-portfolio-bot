<div align="center">

```
╔═══════════════════════════════════════╗
║                                       ║
║   ✦  T G   P O R T F O L I O  ✦     ║
║         B O T                        ║
╚═══════════════════════════════════════╝
```

**A sleek Telegram portfolio bot. Zero code editing — configure everything in one YAML file.**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-26A5E4?style=for-the-badge&logo=telegram&logoColor=white)](https://core.telegram.org/bots)
[![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://sqlite.org)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge)](LICENSE)

</div>

---

## ✦ What it does

A personal portfolio bot for Telegram. Everything — texts, links, projects, bio — is configured in a single `config.yaml` file. No need to touch `bot.py` at all.

```
/start
  ├── 📁 Projects       ← pulled from config.yaml
  │     └── → each repo with desc, stack, GitHub link
  ├── 👤 About          ← pulled from config.yaml
  ├── 📝 Place an order ← client writes brief → you get notified → reply in bot
  └── 🐙 GitHub         ← pulled from config.yaml
       (🌐 Website — one toggle in config.yaml)
```

---

## ✦ Features

| Feature | Details |
|---|---|
| ⚙️ YAML config | Edit all texts, links, projects without touching the code |
| 🌐 Bilingual | Russian & English — language saved per user in SQLite |
| 🗂 Project showcase | Each repo: name, description, tech stack, GitHub link |
| 📝 Order system | Client writes a brief → you get notified → reply right in the bot |
| 💬 Direct reply | Reply to clients without leaving Telegram |
| 🗄 Order history | All orders saved to SQLite |
| 🌐 Website toggle | `website_enabled: true/false` in config |

---

## ✦ How the order system works

```
Client              Bot                  You (admin)
  │                  │                       │
  ├── "Place order" ►│                       │
  ├── writes brief ──►── saves to SQLite     │
  │◄── "Received!" ──│── notifies ──────────►│
  │                  │◄── taps "Reply" ───────┤
  │◄── reply ────────│◄── writes reply ───────┤
```

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

**3. Edit `config.yaml`**

This is the only file you need to edit:

```yaml
bot_token: "YOUR_BOT_TOKEN_HERE"
admin_id: 123456789          # your Telegram ID (@userinfobot)

developer:
  name_ru: "Алекс"
  name_en: "Alex"
  handle: "yourusername"
  ...

links:
  github: "https://github.com/yourusername"
  website_enabled: false
  website: "https://yoursite.com"

repos:
  - name: "your-repo"
    desc_ru: "Описание"
    desc_en: "Description"
    tech: "Python · FastAPI"
    url: "https://github.com/you/repo"
```

**4. Run**
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

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable portfolio-bot && sudo systemctl start portfolio-bot
```

---

## ✦ Stack

- [python-telegram-bot 21](https://github.com/python-telegram-bot/python-telegram-bot)
- [PyYAML](https://pyyaml.org/)
- SQLite (built-in)
- Python 3.10+

---

<div align="center">

**Built by [rmmyself](https://github.com/rmmyself)**

*Open to bot development orders — DM on Telegram*

</div>
