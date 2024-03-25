import discord
from dotenv import load_dotenv
from discord.ext import commands, tasks
from discord import app_commands
import pandas as pd
import os
import random
import datetime, pytz

# Dotenv
load_dotenv()
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
DISCORD_CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID'))

# Ler .csv
df_frases = pd.read_csv('frases.csv')
df_paineis = pd.read_csv('paineis.csv')

# Permissoes e configuracoes
permissions = discord.Intents.all()
bot = commands.Bot(command_prefix=";",intents=permissions)

# Pegar fuso horario e setar horário
dt = datetime.datetime.now(tz=pytz.timezone('America/Sao_Paulo'))
fuso_horario = dt.tzinfo
horario = datetime.time(8, 0, 0, tzinfo=fuso_horario)

# Mensagen Diaria
@tasks.loop(time=horario)
async def citacao_diaria():
    canal = bot.get_channel(DISCORD_CHANNEL_ID)
    await canal.purge(limit=2)
    capa = await canal.send("https://r4.wallpaperflare.com/wallpaper/943/424/1010/vagabond-takehiko-inoue-wallpaper-f8caaa3ad89c7da1451d37cc5449be15.jpg")
    i = random.randint(0, len(df_frases) - 1)
    dado_aleatorio = df_frases.iloc[i]
    embed_citacao = discord.Embed(
        description=f'### "{dado_aleatorio['frase']}" \n – *{dado_aleatorio['autor']}, {dado_aleatorio["obra"]}.*',
    )
    embed_citacao.color = discord.Color.dark_grey()
    mensagem = await canal.send(embed=embed_citacao)
    await capa.publish()
    await mensagem.publish()
    print("citacao_diaria enviada!")

# Comando - Sincronizar o bot
@commands.has_permissions(administrator=True)
@bot.command(description="Sincronizar o bot.")
async def sync(ctx:commands.Context):
    sync = await bot.tree.sync()
    print(f"Comandos sincronizados: {len(sync)}")
    await ctx.channel.purge(limit=1)

# Comando - Deletar messagens
@commands.has_permissions(manage_messages=True)
@bot.command(description="Deletar mensagens.")
async def delete(ctx:commands.Context, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    print(f";delete enviado! {amount}")

# Comando - Sobre
@bot.tree.command(description="Sobre o bot.")
async def sobre(interact:discord.Interaction):
    embed_sobre = discord.Embed(
        title=f"Sobre o {bot.user.name}",
        description="- Desenvolvido por @ianfelps. \n- Aperte '/' e conheça os comandos do bot!",
    )
    embed_sobre.color = discord.Color.dark_grey()
    embed_sobre.set_author(name="ianfelps", url="https://github.com/ianfelps", icon_url="https://avatars.githubusercontent.com/u/102767014?v=4")
    await interact.response.send_message(embed=embed_sobre)
    print("/sobre enviado!")

# Comando - VASCO
@bot.tree.command(description="Vasco da Gama e nada mais!")
async def vasco(interact:discord.Interaction):
    await interact.response.send_message("◤✠◢ \n> Infelizmente, acabou a competitividade. Não existe mais nenhum adversário a altura do Vasco da Gama no Brasil. Talvez, a exemplo da Austrália que se mudou da Oceania para o futebol asiático em busca de maiores desafios, esteja na hora do Vasco ir pra Europa e jogar a Champions League.")
    print("/vasco enviado!")

# Comando - Citacao aleatoria
@bot.tree.command(description="Citação aleatória.")
async def citacao(interact:discord.Interaction):
    i = random.randint(0, len(df_frases) - 1)
    dado_aleatorio = df_frases.iloc[i]
    embed_citacao = discord.Embed(
        description=f'### "{dado_aleatorio['frase']}" \n – *{dado_aleatorio['autor']}, {dado_aleatorio["obra"]}.*',
    )
    embed_citacao.color = discord.Color.dark_grey()
    await interact.response.send_message(embed=embed_citacao)
    print("/citacao enviada!")

# Comando - Painel aleatorio
@bot.tree.command(description="Painel aleatório.")
async def painel(interact:discord.Interaction):
    i = random.randint(0, len(df_paineis) - 1)
    dado_aleatorio = df_paineis.iloc[i]
    embed_painel = discord.Embed(
        description=f'– *{dado_aleatorio["obra"]}*.',
    )
    embed_painel.set_image(url=dado_aleatorio["link"])
    embed_painel.color = discord.Color.dark_grey()
    await interact.response.send_message(embed=embed_painel)
    print("/painel enviada!")

# Comando - Ping
@bot.tree.command(description="Ping do bot.")
async def ping(interact:discord.Interaction):
    await interact.response.send_message('Pong! \n{0}ms'.format(round(bot.latency * 1000, 1)))
    print("/ping enviado!")

# Comando - Avatar
@bot.tree.command(description="Avatar de usuários.")
async def avatar(interact:discord.Interaction, usuario: discord.Member):
    embed_avatar = discord.Embed(
        title=f"Avatar de {usuario.name}",
    )
    embed_avatar.set_image(url=usuario.display_avatar.url)
    embed_avatar.color = discord.Color.dark_grey()
    await interact.response.send_message(embed=embed_avatar)
    print("/avatar enviado!")

# Comando - Dado
@bot.tree.command(description="Jogar um dado.")
async def dado(interact:discord.Interaction, vezes: int, lados: int,):
    if lados <= 0 or vezes <= 0:
        await interact.response.send_message("O número de vezes e de lados deve ser maior que zero.")
    resultados = []
    total = 0
    for _ in range(vezes):
        resultado = random.randint(1, lados)
        resultados.append(resultado)
        total += resultado
    vezes_str = '\n'.join(str(resultado) for resultado in resultados)
    await interact.response.send_message(f"**Jogadas:**\n{vezes_str}\n\n**Total:** {total}")
    print("/dado enviado!")

# Comandos ao ligar o bot
@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.idle, activity=discord.CustomActivity(name='▬ι══════ﺤ'))
    await citacao_diaria.start()
    print(f"O {bot.user.name} foi iniciado!")

# Ligar Bot
bot.run(DISCORD_BOT_TOKEN)