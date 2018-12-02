import discord
import json
import os
from discord.ext import commands


class Levels:
    def __init__(self, client):
        self.client = client

    async def on_member_join(self, member):
        with open('users.json', 'r') as f:
            users = json.load(f)

        await self.update_data(users, member)

        with open('users.json', 'w') as f:
            json.dump(users, f)

    async def on_message(self, message):
        with open('users.json', 'r') as f:
            users = json.load(f)

        await self.update_data(users, message.author)
        await self.add_experience(users, message.author, 5)
        await self.level_up(users, message.author, message.channel)

        with open('users.json', 'w') as f:
            json.dump(users, f)

    @staticmethod
    async def update_data(users, user):
        if user.id not in users:
            users[user.id] = {}
            users[user.id]['experience'] = 0
            users[user.id]['level'] = 1

    @staticmethod
    async def add_experience(users, user, exp):
        users[user.id]['experience'] += exp

    async def level_up(self, users, user, channel):
        experience = users[user.id]['experience']
        lvl_start = users[user.id]['level']
        lvl_end = int(experience ** (1/4))

        if lvl_start < lvl_end:
            await self.client.send_message(channel, '{} has leveld up to level {}'.format(user.mention, lvl_end))
            users[user.id]['level'] = lvl_end


def setup(client):
    client.add_cog(Levels(client))
