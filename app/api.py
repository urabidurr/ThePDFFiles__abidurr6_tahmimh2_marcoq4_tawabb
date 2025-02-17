'''
The PDF Files - Tawab Berri, Abidur Rahman, Marco Quintero, Tahmim Hassan
SoftDev
2025-01-09
p02 - Devuzz
time spent: 14 hrs
'''

from characterai import aiocai
import asyncio
import requests
# Store chat sessions
chat_sessions = {}


CHARACTER_IDS = {
    'Git Clone Topher': '6cfnxCukeMpNyVmQ-bIbR9_X3k95XDk1lm3Buot6AiM',
    'Drake': 'R6pJbz7xlKe7XPrK4I7izj9zn53e4z4c-knowIkyqPU',
    'Hisoka': 'lvB7Pethj1fXrKy1z6FswxpTzjKUGN-98sQX1xpyR-0',
    'Bryant': '2vYCbrPtfS240F4CeQ1fB6pB0nQXqQhBkSLb1Bw-4P8'
}


async def send_message(char_id, message, session_id=None):
    """Sends message To API"""
    client = aiocai.Client('d617adf0297d7f83c25b75f94066db8b1a90a0ec')
    me = await client.get_me()
        
    async with await client.connect() as chat:
        # Create new chat if no session exists
        if session_id not in chat_sessions:
            new, _ = await chat.new_chat(char_id, me.id)
            chat_sessions[session_id] = new.chat_id
            
        # Send message and get response
        message = await chat.send_message(
            char_id, 
            chat_sessions.get(session_id, None),
            message
        )
            
        return message.name, message.text

# async def main():
#     char = input('CHAR ID: ')
#     name, response = await send_message(char, "Hello!")
#     print(f"{name}: {response}")

# asyncio.run(main())
