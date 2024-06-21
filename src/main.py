import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import sys

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()  # Load the .env file

TOKEN = os.getenv('DISCORD_TOKEN')

# Set up the bot
# Set intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # Ensure you enable message content intent

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.command()
async def hello(ctx):
    await ctx.send('Hello!')

# Event when the bot has connected to Discord


async def load_extensions():
    try:
        await bot.load_extension('cogs.twitter_bot')
        print("Cog loaded successfully")
    except Exception as e:
        print(f"Failed to load cog: {e}")


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} - {bot.user.id}')
    await load_extensions()


if __name__ == '__main__':
    # Run the bot
    bot.run(TOKEN)
