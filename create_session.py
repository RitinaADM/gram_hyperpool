import os
from dotenv import load_dotenv
import asyncio
import telethon
from telethon.sync import TelegramClient

load_dotenv()


async def main():
    phone_number = str(input('Укажите phone_number: '))
    if input('Номер телефона указан корректно? Y/n: ') in ['Y', 'y', 'yes']:
        client = TelegramClient('session', api_id=os.getenv('api_id'), api_hash=os.getenv('api_hash'), device_model='iphone 13')
        await client.connect()
        if not await client.is_user_authorized():
            try:
                await client.send_code_request(phone_number)
                await client.sign_in(phone_number, input('Введите код подтверждения: '))

            except telethon.errors.rpcerrorlist.PhoneNumberBannedError as e:
                exit('Phone number is banned')
            exit('not authorized')
        await client.disconnect()
        print('Сессия успешно обновлена, теперь вы можете перейти к запуску сервера.')
    else:
        exit()


asyncio.run(main())
