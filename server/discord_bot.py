import discord
from discord.ext import tasks
import request_file
import secrets

class MyClient(discord.Client):

    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        channel = client.get_channel(1136435376718884864)
        await channel.send("Discord Bod Activated.")
        self.myLoop.start()

    async def on_message(self,message):
        print(f'Message from {message.author}: {message.content}')
        if message.author == self.user:
            return
        
        if message.content =='ping':
            await message.channel.send('pong')

    @tasks.loop(seconds=5.0)
    async def myLoop(self):
        channel = client.get_channel(1136435376718884864)
        print(request_file.status())


intents = discord.Intents.default()
intents.messages = True 
client = MyClient(intents=intents)
client.run(secrets.TOKEN_KEY)