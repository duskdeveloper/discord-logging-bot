import discord
from discord.ext import commands
import json
import logging

class CommandHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger(__name__)
    
    @commands.group(name="log", invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def log_group(self, ctx):
        await ctx.send("Use `log help` to see available logging commands.")
    
    @log_group.command(name="help")
    async def log_help(self, ctx):
        embed = discord.Embed(
            title="Logging Commands",
            description="Advanced Discord Server Logging Bot",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="Configuration",
            value="`log setup` - Initial setup wizard\n"
                  "`log status` - Show current configuration\n"
                  "`log toggle <feature>` - Toggle logging features\n"
                  "`log prefix <prefix>` - Set command prefix",
            inline=False
        )
        
        embed.add_field(
            name="Channel Management",
            value="`log channel <type> <channel>` - Set log channel\n"
                  "`log channels` - List all log channels\n"
                  "`log clear <type>` - Clear log channel setting",
            inline=False
        )
        
        embed.add_field(
            name="Log Types",
            value="messages, edits, deletions, joins, leaves, roles, voice, default",
            inline=False
        )
        
        await ctx.send(embed=embed)
    
    @log_group.command(name="setup")
    @commands.has_permissions(administrator=True)
    async def log_setup(self, ctx):
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel
        
        embed = discord.Embed(
            title="Logging Setup Wizard",
            description="Let's configure your server logging settings!",
            color=discord.Color.green()
        )
        
        embed.add_field(
            name="Step 1",
            value="Please mention the channel where you want to log all activities (or type 'skip' to configure later):",
            inline=False
        )
        
        await ctx.send(embed=embed)
        
        try:
            response = await self.bot.wait_for('message', check=check, timeout=60.0)
            
            if response.content.lower() == 'skip':
                await ctx.send("Setup completed! Use `log channel` commands to configure specific log channels.")
                return
            
            if response.channel_mentions:
                channel = response.channel_mentions[0]
                
                config = self.bot.config_manager.get_guild_config(ctx.guild.id)
                config['log_channels']['default'] = channel.id
                self.bot.config_manager.save_guild_config(ctx.guild.id, config)
                
                embed = discord.Embed(
                    title="Setup Complete!",
                    description=f"Default log channel set to {channel.mention}",
                    color=discord.Color.green()
                )
                
                embed.add_field(
                    name="Next Steps",
                    value="Use `log toggle` commands to enable/disable specific logging features\n"
                          "Use `log channel` to set specific channels for different log types",
                    inline=False
                )
                
                await ctx.send(embed=embed)
            else:
                await ctx.send("No valid channel mentioned. Setup cancelled.")
        
        except Exception:
            await ctx.send("Setup timed out. Please run the command again.")
    
    @log_group.command(name="status")
    @commands.has_permissions(administrator=True)
    async def log_status(self, ctx):
        config = self.bot.config_manager.get_guild_config(ctx.guild.id)
        
        embed = discord.Embed(
            title="Logging Configuration",
            color=discord.Color.blue()
        )
        
        features = {
            'logging_enabled': 'Main Logging',
            'log_messages': 'Message Logging',
            'log_edits': 'Edit Logging',
            'log_deletions': 'Deletion Logging',
            'log_joins': 'Join Logging',
            'log_leaves': 'Leave Logging',
            'log_role_changes': 'Role Change Logging',
            'log_voice': 'Voice Activity Logging'
        }
        
        enabled_features = []
        disabled_features = []
        
        for key, name in features.items():
            if config.get(key, True):
                enabled_features.append(name)
            else:
                disabled_features.append(name)
        
        if enabled_features:
            embed.add_field(
                name="✅ Enabled Features",
                value="\n".join(enabled_features),
                inline=True
            )
        
        if disabled_features:
            embed.add_field(
                name="❌ Disabled Features",
                value="\n".join(disabled_features),
                inline=True
            )
        
        embed.add_field(
            name="Command Prefix",
            value=f"`{config.get('prefix', '!')}`",
            inline=False
        )
        
        channels_info = []
        for log_type, channel_id in config.get('log_channels', {}).items():
            channel = self.bot.get_channel(channel_id)
            if channel:
                channels_info.append(f"{log_type}: {channel.mention}")
        
        if channels_info:
            embed.add_field(
                name="Log Channels",
                value="\n".join(channels_info),
                inline=False
            )
        
        await ctx.send(embed=embed)
    
    @log_group.command(name="toggle")
    @commands.has_permissions(administrator=True)
    async def log_toggle(self, ctx, feature: str):
        valid_features = {
            'main': 'logging_enabled',
            'messages': 'log_messages',
            'edits': 'log_edits',
            'deletions': 'log_deletions',
            'joins': 'log_joins',
            'leaves': 'log_leaves',
            'roles': 'log_role_changes',
            'voice': 'log_voice'
        }
        
        if feature.lower() not in valid_features:
            await ctx.send(f"Invalid feature. Valid options: {', '.join(valid_features.keys())}")
            return
        
        config_key = valid_features[feature.lower()]
        config = self.bot.config_manager.get_guild_config(ctx.guild.id)
        
        current_value = config.get(config_key, True)
        new_value = not current_value
        
        config[config_key] = new_value
        self.bot.config_manager.save_guild_config(ctx.guild.id, config)
        
        status = "enabled" if new_value else "disabled"
        await ctx.send(f"✅ {feature.title()} logging has been **{status}**.")
    
    @log_group.command(name="channel")
    @commands.has_permissions(administrator=True)
    async def log_channel(self, ctx, log_type: str, channel: discord.TextChannel):
        valid_types = ['messages', 'edits', 'deletions', 'joins', 'leaves', 'roles', 'voice', 'default']
        
        if log_type.lower() not in valid_types:
            await ctx.send(f"Invalid log type. Valid options: {', '.join(valid_types)}")
            return
        
        config = self.bot.config_manager.get_guild_config(ctx.guild.id)
        
        if 'log_channels' not in config:
            config['log_channels'] = {}
        
        config['log_channels'][log_type.lower()] = channel.id
        self.bot.config_manager.save_guild_config(ctx.guild.id, config)
        
        await ctx.send(f"✅ {log_type.title()} logging channel set to {channel.mention}")
    
    @log_group.command(name="channels")
    @commands.has_permissions(administrator=True)
    async def log_channels(self, ctx):
        config = self.bot.config_manager.get_guild_config(ctx.guild.id)
        log_channels = config.get('log_channels', {})
        
        if not log_channels:
            await ctx.send("No log channels configured. Use `log channel` to set them up.")
            return
        
        embed = discord.Embed(
            title="Configured Log Channels",
            color=discord.Color.blue()
        )
        
        for log_type, channel_id in log_channels.items():
            channel = self.bot.get_channel(channel_id)
            if channel:
                embed.add_field(
                    name=log_type.title(),
                    value=channel.mention,
                    inline=True
                )
            else:
                embed.add_field(
                    name=log_type.title(),
                    value="❌ Channel not found",
                    inline=True
                )
        
        await ctx.send(embed=embed)
    
    @log_group.command(name="clear")
    @commands.has_permissions(administrator=True)
    async def log_clear(self, ctx, log_type: str):
        valid_types = ['messages', 'edits', 'deletions', 'joins', 'leaves', 'roles', 'voice', 'default']
        
        if log_type.lower() not in valid_types:
            await ctx.send(f"Invalid log type. Valid options: {', '.join(valid_types)}")
            return
        
        config = self.bot.config_manager.get_guild_config(ctx.guild.id)
        
        if 'log_channels' in config and log_type.lower() in config['log_channels']:
            del config['log_channels'][log_type.lower()]
            self.bot.config_manager.save_guild_config(ctx.guild.id, config)
            await ctx.send(f"✅ {log_type.title()} logging channel cleared.")
        else:
            await ctx.send(f"No {log_type.lower()} logging channel was configured.")
    
    @log_group.command(name="prefix")
    @commands.has_permissions(administrator=True)
    async def log_prefix(self, ctx, prefix: str):
        if len(prefix) > 5:
            await ctx.send("Prefix must be 5 characters or less.")
            return
        
        config = self.bot.config_manager.get_guild_config(ctx.guild.id)
        config['prefix'] = prefix
        self.bot.config_manager.save_guild_config(ctx.guild.id, config)
        
        await ctx.send(f"✅ Command prefix set to `{prefix}`")
    
    @commands.command(name="ping")
    async def ping(self, ctx):
        latency = round(self.bot.latency * 1000)
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"Bot latency: {latency}ms",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
    
    @commands.command(name="info")
    async def info(self, ctx):
        embed = discord.Embed(
            title="Advanced Discord Logging Bot",
            description="Comprehensive server logging with message tracking and administrative controls",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="Servers",
            value=str(len(self.bot.guilds)),
            inline=True
        )
        
        embed.add_field(
            name="Users",
            value=str(len(self.bot.users)),
            inline=True
        )
        
        embed.add_field(
            name="Features",
            value="• Message Logging\n• Edit/Delete Tracking\n• User Activity\n• Voice Logging\n• Role Changes\n• Configurable Settings",
            inline=False
        )
        
        embed.add_field(
            name="Commands",
            value="Use `log help` for all logging commands",
            inline=False
        )
        
        embed.set_footer(text="Built with discord.py")
        
        await ctx.send(embed=embed)
