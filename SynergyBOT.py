import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
import MySQLdb
import json

datas_json_auth = json.load(open('auth.json'))

Client = discord.Client() #Initialise Client 
client = commands.Bot(command_prefix = "?") #Initialise client bot
canal_id = str(datas_json_auth["channel_id"]) # Obtain the id from default channel to the bot chat in
database_connection = datas_json_auth["connection_db"] # Get the configurations to access the database

@client.event
async def on_ready():
    print("Bot is online and connected to Discord") #This will be called when the bot connects to the server

@client.event
async def on_message(message):
    if canal_id: # Check if the var canal_id is setted
        if message.content.startswith('s!comandos'):
            comandos = "Oi "+message.author.mention+" segue a lista de comandos disponíveis atualmente:\n"
            comandos += "s!cookie -> Bot envia um emoji de cookie\n"
            comandos += "por enquanto é só :D"
            await client.send_message(discord.Object(id=canal_id), comandos)
        if message.content.startswith('s!cookie'): # Command cookie to print the emoticon cookie
            await client.send_message(discord.Object(id=canal_id), ":cookie:") #responds with Cookie emoji when someone says "cookie"
        elif message.content == "$tipos_jogos":
            await client.send_message(discord.Object(id=canal_id), message.author.mention+", estamos analisando nossos dados e isso é o que temos pra hoje :microphone:") #responds with Cookie emoji when someone says "cookie"
            db = MySQLdb.connect(host=database_connection["host"],# your host, usually localhost
                                 user=database_connection["user"],# your username
                                 passwd=database_connection["passwd"],# your password
                                 db=database_connection["db_name"])
            # you must create a Cursor object. It will let
            #  you execute all the queries you need
            cur = db.cursor()
            # Use all the SQL you like
            cur.execute("SELECT name FROM type_game")
            mensagem = "Infelizmente não está cadastrado nenhum tipo de jogo atualmente"
            if len(cur.fetchall()) > 0:
                # print all the first cell of all the rows
                for row in cur.fetchall():
                    await client.send_message(discord.Object(id=canal_id), row[0]+" putsss")
            else:
                print(message.author.id)
                await client.send_message(discord.Object(id=canal_id), " Opa, "+ message.author.mention +" : "+mensagem)
            
            db.close()
        if message.content.startswith('$bixao'):
            await client.send_message(discord.Object(id=canal_id), 'Quem é o bixão? Escreva $nome_do_bixao nome')
            def check(msg):
                return msg.content.startswith('$nome_do_bixao')
            message = await client.wait_for_message(author=message.author, check=check)
            name = message.content[len('$nome_do_bixao'):].strip()
            await client.send_message(discord.Object(id=canal_id), '{} é o bixão meeeemo heeeeeein!!!!'.format(name))
        if message.content.startswith('$CANAL'):
            await client.send_message(discord.Object(id=canal_id), 'hello')
    else:
        print("Vazio");
        exit();
        print(discord.Object(id=canal_id))
        #await client.send_message(message.channel, "Hey, Listen! :space_invader:")
        
        # await client.send_message(message.channel, "Por favor, "+ message.author.mention + ", insira os comandos no canal de texto : "+discord.Object(id=canal_id))
                

client.run(datas_json_auth["token"]) #Replace token with your bots token
