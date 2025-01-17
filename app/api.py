from characterai import aiocai
import asyncio
import requests

uList = []


def p(text):
    uList.append(text)
    print(uList)
    

async def main():
    uList.clear()
    char = "6cfnxCukeMpNyVmQ-bIbR9_X3k95XDk1lm3Buot6AiM"

    client = aiocai.Client('d617adf0297d7f83c25b75f94066db8b1a90a0ec')

    me = await client.get_me()

    async with await client.connect() as chat:
        new, answer = await chat.new_chat(
            char, me.id
        )

        print(f'{answer.name}: {answer.text}')
        
        while True:
            text = "hello"

            message = await chat.send_message(
                char, new.chat_id, text
            )

            print(f'{message.name}: {message.text}')

# asyncio.run(main())
