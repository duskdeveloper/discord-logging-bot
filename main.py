import asyncio
import os
import sys
import logging
from bot.core import DiscordBot

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('bot.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )

async def main():
    setup_logging()
    
    token = os.getenv('DISCORD_BOT_TOKEN')
    if not token:
        logging.error("DISCORD_BOT_TOKEN environment variable is required")
        return
    
    bot = DiscordBot()
    
    try:
        await bot.start(token)
    except KeyboardInterrupt:
        logging.info("Bot stopped by user")
    except Exception as e:
        logging.error(f"Bot crashed: {e}")
    finally:
        await bot.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Application terminated")
