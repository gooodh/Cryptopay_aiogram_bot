# The bot was created on aiogram payment via CryptoBot. The bot and payment work on FastAPI webhooks.
## 1. install dependencies pip intall -r requirements.txt
## 2. created .env file
```
#B0T
BOT_TOKEN="BOT_TOKEN"

PORT=8080
HOST=0.0.0.0
BASE_URL="URL"
FROM_CHAT_ID=Names_bot

ADMIN_IDS=[1234567,7654321]

CRYPTOPAY_TOKEN=TOKEN_from_@CryptoBot
```

## 3. Command start bot 
```
uvicorn bot.main:app --host 0.0.0.0 --port 8080
```
