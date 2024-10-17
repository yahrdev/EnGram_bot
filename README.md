# EnGram Telegram Bot

The **EnGram Telegram bot** was created for practicing English grammar. It was built using the **aiogram** framework. The bot extracts tests from APIs presented [here (Async API)](https://github.com/yahrdev/EnGram_async) and [here (Sync API)](https://github.com/yahrdev/EnGram_sync), depending on the specified setup. It also uses **Aioredis** for saving the user's ID, allowing the user to continue interacting with the bot without having to reselect their English level.

## Technologies Used

- **aiogram**: Framework for building Telegram bots.
- **Aioredis**: Asynchronous Redis client for managing the cache layer.
- **Pydantic**: For data validation in the bot's logic.
- **pytest-asyncio**: For writing and running asynchronous unit tests.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/EnGram_bot.git
```

### 2. Navigate into the project directory

```bash
cd EnGram_bot
```

### 3. Install the dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up the environment

Create .env and file based on the provided example. 


### 5. Set up Redis

Download Redis and place the folder on disk C (for example). Open a command prompt and navigate to the Redis folder:

```bash
cd C:\Redis
```

Set up configuration file. You can either modify the redis.windows.conf or create a copy: redis-bot.conf.
Start Redis server:

```bash
redis-server.exe redis-bot.conf
```

### 7. Run the application

```bash
python api/app.py
```
And check the telegram bot.
