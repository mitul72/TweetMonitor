import discord
from discord.ext import commands, tasks
import snscrape.modules.twitter as sntwitter
import os
import certifi
from utils.login import login

os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()


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
        if self.username is None:
            return []

        tweets = []
        scraper = sntwitter.TwitterUserScraper(self.username)
        for tweet in scraper.get_items():
            if self.last_tweet_id is not None and tweet.id <= self.last_tweet_id:
                break
            tweets.append({
                'date': tweet.date,
                'tweet_id': tweet.id,
                'content': tweet.content,
                'username': tweet.user.username,
                'url': tweet.url
            })

        if tweets:
            # Update last tweet ID to the latest tweet fetched
            print(f"Updating last tweet ID to {tweets[0]['tweet_id']}")
            print(f"last tweet: {tweets[0]}")
            self.last_tweet_id = tweets[0]['tweet_id']
        return tweets

    @tasks.loop(minutes=1.0)
    async def check_tweets(self):
        if self.channel_id is None or self.role_id is None or self.username is None:
            return

        channel = self.bot.get_channel(self.channel_id)
        role = channel.guild.get_role(self.role_id)
        new_tweets = await self.fetch_latest_tweet()
        if new_tweets:
            for tweet in new_tweets[::-1]:
                print(f"Processing tweet: {tweet}")
                embed = discord.Embed(
                    title=f"New tweet from @{tweet['username']}",
                    description=tweet['content'],
                    url=tweet['url'],
                    timestamp=tweet['date'],
                    color=discord.Color.blue()
                )
                embed.set_author(
                    name=tweet['username'], url=f"https://twitter.com/{tweet['username']}")
                await channel.send(content=f"{role.mention}", embed=embed)

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
