API KEYS

Character AI
API Key Status: Uploaded and Active

Obtain Method: 

Log In Via Email
This code asks the user for their email address and sends them a confirmation link. The user then enters the link they received in their email and is given a token for their account

from characterai import aiocai, sendCode, authUser
import asyncio

async def main():
    email = input('YOUR EMAIL: ')

    code = sendCode(email)

    link = input('CODE IN MAIL: ')

    token = authUser(link, email)

    print(f'YOUR TOKEN: {token}')

asyncio.run(main())

Limitations: No Limits

Expiration: Non-expiring

Owner: Abidur Rahman
