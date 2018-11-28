import discord
from discord.ext import commands


class Events:
    def __init__(self, client):
        self.client = client

    # When bot is ready from launch.
    async def on_ready(self):
        print("Logged in as " + self.client.user.name)


def setup(client):
    client.add_cog(Events(client))
