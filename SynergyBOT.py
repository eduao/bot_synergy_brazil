import discord
from discord.ext.commands import Bot
from discord.ext import commands
# import asyncio
import time
import MySQLdb
import json

# Busca as configurações do arquivo auth.json
#   - o padrão encontra-se em auth.json.example
datas_json_auth = json.load(open('auth.json'))
# prefixo padrão será s!
prefix = 's!'
#inicializa o bot com o prefixo - prefix
client = commands.Bot(command_prefix=prefix)
# o id do canal é inserido no arquivo json
# com isso ele só irá imprimir neste local, caso queira alterar esse cenário, 
# há a necessidade de onde pergunta se é o canal_id
canal_id = str(datas_json_auth['channel_id'])
# informações para conectar ao banco de dados
database_connection = datas_json_auth['connection_db'] # Get the configurations to access the database
#game_set = discord.Game(name=':: s!')

@client.event
async def on_ready():
    print("Bot is online and connected to Discord") #This will be called when the bot connects to the server
    await client.change_presence(game=discord.Game(name='Somos todos s!')) # altera o status do bot (jogando ...)

@client.event
async def on_message(message):
    if canal_id: # Check if the var canal_id is setted
        # caso a mensagem inicie com o prefixo
        if message.content.startswith(prefix):
            # o comando é buscado da mensagem enviada
            cmd = message.content[len(prefix):]
            # caso tenha comando
            if cmd:
                # caso o comando seja 'comandos'
                if cmd.startswith('comandos'):
                    # comandos é a mensagem que será enviada
                    comandos = 'Oi '+message.author.mention+' segue a lista de comandos disponíveis atualmente:\n'
                    # envia de modo assincrono a mensagem para o canal_id a mensagem comandos
                    await client.send_message(discord.Object(id=canal_id), comandos)
                    #comandos é a mensagem com a lista de comandos disponíveis
                    comandos = '```Markdown \n'
                    comandos += '# '+prefix+'comandos: \n'
                    comandos += '[s!cookie](Bot envia um emoji de cookie)\n'
                    comandos += '[s!qeb <nome>] ou [s!bixao <nome>] ou [s!bixão <nome>](Diga quem é o bixão do server)\n'
                    comandos += 'por enquanto é só :D'
                    comandos += '```'
                    # envia a mensagem para o canal_id a mensagem contida em comandos
                    await client.send_message(discord.Object(id=canal_id), comandos)
                # caso o comando for cookie
                elif cmd.startswith('cookie'): 
                    #responde para o canal_id o emoji cookie
                    await client.send_message(discord.Object(id=canal_id), ":cookie:")
                # caso o comando qeb ou bixao ou bixão
                elif cmd.startswith('qeb') or cmd.startswith('bixao') or cmd.startswith('bixão'):
                    passp = 'bixão'
                    # verifica qual comando foi iniciado
                    if cmd.startswith('qeb'):
                        passp = 'qeb'
                    elif cmd.startswith('bixao'):
                        passp = 'bixao'
                    # retira da mensagem o comando para buscar o restante da mesma
                    name = cmd[len(passp):].strip()
                    # caso tenha o nome do bixão
                    if name:
                        # envia a mensagem que o mencionado é o bixão
                        await client.send_message(discord.Object(id=canal_id), '{} é o bixão meeeemo heeeeeein!!!!'.format(name))
                    else:
                        # envia como utizar o método do bixão
                        await client.send_message(discord.Object(id=canal_id), 'coloque '+prefix+passp+' <nome do bixão>')
            # caso entre apenas com o prefixo sem um comando                
            else:
                # informa ao usuário que a mensagem é um comando vazio
                await client.send_message(discord.Object(id=canal_id), 'entrou com comando vazio')
        # caso não seja enviado no canal apenas retorna
        else:
            return
    else:
        print("Vazio");
        exit();
        print(discord.Object(id=canal_id))

#inicializa o client com o token nas configurações em json                
client.run(datas_json_auth["token"]) 
