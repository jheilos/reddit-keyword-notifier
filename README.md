# Reddit Keyword Notifier

A lightweight personal bot that streams Reddit submissions in real time and sends a Telegram message whenever a post matches one of your keywords.

Built with [PRAW](https://praw.readthedocs.io/) (the official Python Reddit API Wrapper).

## Features

- Streams live submissions from one subreddit, a multi-subreddit list, or all of Reddit
- Case-insensitive keyword matching across post title and body
- Telegram notification with subreddit, title, and direct link
- Auto-reconnects after network or API errors
- Runs as a single Docker container — no database, no dependencies beyond pip

## Quick start (local)

```bash
cp .env.example .env
# fill in your credentials in .env

pip install -r requirements.txt
python bot.py
```

## Quick start (Docker)

```bash
cp .env.example .env
# fill in your credentials in .env

docker build -t reddit-keyword-notifier .
docker run --env-file .env reddit-keyword-notifier
```

Or with docker compose:

```bash
docker compose up -d
```

## Configuration

All configuration is done via environment variables (or a `.env` file):

| Variable | Description |
|---|---|
| `REDDIT_CLIENT_ID` | Reddit app client ID |
| `REDDIT_CLIENT_SECRET` | Reddit app client secret |
| `REDDIT_USER_AGENT` | User-agent string for Reddit API requests |
| `KEYWORDS` | Comma-separated keywords to watch for |
| `SUBREDDITS` | Comma-separated subreddit names, or `all` |
| `TELEGRAM_BOT_TOKEN` | Token from [@BotFather](https://t.me/BotFather) |
| `TELEGRAM_CHAT_ID` | Your Telegram chat/user ID |

### Getting Reddit API credentials

1. Go to <https://www.reddit.com/prefs/apps>
2. Click **create another app**
3. Choose **script**, fill in any redirect URI (e.g. `http://localhost`)
4. Copy the **client ID** (under the app name) and **client secret**

### Getting your Telegram credentials

1. Message [@BotFather](https://t.me/BotFather) → `/newbot` → copy the token
2. Message [@userinfobot](https://t.me/userinfobot) to get your numeric chat ID

## Usage

The bot uses Reddit's push stream, so it only fires on new posts — no polling delay, no duplicate alerts.

To watch multiple specific subreddits set `SUBREDDITS=python+learnpython+programming`.

## License

MIT
