import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
# from web_server import keep_alive

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
HAS_PERMISSIONS = [
        326339597149929504,
        456841430208479262
    ]
BOT_ID = 234395307759108106
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', help_command=None, intents=intents)


@bot.event
async def on_ready():
    print("bot on")
    await bot.change_presence(activity=discord.Game(name=":)"))


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.MissingRequiredArgument):
        await ctx.send("Niepoprawna składnia komendy, wpisz !help aby sprawdzić składnie komendy.")
    elif isinstance(error, discord.ext.commands.errors.MemberNotFound):
        await ctx.send('Nie ma takiego użytkownika.')
    elif isinstance(error, discord.ext.commands.errors.CheckFailure):
        await ctx.send('Nie masz uprawnień do używania tej komendy.')
    elif isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.send('Brak uprawnień.')


@bot.listen('on_message')
async def check_message(message):
    if message.author == bot.user:
        return

    # linijki poniżej służą do usuwania wiadomości związanych z puszczaniem muzyki oraz wiadomości bota.

    if message.content.lower().startswith(('-p', '-q', '-s', '-r', '-l', '-c', '-b', '-n', '-j', '-d', '-f', '-m')):
        await message.delete(delay=10)
    if message.author.id == BOT_ID:
        await message.delete(delay=15)


@bot.command('kielecka')
@commands.has_role('Kielecka Ekipa')
@commands.cooldown(1, 60, commands.BucketType.guild)
async def send_msg_to_kielecka(ctx):
    msg = 'Ludzie na serwerze Kielecka Ekipa potrzebują Cię w swoim składzie!'
    for member in ctx.guild.members:
        for role in member.roles:
            if str(role) == 'Kielecka Ekipa':
                await member.send(msg)


def check_permissions(ctx):
    return ctx.message.author.id in HAS_PERMISSIONS


@bot.command(pass_content=True)
@commands.check(check_permissions)
async def daj_role(ctx, user: discord.Member, role: discord.Role):
    await user.add_roles(role)


@bot.command(pass_content=True)
@commands.check(check_permissions)
async def usun_role(ctx, user: discord.Member, role: discord.Role):
    await user.remove_roles(role)


@bot.command(pass_content=True)
async def cls(ctx, msg_number: int = None, user: discord.Member = None):
    if ctx.message.author.id not in HAS_PERMISSIONS:
        await ctx.channel.send('Nie masz uprawnień do tej komendy.')
        return
    if msg_number > 100:
        response = '**Zbyt dużo wiadomości do usunięcia! Maksymalnie można usunąć 100 wiadomości.**'
        await ctx.channel.send(response)
        return
    if user is None:
        await ctx.channel.purge(limit=msg_number + 1, check=None, bulk=True)
        return
    await ctx.channel.purge(limit=1, check=None, bulk=True)

    def check_user(ctx):
        return ctx.author == user

    msg_to_delete: int = 0
    all_msg: int = 0

    messages = await ctx.channel.history().flatten()

    for message in messages:
        if msg_to_delete == msg_number:
            break
        if message.author == user:
            msg_to_delete += 1
        all_msg += 1

    await ctx.channel.purge(limit=all_msg, check=check_user, bulk=True)


# keep_alive()
bot.run(TOKEN)  # run bot

# bot.remove_command('help') # removes default help command
