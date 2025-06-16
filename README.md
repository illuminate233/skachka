# Telegram Image Bot

Бот шукає всі зображення на сторінці та надсилає найкращу якість у відповідь.

## 🚀 Запуск на Railway

1. Форкни цей репозиторій
2. Додай `.env` з токеном `BOT_TOKEN`
3. Підключи до Railway → New Project → Deploy from GitHub
4. Укажи `worker` як стартову команду

## 🛠️ Ручний запуск

```bash
pip install -r requirements.txt
cp .env.example .env
# додай токен у .env
python bot.py
```
