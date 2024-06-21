from utils.fetch_tweet_url import fetch_tweet
from utils.login import login
import discord
from discord.ext import commands, tasks
import datetime


class TwitterCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_tweet_id = None
        self.username = None
        self.channel_id = None
        self.role_id = None
        self.check_tweets.start()
        self.driver = login()
        print("TwitterCog initialized")

    def cog_unload(self):
        self.check_tweets.cancel()

    async def fetch_latest_tweet(self):

        tweet_link = fetch_tweet(
            self.driver, self.last_tweet_id, self.username)

        if tweet_link is not None:
            self.last_tweet_id = tweet_link
            return tweet_link
        else:
            return None

    @tasks.loop(minutes=10.0)
    async def check_tweets(self):
        if self.channel_id is None or self.role_id is None or self.username is None:
            return

        channel = self.bot.get_channel(self.channel_id)
        role = channel.guild.get_role(self.role_id)
        new_tweet = await self.fetch_latest_tweet()
        if new_tweet is not None:
            embed = discord.Embed(
                title=new_tweet,
                url=new_tweet,
                timestamp=datetime.datetime.now(),
                color=discord.Color.blue()
            )
            embed.set_author(name="DBSparkingNews")
            await channel.send(content=f"{role.mention} [New tweet from @{self.username}]({new_tweet})")

    @commands.command(name='set_channel')
    @commands.has_permissions(administrator=True)
    async def set_channel(self, ctx, channel: discord.TextChannel):
        self.channel_id = channel.id
        await ctx.send(f"Channel set to {channel.mention}")
        print(f"Channel set to {channel.id}")

    @commands.command(name='set_role')
    @commands.has_permissions(administrator=True)
    async def set_role(self, ctx, role: discord.Role):
        self.role_id = role.id
        await ctx.send(f"Role set to {role.mention}")
        print(f"Role set to {role.id}")

    @commands.command(name='set_username')
    @commands.has_permissions(administrator=True)
    async def set_username(self, ctx, username: str):
        self.username = username
        self.last_tweet_id = None  # Reset the last tweet ID to fetch new tweets from the start
        await ctx.send(f"Tracking tweets from @{username}")
        print(f"Tracking tweets from @{username}")


async def setup(bot):
    await bot.add_cog(TwitterCog(bot))
