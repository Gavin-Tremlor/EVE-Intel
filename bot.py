import asyncio
import configparser
import discord
from discord.ext import commands
import json

import esi_routes
import log_reader
from system_status import System, IntelParser

evebot = commands.Bot(command_prefix=commands.when_mentioned_or('!'), description='An intel scraper for EVE')
config = configparser.ConfigParser()


class EVEbot:
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.intel_channels = {}

        game_channels = json.loads(config.get('intel', 'eve_channels'))
        self.intel_parser = IntelParser(game_channels)

        self.bot.loop.create_task(self.get_default_systems())
        self.bot.loop.create_task(self.scrape_to_systems())

    async def get_default_systems(self):
        await self.bot.wait_until_ready()
        channels = [ch for ch in self.bot.get_all_channels() if ch.name.startswith('intel-')]
        for chan in channels:
            system_name = chan.name[6:].swapcase()
            system_id = esi_routes.get_system_id(system_name)
            self.intel_channels[system_id] = (chan, System(system_id))
            print('Providing intel to {0}'.format(system_name))

        print(self.intel_channels)

    async def scrape_to_systems(self):
        await self.bot.wait_until_ready()
        self.intel_parser.start()

        await asyncio.sleep(5)  # this helps, i promise

        while not self.bot.is_closed:
            for system_id, (channel, system) in self.intel_channels.items():
                message, jumps, = "hi", 5
                self.bot.send_message(channel, message, tts=True if jumps < 9 else False)

            asyncio.sleep(2)

    @commands.command(pass_context=True, no_pm=True)
    async def watch(self, ctx, *, system: str):
        system_id = esi_routes.get_system_id(system)
        if system_id in self.intel_channels:
            await self.bot.say("already watching {0}".format(system))
            return

        channel = await self.bot.create_channel(ctx.message.server, 'intel-'+system.swapcase())
        self.intel_channels[system_id] = (channel, System(system_id))

    @commands.command(pass_context=True, no_pm=True)
    async def unwatch(self, ctx, *, system: str):
        system_id = esi_routes.get_system_id(system)
        await self.bot.delete_channel(self.intel_channels[system_id][0])
        self.intel_channels.pop(system_id)
        await self.bot.say("removing channel {0}".format(system))


@evebot.event
async def on_ready():
    print('Logged in as:{0} (ID: {0.id})'.format(evebot.user))

if __name__ == '__main__':
    config.read('eve-bot.cfg')
    evebot.add_cog(EVEbot(evebot))

    try:
        token = config['discord']['dev_token'] if 'dev_token' in config['discord'] else config['discord']['token']
        evebot.run(token)
    except KeyError:
        print("Could not find token in config file. Please check that 'token' exists under [discord].")
