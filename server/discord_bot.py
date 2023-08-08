import discord
from discord.ext import tasks
import request_file
import secrets

class MyClient(discord.Client):

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

        # Get Channel ID
        text_channel_id = []
        for server in self.guilds:
            for channel in server.channels:
                if str(channel.type)=='text':
                    text_channel_id.append(channel.id)

        
        self.channel = client.get_channel((text_channel_id[0]))  
        embed = discord.Embed(title="Discord Bot Activated.",colour=0xe9b96e)
        await self.channel.send(embed=embed)


        self.myLoop.start()
        self.tempAlarm=0
        self.isAccesible=True
        self.stats=[]

    async def on_message(self,message):
        
        print(f'Message from {message.author}: {message.content}')

        if message.author == self.user:
            return
        
        if message.content =='!ping':
            await message.channel.send('pong')

        elif message.content.startswith('!reset'):
            if request_file.make_request("http://192.168.1.254:255/reset")==200:
                embed = discord.Embed(title="Alarm Resetted.",colour=0xedd400)
                await message.channel.send(embed=embed)
            else:
                await message.channel.send("Can't connect to the Sensor.")

        elif message.content.startswith('!toggle'):
            if request_file.make_request("http://192.168.1.254:255/toggle")==200:
                if self.stats[2]==0:
                    embed=discord.Embed(title="Sensor Activated.", color=0x73d216)
                    await message.channel.send(embed=embed)
                else:
                    embed=discord.Embed(title="Sensor Deactivated.", color=0xcc0000)
                    await message.channel.send(embed=embed)
            else:
                await message.channel.send("Can't connect to the Sensor.")
            
        elif message.content.startswith('!status'):

            if request_file.status()!=502:
                embed = discord.Embed(title="Status",colour=0x00b0f4)
                embed.add_field(name="Distance",value=f"{self.stats[0]} cm")
                if(self.stats[1]==0):
                    embed.add_field(name="Alarm",value="Off")
                else:
                    embed.add_field(name="Alarm",value="On")
                if(self.stats[2]==0):
                    embed.add_field(name="Toggle",value="Off")
                else:
                    embed.add_field(name="Toggle",value="On")
                await message.channel.send(embed=embed)
            else:
                await message.channel.send("Can't connect to the Sensor.")



    @tasks.loop(seconds=5.0)
    async def myLoop(self):

        if request_file.status()!=502:
            
            self.stats=request_file.status()
            #Stats[0]=Distance,[1]=Alarm, [2]=Toggle
            alarm=int(self.stats[1])

            if (alarm!=self.tempAlarm and alarm!=0):
                print("Alarm!")
                embed=discord.Embed(title="Detect Movement in the Bedroom!", description="DANGER!! DANGER!! DANGER!!", color=0xcc0000)
                await self.channel.send(embed=embed)
            self.tempAlarm=alarm
            if self.isAccesible==False:
                await self.channel.send("Connected to the Sensor")     
                if(self.stats[2]==0):
                    if request_file.make_request("http://192.168.1.254:255/toggle")==200:
                        pass
            self.isAccesible=True   
        else:
            if self.isAccesible==True:
                print('Cannot communicate with sensor!')
                await self.channel.send("Can't Communicate with Sensor")
                self.isAccesible=False
        

intents = discord.Intents.default()
intents.message_content = True 
client = MyClient(intents=intents)

# Discord Token
client.run(secrets.TOKEN_KEY)

