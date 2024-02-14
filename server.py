import os
from dotenv import load_dotenv
import asyncio
from fastapi import FastAPI
import telethon
import logging
import uvicorn

load_dotenv()
logger = logging.getLogger(__name__)
app = FastAPI()


@app.get("/balance")
async def get_balance():
    client = telethon.TelegramClient(session='session', api_id=os.getenv('api_id'), api_hash=os.getenv('api_hash'))
    await client.connect()
    if not await client.is_user_authorized():
        return {'message': 'session is not authorized'}

    bot_username = 'hyperpool_bot'
    event = await client.send_message(bot_username, '/balance')
    await asyncio.sleep(1)
    result = {}
    async for message in client.iter_messages(bot_username, limit=1):
        data = message.text.split('\n')
        result['balance'] = data[0].split(': ')[2]
        result['shares'] = data[1].split(': ')[1]

    await client.disconnect()
    return result


if __name__ == "__main__":
    uvicorn.run('server:app', host="localhost")