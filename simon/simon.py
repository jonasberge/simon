import discord


class Simon(discord.Client):

    async def on_ready(self):
        async for guild in self.fetch_guilds(limit=100):
            print(guild.name)
