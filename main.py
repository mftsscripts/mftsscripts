# ZÁKLAD

import discord

from discord.ext import commands

import logging

from dotenv import load_dotenv

import os



load_dotenv()

token = os.getenv('DISCORD_TOKEN')

log_channel_id = int(os.getenv("LOG_CHANNEL_ID"))



# LOGY

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()

intents.message_content = True

intents.members = True



# ZNAK NA VYVOLÁNÍ

bot = commands.Bot(command_prefix='.', intents=intents)



# FUNKCE PRO DISCORD LOGOVÁNÍ

async def log_to_channel(zprava: str):

    try:

        kanal = await bot.fetch_channel(log_channel_id)

        if kanal:

            await kanal.send(zprava)

    except Exception as e:

        print(f"Chyba při logování do kanálu: {e}")



# ZAPNUTÍ KÓDU

@bot.event

async def on_ready():

    print(f"Spouštím kód >>>, {bot.user.name}")

    await log_to_channel(f"⏰ **Sentinel** byl spuštěn")



# STATUS CHECK

@bot.command()

@commands.cooldown(rate=1, per=15.0, type=commands.BucketType.user)

async def sentinel(ctx):

    await ctx.send(f"Jsem online a připraven posloužit {ctx.author.mention}!")

    await log_to_channel(f"📨 **{ctx.author}** použil příkaz .sentinel v {ctx.channel.mention}")



@sentinel.error

async def sentinel_error(ctx, error):

    if isinstance(error, commands.CommandOnCooldown):

        await ctx.send(f"⏳ Tento příkaz můžeš použít znovu za {error.retry_after:.1f} sekund.")



# ANKETA

@bot.command()

@commands.cooldown(rate=1, per=15.0, type=commands.BucketType.user)

async def anketa(ctx, *, otazka):

    embed = discord.Embed(title="Anketa", description=otazka)

    zprava = await ctx.send(embed=embed)

    await zprava.add_reaction("✅")

    await zprava.add_reaction("❌")

    await log_to_channel(f"📊 **{ctx.author}** vytvořil anketu v {ctx.channel.mention} s názvem : *{otazka}*")



@anketa.error

async def anketa_error(ctx, error):

    if isinstance(error, commands.CommandOnCooldown):

        await ctx.send(f"⏳ Tento příkaz můžeš použít znovu za {error.retry_after:.1f} sekund.")



# CHAT FILTER

ZAKAZANA_SLOVA = [

    "nigger", "n1gger", "n!gger", "ni99er", "nigg3r", "n1gg3r", "nigg*r", "nigg.r", "n1gg4", "nigg.a",

    "n i g g e r", "nıgger", "ńigger", "nīgger", "nɪgger", "nigga", "n1gga", "n!gga", "ni99a", "nigg4", "nigg@",

    "n i g g a", "nıgga", "ńigga", "niggah", "nigguh", "niqqa", "nikka", "niga", "nigar", "kneegrow",

    "knee-gah", "neega", "neegah", "neegro", "negr", "nigr", "négř", "negrík", "tmavák", "nigg@h", "nigguhh",

    "banánžrout", "čokovůdce", "cigoš", "cigos", "cigoši", "dežo", "dežko", "dežik", "n!gga", "n!g@", "n_gga",

    "n!gg@", "n1gg@", "n!gg4", "n!gguh", "ni.gga", "n1.g.g.e.r", "n!g.g.a", "n¡gga",

]



@bot.event

async def on_message(message):

    if message.author == bot.user:

        return



    obsah = message.content.lower()

    if any(slovo in obsah for slovo in ZAKAZANA_SLOVA):

        await message.delete()

        upozorneni = f"{message.author.mention} - Tvá zpráva byla smazána z důvodu nevhodného výrazu."

        await message.channel.send(upozorneni)

        await log_to_channel(

            f"🚫 Zpráva od **{message.author}** smazána v {message.channel.mention}:\n\n{message.content}\n")

        

    await bot.process_commands(message)

    



# MUSÍ BÝT NA KONCI PRO LOGY

bot.run(token, log_handler=handler, log_level=logging.DEBUG)
