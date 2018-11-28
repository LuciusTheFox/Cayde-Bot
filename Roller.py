import re
import discord
import argparse

from discord.ext import commands
# Dice-rolling related imports
from dice_tools.rollers import DiceRoller
from dice_tools.rollers.statistical import MaxRoller, MinRoller, AvgRoller
from dice_tools.exceptions import DiceToolsError

# RegEx patterns used in this script
patterns = {}

patterns["sign"] = r"[\+\-]"
patterns["dice"] = r"\d+d(\d+~)?\d+(:\w+)?"
patterns["mod"] = r"\d+"

patterns["single roll"] = r"{0}?\s*({1}|{2})\b".format(patterns["sign"], patterns["dice"], patterns["mod"])
patterns["simple roll"] = r"({0})+".format(patterns["single roll"])

# This is that argument parser that will process roll flags.
roll_preparser = argparse.ArgumentParser(prog='!roll')
roll_preparser.add_argument('-b', '--brief', action='store_true')
stat_flags = roll_preparser.add_mutually_exclusive_group()
stat_flags.add_argument('-avg', action='store_true')
stat_flags.add_argument('-max', action='store_true')
stat_flags.add_argument('-min', action='store_true')


class Roller:
    def __init__(self, client):
        self.client = client

    def construct_message(self, roller, author, detail=True):
        """Constructs the result message for a random dice roll as as a string.

        :param roller: The dice roller object with the roll result
        :param author: The original message author
        :param detail: Flag indicating whether or not to include roll details.
        """
        if detail == False:
            message = "{0} rolled a total of `{1}`.".format(author.mention, roller.result)
        else:
            details = '; '.join(roller.roll_detail_strings())
            message = "{0} rolled a total of `{1}` from `{2}`.".format(author.mention, roller.result, details)
        return message


    # .roll command.
    @commands.command(description='Rolls dice, made by GitHub user modimore',
                      brief="General dice roller.",
                      aliases=['r'],
                      pass_context=True)
    async def roll(self, ctx, *, roll: str):
        """
        Rolls dice based on user messages.
        Reports result back to channel.

        Currently supports:
            (x1)d(y1) + (x2)d(y2) + ... + (xN)d(yN) + m1 + m2 + ... +  mN
            with the following dice-specific options applied as '(x)d(y):opt':
                advantage (adv, a)
                disadvantage (disadv, da, d)
                best (b, high, h)
                worst (w, low, l)
            and the following roll-global flags added as '-flagname'
            to the start of the whole roll:
                max
                min
                avg
        """
        author = ctx.message.author

        try:
            flags, _ = roll_preparser.parse_known_args(roll.split())
            roll = re.sub(r"\s*\-{1,2}[^\W\d]+\s*", "", roll)

            if flags.max:
                roller = MaxRoller(roll)
                await self.client.say(
                    "{0}, `{2}` is the maximum possible result of `{1}`.".format(author.mention, roll, roller.result))
            elif flags.min:
                roller = MinRoller(roll)
                await self.client.say(
                    "{0}, `{2}` is the minimum possible result of `{1}`.".format(author.mention, roll, roller.result))
            elif flags.avg:
                roller = AvgRoller(roll)
                await self.client.say(
                    "{0}, `{2}` is (close to) the average result of `{1}`.".format(author.mention, roll, roller.result))
            elif re.match(patterns["simple roll"], roll):
                # Handle a simple roll
                # 'XdY + ZdW + ... + M + N'
                roller = DiceRoller(roll)
                await self.client.say(self.construct_message(roller, author, not flags.brief))
            else:
                await self.client.say(
                    "{0}, the specification you provided did not match any of our roll patterns. Please try again."
                    .format(author.mention))
        except DiceToolsError as err:
            await self.client.say(
                "{0}, your roll has produced an error with the following message:\n**{1}**"
                "\nPlease fix your roll and try again.".format(author.mention, err.get_message()))
        except Exception as err:
            # If an exception is raised, have the bot say so in the channel
            await self.client.say("{0}, an unexpected error has occured: {1}.".format(author.mention, err))
            raise err


def setup(client):
    client.add_cog(Roller(client))
