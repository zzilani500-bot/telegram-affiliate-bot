# 🤖 Telegram Affiliate Marketing Bot (AI-Powered)

An automated Telegram channel bot that uses **Google Gemini AI** to generate and post trending product deals with your **Wishlink** affiliate links. Completely FREE to run!

---

## ✨ Features

- **AI-Powered Content**: Uses Google Gemini to generate realistic product deals
- **Attractive Posts**: Emojis, formatting, urgency-driven captions
- **Auto-Posting**: Posts automatically every 1-2 hours
- **Multiple Categories**: Electronics, fashion, home, beauty, fitness & more
- **No Duplicates**: Tracks posted products to avoid repetition
- **Free to Run**: No paid APIs or services needed

---

## 📋 Setup Instructions

### Step 1: Prerequisites

You need:
- Python 3.7+ installed
- A Telegram Bot (you already have this ✅)
- A Telegram Channel with bot as admin (you already have this ✅)
- Google Gemini API key (you already have this ✅)
- Wishlink account (you already have this ✅)

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Configure the Bot

Open `bot.py` and check these settings at the top:

```python
BOT_TOKEN = "your_bot_token"
CHANNEL_ID = "@your_channel_username"
GEMINI_API_KEY = "your_gemini_api_key"
WISHLINK_URL = "https://wishlink.com/zilani"
POST_INTERVAL = 3600  # seconds between posts
```

### Step 4: Make Sure Bot is Channel Admin

1. Go to your Telegram channel settings
2. Go to Administrators
3. Add your bot as admin
4. Give it permission to "Post Messages"

### Step 5: Run the Bot

```bash
python bot.py
```

---

## 🆓 Free Hosting Options (Run 24/7)

### Option 1: PythonAnywhere (Recommended - Free)

1. Go to [pythonanywhere.com](https://www.pythonanywhere.com)
2. Create a free account
3. Go to "Files" → Upload `bot.py` and `requirements.txt`
4. Go to "Consoles" → Start a Bash console
5. Run:
   ```bash
   pip install -r requirements.txt
   python bot.py
   ```
6. Note: Free tier has daily limits, but works for basic usage

### Option 2: Replit (Free)

1. Go to [replit.com](https://replit.com)
2. Create a new Python project
3. Upload `bot.py` and `requirements.txt`
4. Click "Run"
5. Use UptimeRobot (free) to keep it alive

### Option 3: GitHub Actions (Free - Best for Scheduled Posts)

Create `.github/workflows/post.yml`:
```yaml
name: Post Deal
on:
  schedule:
    - cron: '0 */2 * * *'  # Every 2 hours
  workflow_dispatch:

jobs:
  post:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - run: pip install requests
      - run: python post_once.py
```

### Option 4: Your Own Computer

Just run `python bot.py` and keep your computer on. Use `screen` or `tmux` on Linux:
```bash
screen -S bot
python bot.py
# Press Ctrl+A then D to detach
```

---

## ⚙️ Customization

### Change Posting Frequency

In `bot.py`, change `POST_INTERVAL`:
```python
POST_INTERVAL = 1800   # Every 30 minutes
POST_INTERVAL = 3600   # Every 1 hour (default)
POST_INTERVAL = 7200   # Every 2 hours
```

### Add/Remove Product Categories

Edit the `CATEGORIES` list in `bot.py` to add your preferred niches.

### Change Post Style

Modify the prompt in `generate_post_caption()` to change how posts look.

---

## 💰 How to Earn Money

### 1. Wishlink Affiliate Earnings

- Every time someone clicks your Wishlink and buys a product, you earn commission
- Commission varies: 1-10% depending on category
- More channel subscribers = more clicks = more earnings

### 2. Telegram Ad Platform (After 1000+ Subscribers)

- Once you reach 1000+ subscribers, you can enable Telegram Ads
- Telegram shares 50% of ad revenue with channel owners
- Apply at: [promote.telegram.org](https://promote.telegram.org)

### 3. Sponsored Posts

- Once you have 500+ subscribers, brands may pay for sponsored posts
- Charge ₹500-5000 per sponsored post depending on your audience size

### 4. Other Ad Networks

- **Telega.io** - Telegram ad marketplace
- **Collaborator.pro** - Find advertisers for your channel
- **Direct brand deals** - Reach out to brands for partnerships

---

## 📈 Tips to Grow Your Channel

1. **Post consistently** - 5-10 posts per day
2. **Share in groups** - Share your channel link in related Telegram groups
3. **Cross-promote** - Share on Instagram, WhatsApp status
4. **Quality deals** - Focus on genuinely good discounts (40%+ off)
5. **Engage** - Reply to comments, create polls
6. **Niche down** - Consider focusing on one category initially

---

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| Bot can't post | Make sure bot is admin in channel |
| Wrong channel | Try @shopfree_shop or @shopfreeshop |
| Gemini error | Check API key, ensure free quota not exceeded |
| Posts look bad | Modify the prompt in generate_post_caption() |
| Too many posts | Increase POST_INTERVAL value |

---

## 📁 Files

- `bot.py` - Main bot script (run this)
- `requirements.txt` - Python dependencies
- `README.md` - This file

---

## ⚠️ Important Notes

- Gemini free tier allows 15 requests/minute — more than enough
- Keep your API keys private, never share publicly
- Wishlink terms: Make sure you follow their affiliate guidelines
- Telegram ToS: Don't spam, post quality content

---

Made with ❤️ for your affiliate marketing journey!
