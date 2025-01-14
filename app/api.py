from characterai import aiocai
import asyncio
import requests

async def main():
    char = input('CHAR ID: ')

    client = aiocai.Client('d617adf0297d7f83c25b75f94066db8b1a90a0ec')

    me = await client.get_me()

    async with await client.connect() as chat:
        new, answer = await chat.new_chat(
            char, me.id
        )

        print(f'{answer.name}: {answer.text}')
        
        while True:
            text = input('YOU: ')

            message = await chat.send_message(
                char, new.chat_id, text
            )

            print(f'{message.name}: {message.text}')

asyncio.run(main())
