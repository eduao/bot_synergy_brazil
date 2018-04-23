import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
import MySQLdb
import json

datas_json_auth = json.load(open('auth.json'))
prefix = 's!'

client = commands.Bot(command_prefix=prefix) #Initialise client bot

#client.run(datas_json_auth["token"]) #Replace token with your bots token

#Client = discord.Client() #Initialise Client 

# client = commands.Bot(command_prefix=prefix) #Initialise client bot
#bot = commands.Bot(command_prefix='?', description=description)
canal_id = str(datas_json_auth['channel_id']) # Obtain the id from default channel to the bot chat in
database_connection = datas_json_auth['connection_db'] # Get the configurations to access the database
#game_set = discord.Game(name=':: s!')

@client.event
async def on_ready():
    print("Bot is online and connected to Discord") #This will be called when the bot connects to the server
    await client.change_presence(game=discord.Game(name='Somos todos s!'))
    print('teste')

@client.event
async def on_message(message):
    if canal_id: # Check if the var canal_id is setted
        # await client.send_message(discord.Object(id=canal_id), prefix)
        if message.content.startswith(prefix):
            cmd = message.content[len(prefix):]
            if cmd:
                # await client.send_message(discord.Object(id=canal_id), cmd)
                if cmd.startswith('comandos'):
                    comandos = 'Oi '+message.author.mention+' segue a lista de comandos disponíveis atualmente:\n'
                    await client.send_message(discord.Object(id=canal_id), comandos)
                    comandos = '```Markdown \n'
                    comandos += '# '+prefix+'comandos: \n'
                    comandos += '[s!cookie](Bot envia um emoji de cookie)\n'
                    comandos += '[s!qeb <nome>] ou [s!bixao <nome>] ou [s!bixão <nome>](Diga quem é o bixão do server)\n'
                    comandos += 'por enquanto é só :D'
                    comandos += '```'
                    await client.send_message(discord.Object(id=canal_id), comandos)
                elif cmd.startswith('cookie'): # Command cookie to print the emoticon cookie
                    await client.send_message(discord.Object(id=canal_id), ":cookie:") #responds with Cookie emoji when someone says "cookie"
                elif cmd.startswith('qeb') or cmd.startswith('bixao') or cmd.startswith('bixão'):
                    passp = 'bixão'
                    if cmd.startswith('qeb'):
                        passp = 'qeb'
                    elif cmd.startswith('bixao'):
                        passp = 'bixao'
                    name = cmd[len(passp):].strip()
                    if name:
                        await client.send_message(discord.Object(id=canal_id), '{} é o bixão meeeemo heeeeeein!!!!'.format(name))
                    else:
                        await client.send_message(discord.Object(id=canal_id), 'coloque '+prefix+passp+' <nome do bixão>')
                        
            else:
                await client.send_message(discord.Object(id=canal_id), 'entrou com comando vazio')
        else:
            return
    else:
        print("Vazio");
        exit();
        print(discord.Object(id=canal_id))
        #await client.send_message(message.channel, "Hey, Listen! :space_invader:")
        
        # await client.send_message(message.channel, "Por favor, "+ message.author.mention + ", insira os comandos no canal de texto : "+discord.Object(id=canal_id))
                
client.run(datas_json_auth["token"]) #Replace token with your bots token
