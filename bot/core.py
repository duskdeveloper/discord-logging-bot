import discord
from discord.ext import commands
import logging
import json
import os
from .config import ConfigManager
from .events import EventHandler
from .commands import CommandHandler

class DiscordBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(
            command_prefix="!",
            intents=intents,
            help_command=None,
            case_insensitive=True
        )
        
        self.config_manager = ConfigManager()
        self.event_handler = EventHandler(self)
        self.command_handler = CommandHandler(self)
        self.logger = logging.getLogger(__name__)
        
        self.setup_events()
    
    async def setup_hook(self):
        await self.add_cog(self.command_handler)
    
    async def get_prefix(self, message):
        if not message.guild:
            return "!"
        
        config = self.config_manager.get_guild_config(message.guild.id)
        return config.get('prefix', '!')
    
    def setup_events(self):
        @self.event
        async def on_ready():
            await self.event_handler.on_ready()
        
        @self.event
        async def on_message(message):
            await self.event_handler.on_message(message)
            await self.process_commands(message)
        
        @self.event
        async def on_message_edit(before, after):
            await self.event_handler.on_message_edit(before, after)
        
        @self.event
        async def on_message_delete(message):
            await self.event_handler.on_message_delete(message)
        
        @self.event
        async def on_member_join(member):
            await self.event_handler.on_member_join(member)
        
        @self.event
        async def on_member_remove(member):
            await self.event_handler.on_member_remove(member)
        
        @self.event
        async def on_member_update(before, after):
            await self.event_handler.on_member_update(before, after)
        
        @self.event
        async def on_voice_state_update(member, before, after):
            await self.event_handler.on_voice_state_update(member, before, after)
        
        @self.event
        async def on_guild_join(guild):
            await self.event_handler.on_guild_join(guild)
        
        @self.event
        async def on_command_error(ctx, error):
            await self.event_handler.on_command_error(ctx, error)
    
    async def get_log_channel(self, guild_id, log_type):
        config = self.config_manager.get_guild_config(guild_id)
        
        if not config.get('logging_enabled', True):
            return None
        
        channel_id = config.get('log_channels', {}).get(log_type)
        if not channel_id:
            channel_id = config.get('log_channels', {}).get('default')
        
        if channel_id:
            return self.get_channel(channel_id)
        
        return None
