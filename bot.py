# Work with Python 3.6
import asyncio
import discord
from itertools import cycle
from discord.ext.commands import Bot

BOT_PREFIX = "."
client = Bot(command_prefix=BOT_PREFIX)

extensions = ['Events', 'Fun', 'Roller']

status = [
        'against the Fallen.',
        'against the Vex.',
        'against the Taken.',
        'against the Scourge.',
        'against the Cabal.'
    ]


@client.event
# Whenever a message is sent.
async def on_message(message):
    """
    The callback invoked when the bot receives a message.

    The only difference from the default is that when an error occurs,
    the message and error are printed here.

    :param message: The message that was received.
    """
    try:
        await client.process_commands(message)
    except Exception as error:
        print(message, error)


@client.event
async def on_ready():
    print('Bot Online.')


@client.event
# Rotates through status' every few minutes.
async def change_status():
    await client.wait_until_ready()
    msgs = cycle(status)

    while not client.is_closed:
        current_status = next(msgs)
        await client.change_presence(game=discord.Game(name=current_status))
        await asyncio.sleep(300)


@client.event
# Lists the currently connected servers' in console
async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print("Current servers:")
        for server in client.servers:
            print(server.name)
        await asyncio.sleep(600)


if __name__ == '__main__':
    for extension in extensions:
        try:
            client.load_extension(extension)
        except Exception as err:
            print('{} cannot be loaded. [{}]'.format(extension, err))

    client.loop.create_task(list_servers())
    client.loop.create_task(change_status())
    client.run(os.getenv('TOKEN'))
