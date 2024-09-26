from discord.ext import commands
from dotenv import load_dotenv
import aiosqlite
import discord
import os

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Initialize the database
@bot.event
async def on_ready():
    async with aiosqlite.connect('economy.db') as db:
        await db.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, balance INTEGER)')
        await db.commit()
    print(f'{bot.user} has connected to Discord!')

@bot.command(name='balance')
async def balance(ctx):
    async with aiosqlite.connect('economy.db') as db:
        async with db.execute('SELECT balance FROM users WHERE id = ?', (ctx.author.id,)) as cursor:
            row = await cursor.fetchone()
            if row is None:
                await db.execute('INSERT INTO users (id, balance) VALUES (?,?)', (ctx.author.id, 100))
                await db.commit()
                balance = 100
            else:
                balance = row[0]
        await ctx.send(f'{ctx.author.mention} has a balance of {balance} coins.')



bot.run(os.getenv('BOT_TOKEN'))