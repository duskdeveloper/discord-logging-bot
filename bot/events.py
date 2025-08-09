import discord
import logging
from datetime import datetime
from discord.ext import commands
from .utils import create_embed, format_timestamp, get_user_avatar, get_audit_log_entry

class EventHandler:
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger(__name__)
    
    async def on_ready(self):
        self.logger.info(f"{self.bot.user} has connected to Discord!")
        self.logger.info(f"Bot is in {len(self.bot.guilds)} guilds")
        
        activity = discord.Activity(
            type=discord.ActivityType.watching,
            name=f"{len(self.bot.guilds)} servers"
        )
        await self.bot.change_presence(activity=activity)
    
    async def on_message(self, message):
        if message.author.bot:
            return
        
        if not message.guild:
            return
        
        config = self.bot.config_manager.get_guild_config(message.guild.id)
        if not config.get('log_messages', True):
            return
        
        log_channel = await self.bot.get_log_channel(message.guild.id, 'messages')
        if not log_channel:
            return
        
        embed = create_embed(
            title="Message Sent",
            color=discord.Color.green(),
            timestamp=message.created_at
        )
        
        embed.add_field(
            name="Author",
            value=f"{message.author.mention} (`{message.author.id}`)",
            inline=True
        )
        
        embed.add_field(
            name="Channel",
            value=f"{message.channel.mention} (`{message.channel.id}`)",
            inline=True
        )
        
        if message.content:
            content = message.content
            if len(content) > 1024:
                content = content[:1021] + "..."
            embed.add_field(
                name="Content",
                value=content,
                inline=False
            )
        
        if message.attachments:
            attachments = "\n".join([att.url for att in message.attachments])
            embed.add_field(
                name="Attachments",
                value=attachments,
                inline=False
            )
        
        embed.set_thumbnail(url=get_user_avatar(message.author))
        embed.set_footer(text=f"Message ID: {message.id}")
        
        try:
            await log_channel.send(embed=embed)
        except discord.HTTPException as e:
            self.logger.error(f"Failed to log message: {e}")
    
    async def on_message_edit(self, before, after):
        if before.author.bot:
            return
        
        if not before.guild:
            return
        
        if before.content == after.content:
            return
        
        config = self.bot.config_manager.get_guild_config(before.guild.id)
        if not config.get('log_edits', True):
            return
        
        log_channel = await self.bot.get_log_channel(before.guild.id, 'edits')
        if not log_channel:
            return
        
        embed = create_embed(
            title="Message Edited",
            color=discord.Color.orange(),
            timestamp=after.edited_at or datetime.utcnow()
        )
        
        embed.add_field(
            name="Author",
            value=f"{before.author.mention} (`{before.author.id}`)",
            inline=True
        )
        
        embed.add_field(
            name="Channel",
            value=f"{before.channel.mention} (`{before.channel.id}`)",
            inline=True
        )
        
        if before.content:
            content = before.content
            if len(content) > 1024:
                content = content[:1021] + "..."
            embed.add_field(
                name="Before",
                value=content,
                inline=False
            )
        
        if after.content:
            content = after.content
            if len(content) > 1024:
                content = content[:1021] + "..."
            embed.add_field(
                name="After",
                value=content,
                inline=False
            )
        
        embed.add_field(
            name="Jump to Message",
            value=f"[Click here]({after.jump_url})",
            inline=False
        )
        
        embed.set_thumbnail(url=get_user_avatar(before.author))
        embed.set_footer(text=f"Message ID: {before.id}")
        
        try:
            await log_channel.send(embed=embed)
        except discord.HTTPException as e:
            self.logger.error(f"Failed to log message edit: {e}")
    
    async def on_message_delete(self, message):
        if message.author.bot:
            return
        
        if not message.guild:
            return
        
        config = self.bot.config_manager.get_guild_config(message.guild.id)
        if not config.get('log_deletions', True):
            return
        
        log_channel = await self.bot.get_log_channel(message.guild.id, 'deletions')
        if not log_channel:
            return
        
        embed = create_embed(
            title="Message Deleted",
            color=discord.Color.red(),
            timestamp=datetime.utcnow()
        )
        
        embed.add_field(
            name="Author",
            value=f"{message.author.mention} (`{message.author.id}`)",
            inline=True
        )
        
        embed.add_field(
            name="Channel",
            value=f"{message.channel.mention} (`{message.channel.id}`)",
            inline=True
        )
        
        embed.add_field(
            name="Created At",
            value=format_timestamp(message.created_at),
            inline=True
        )
        
        audit_entry = await get_audit_log_entry(
            message.guild, 
            discord.AuditLogAction.message_delete,
            target=message.author
        )
        
        if audit_entry and audit_entry.user != message.author:
            embed.add_field(
                name="Deleted By",
                value=f"{audit_entry.user.mention} (`{audit_entry.user.id}`)",
                inline=True
            )
        
        if message.content:
            content = message.content
            if len(content) > 1024:
                content = content[:1021] + "..."
            embed.add_field(
                name="Content",
                value=content,
                inline=False
            )
        
        if message.attachments:
            attachments = "\n".join([att.filename for att in message.attachments])
            embed.add_field(
                name="Attachments",
                value=attachments,
                inline=False
            )
        
        embed.set_thumbnail(url=get_user_avatar(message.author))
        embed.set_footer(text=f"Message ID: {message.id}")
        
        try:
            await log_channel.send(embed=embed)
        except discord.HTTPException as e:
            self.logger.error(f"Failed to log message deletion: {e}")
    
    async def on_member_join(self, member):
        config = self.bot.config_manager.get_guild_config(member.guild.id)
        if not config.get('log_joins', True):
            return
        
        log_channel = await self.bot.get_log_channel(member.guild.id, 'joins')
        if not log_channel:
            return
        
        embed = create_embed(
            title="Member Joined",
            color=discord.Color.green(),
            timestamp=datetime.utcnow()
        )
        
        embed.add_field(
            name="User",
            value=f"{member.mention} (`{member.id}`)",
            inline=True
        )
        
        embed.add_field(
            name="Account Created",
            value=format_timestamp(member.created_at),
            inline=True
        )
        
        embed.add_field(
            name="Member Count",
            value=str(member.guild.member_count),
            inline=True
        )
        
        embed.set_thumbnail(url=get_user_avatar(member))
        embed.set_footer(text=f"User ID: {member.id}")
        
        try:
            await log_channel.send(embed=embed)
        except discord.HTTPException as e:
            self.logger.error(f"Failed to log member join: {e}")
    
    async def on_member_remove(self, member):
        config = self.bot.config_manager.get_guild_config(member.guild.id)
        if not config.get('log_leaves', True):
            return
        
        log_channel = await self.bot.get_log_channel(member.guild.id, 'leaves')
        if not log_channel:
            return
        
        embed = create_embed(
            title="Member Left",
            color=discord.Color.red(),
            timestamp=datetime.utcnow()
        )
        
        embed.add_field(
            name="User",
            value=f"{member} (`{member.id}`)",
            inline=True
        )
        
        embed.add_field(
            name="Joined At",
            value=format_timestamp(member.joined_at) if member.joined_at else "Unknown",
            inline=True
        )
        
        embed.add_field(
            name="Member Count",
            value=str(member.guild.member_count),
            inline=True
        )
        
        if member.roles[1:]:
            roles = ", ".join([role.name for role in member.roles[1:]])
            if len(roles) > 1024:
                roles = roles[:1021] + "..."
            embed.add_field(
                name="Roles",
                value=roles,
                inline=False
            )
        
        embed.set_thumbnail(url=get_user_avatar(member))
        embed.set_footer(text=f"User ID: {member.id}")
        
        try:
            await log_channel.send(embed=embed)
        except discord.HTTPException as e:
            self.logger.error(f"Failed to log member leave: {e}")
    
    async def on_member_update(self, before, after):
        config = self.bot.config_manager.get_guild_config(before.guild.id)
        if not config.get('log_role_changes', True):
            return
        
        if before.roles == after.roles:
            return
        
        log_channel = await self.bot.get_log_channel(before.guild.id, 'roles')
        if not log_channel:
            return
        
        added_roles = set(after.roles) - set(before.roles)
        removed_roles = set(before.roles) - set(after.roles)
        
        embed = create_embed(
            title="Member Roles Updated",
            color=discord.Color.blue(),
            timestamp=datetime.utcnow()
        )
        
        embed.add_field(
            name="User",
            value=f"{after.mention} (`{after.id}`)",
            inline=True
        )
        
        if added_roles:
            roles = ", ".join([role.name for role in added_roles])
            embed.add_field(
                name="Roles Added",
                value=roles,
                inline=True
            )
        
        if removed_roles:
            roles = ", ".join([role.name for role in removed_roles])
            embed.add_field(
                name="Roles Removed",
                value=roles,
                inline=True
            )
        
        embed.set_thumbnail(url=get_user_avatar(after))
        embed.set_footer(text=f"User ID: {after.id}")
        
        try:
            await log_channel.send(embed=embed)
        except discord.HTTPException as e:
            self.logger.error(f"Failed to log role change: {e}")
    
    async def on_voice_state_update(self, member, before, after):
        config = self.bot.config_manager.get_guild_config(member.guild.id)
        if not config.get('log_voice', True):
            return
        
        log_channel = await self.bot.get_log_channel(member.guild.id, 'voice')
        if not log_channel:
            return
        
        embed = None
        
        if before.channel is None and after.channel is not None:
            embed = create_embed(
                title="Voice Channel Joined",
                color=discord.Color.green(),
                timestamp=datetime.utcnow()
            )
            embed.add_field(
                name="Channel",
                value=after.channel.name,
                inline=True
            )
        
        elif before.channel is not None and after.channel is None:
            embed = create_embed(
                title="Voice Channel Left",
                color=discord.Color.red(),
                timestamp=datetime.utcnow()
            )
            embed.add_field(
                name="Channel",
                value=before.channel.name,
                inline=True
            )
        
        elif before.channel != after.channel:
            embed = create_embed(
                title="Voice Channel Switched",
                color=discord.Color.orange(),
                timestamp=datetime.utcnow()
            )
            embed.add_field(
                name="From",
                value=before.channel.name,
                inline=True
            )
            embed.add_field(
                name="To",
                value=after.channel.name,
                inline=True
            )
        
        if embed:
            embed.add_field(
                name="User",
                value=f"{member.mention} (`{member.id}`)",
                inline=True
            )
            embed.set_thumbnail(url=get_user_avatar(member))
            embed.set_footer(text=f"User ID: {member.id}")
            
            try:
                await log_channel.send(embed=embed)
            except discord.HTTPException as e:
                self.logger.error(f"Failed to log voice activity: {e}")
    
    async def on_guild_join(self, guild):
        self.logger.info(f"Joined guild: {guild.name} ({guild.id})")
        self.bot.config_manager.create_default_config(guild.id)
    
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to use this command.")
            return
        
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Missing required argument: `{error.param.name}`")
            return
        
        if isinstance(error, commands.BadArgument):
            await ctx.send("Invalid argument provided.")
            return
        
        self.logger.error(f"Command error in {ctx.command}: {error}")
        await ctx.send("An error occurred while executing the command.")
