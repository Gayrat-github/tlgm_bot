import asyncio
import logging
from aiogram import Bot, Dispatcher, types
import datetime
import pymongo
import json
from pydantic import BaseModel
import procedures as p

# Config values:
db_url          = "mongodb://localhost:27023/"
db_instance     = "test"
db_collection   = "sample_collection"
tlg_api_hash    = "xxxx"

db = pymongo.MongoClient(db_url)[db_instance][db_collection]
bot = Bot(token=tlg_api_hash)
dp = Dispatcher()


class Data(BaseModel):
    dt_from: datetime.datetime
    dt_upto: datetime.datetime
    group_type: str


@dp.message()
async def get_message(message):
    if message.text == "/start":
        await message.answer(text=f"Hi {message.from_user.first_name}!")
    else:
        try:
            req_data = Data(**json.loads(message.text))
            if req_data.group_type not in ("month", "day", "hour"):
                raise ValueError
        except:
            await bot.send_message(message.chat.id, "Не верный формат входных данных.")
        else:
            # bot.send_message(message.chat.id, json.dumps(p.get_data(db, req_data)))
            await bot.send_message(message.chat.id, p.get_data(db, req_data))

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

