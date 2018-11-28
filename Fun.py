import json
import random
import aiohttp
import secrets
import discord
from discord.ext import commands

quotes = json.loads(open('quotes.json', encoding="utf8").read())


class Fun:
    def __init__(self, client):
        self.client = client

    # .8ball command.
    @commands.command(name='8ball',
                      description="Answers a yes/no question.",
                      brief="Answers from the beyond.",
                      aliases=['eight_ball', 'eightball', '8-ball', '8', '8b'],
                      pass_context=True)
    async def eight_ball(self, ctx):
        possible_responses = [
            'That is a resounding no',
            'It is not looking likely',
            'Too hard to tell',
            'It is quite possible',
            'Definitely',
        ]
        await self.client.say(random.choice(possible_responses) + ", " + ctx.message.author.mention)

    # .bitcoin command.
    @commands.command(name='Bitcoin',
                      description="Goes and fetches the current BTC price from CoinDesk.",
                      brief="Wanna know how much BTC is?",
                      aliases=['b', 'B', 'bitcoin'])
    async def bitcoin(self):
        url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
        async with aiohttp.ClientSession() as session:  # Async HTTP request
            raw_response = await session.get(url)
            response = await raw_response.text()
            response = json.loads(response)
            await self.client.say("Bitcoin price is: $" + response['bpi']['USD']['rate'])

    # .quote command.
    @commands.command(name='Quote',
                      description="Gives one of my quotes for all to read and enjoy!",
                      brief="Quote me bitches.",
                      aliases=['q', 'Q', 'quote'],
                      pass_context=True)
    async def quote(self):
        choice = secrets.choice(quotes)
        await self.client.say('{}'.format(choice))

    # .square command.
    @commands.command(name="Square",
                      description="Multiplies the given number by itself and returns the answer.",
                      brief="Square any reasonable number.",
                      aliases=['s', 'S', 'square'])
    async def square(self, number):
        squared_value = int(number) * int(number)
        await self.client.say(str(number) + " squared is " + str(squared_value))


def setup(client):
    client.add_cog(Fun(client))
