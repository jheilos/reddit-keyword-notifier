"""Reddit keyword notifier — streams subreddits and sends Telegram alerts."""

from __future__ import annotations

import logging
import os
import time

import praw
import requests
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def _reddit_client() -> praw.Reddit:
    return praw.Reddit(
        client_id=os.environ["REDDIT_CLIENT_ID"],
        client_secret=os.environ["REDDIT_CLIENT_SECRET"],
        user_agent=os.environ.get(
            "REDDIT_USER_AGENT", "reddit-keyword-notifier/1.0 (personal bot)"
        ),
    )


def _send_telegram(token: str, chat_id: str, text: str) -> None:
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    resp = requests.post(url, json=payload, timeout=10)
    if not resp.ok:
        logger.warning("Telegram send failed: %s", resp.text)


def _keywords() -> list[str]:
    raw = os.environ.get("KEYWORDS", "")
    return [kw.strip().lower() for kw in raw.split(",") if kw.strip()]


def _subreddits() -> str:
    return os.environ.get("SUBREDDITS", "all")


def _matches(submission: praw.models.Submission, keywords: list[str]) -> list[str]:
    haystack = f"{submission.title} {submission.selftext}".lower()
    return [kw for kw in keywords if kw in haystack]


def monitor() -> None:
    keywords = _keywords()
    if not keywords:
        raise SystemExit("Set at least one keyword in KEYWORDS env var.")

    telegram_token = os.environ["TELEGRAM_BOT_TOKEN"]
    telegram_chat = os.environ["TELEGRAM_CHAT_ID"]
    subreddits = _subreddits()

    reddit = _reddit_client()
    logger.info("Watching r/%s for keywords: %s", subreddits, ", ".join(keywords))

    while True:
        try:
            stream = reddit.subreddit(subreddits).stream.submissions(skip_existing=True)
            for submission in stream:
                matched = _matches(submission, keywords)
                if not matched:
                    continue

                logger.info("Match %s — %s", matched, submission.shortlink)
                msg = (
                    f"<b>Keyword alert:</b> {', '.join(matched)}\n"
                    f"<b>Subreddit:</b> r/{submission.subreddit}\n"
                    f"<b>Title:</b> {submission.title}\n"
                    f"<b>Link:</b> {submission.shortlink}"
                )
                _send_telegram(telegram_token, telegram_chat, msg)

        except Exception as exc:
            logger.error("Stream error: %s — restarting in 60 s", exc)
            time.sleep(60)


if __name__ == "__main__":
    monitor()
