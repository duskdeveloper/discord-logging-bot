import discord
from datetime import datetime
import logging

def create_embed(title=None, description=None, color=None, timestamp=None):
    embed = discord.Embed(
        title=title,
        description=description,
        color=color or discord.Color.default(),
        timestamp=timestamp
    )
    return embed

def format_timestamp(dt):
    if dt is None:
        return "Unknown"
    return dt.strftime("%Y-%m-%d %H:%M:%S UTC")

def get_user_avatar(user):
    if user.avatar:
        return user.avatar.url
    return user.default_avatar.url

def truncate_text(text, max_length=1024):
    if len(text) > max_length:
        return text[:max_length-3] + "..."
    return text

async def safe_send(channel, content=None, embed=None):
    try:
        if content and embed:
            return await channel.send(content=content, embed=embed)
        elif content:
            return await channel.send(content=content)
        elif embed:
            return await channel.send(embed=embed)
    except discord.HTTPException as e:
        logging.error(f"Failed to send message to {channel}: {e}")
        return None

def has_permission(member, permission):
    if isinstance(permission, str):
        return getattr(member.guild_permissions, permission, False)
    return member.guild_permissions >= permission

def format_permissions(permissions):
    permission_names = []
    for perm, value in permissions:
        if value:
            permission_names.append(perm.replace('_', ' ').title())
    return permission_names

def get_channel_type(channel):
    if isinstance(channel, discord.TextChannel):
        return "Text Channel"
    elif isinstance(channel, discord.VoiceChannel):
        return "Voice Channel"
    elif isinstance(channel, discord.CategoryChannel):
        return "Category"
    elif isinstance(channel, discord.StageChannel):
        return "Stage Channel"
    elif isinstance(channel, discord.DMChannel):
        return "DM Channel"
    elif isinstance(channel, discord.GroupChannel):
        return "Group Channel"
    else:
        return "Unknown"

def format_member_status(member):
    status_map = {
        discord.Status.online: "🟢 Online",
        discord.Status.idle: "🟡 Idle",
        discord.Status.dnd: "🔴 Do Not Disturb",
        discord.Status.offline: "⚫ Offline"
    }
    return status_map.get(member.status, "❓ Unknown")

def escape_markdown(text):
    chars = ['*', '_', '`', '~', '\\', '|']
    for char in chars:
        text = text.replace(char, f'\\{char}')
    return text

def format_activity(activity):
    if activity is None:
        return "No activity"
    
    activity_types = {
        discord.ActivityType.playing: "Playing",
        discord.ActivityType.streaming: "Streaming",
        discord.ActivityType.listening: "Listening to",
        discord.ActivityType.watching: "Watching",
        discord.ActivityType.competing: "Competing in"
    }
    
    activity_type = activity_types.get(activity.type, "Unknown")
    return f"{activity_type} {activity.name}"

class RateLimiter:
    def __init__(self, max_requests=5, time_window=60):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = {}
    
    def is_rate_limited(self, user_id):
        now = datetime.utcnow().timestamp()
        
        if user_id not in self.requests:
            self.requests[user_id] = []
        
        user_requests = self.requests[user_id]
        user_requests[:] = [req for req in user_requests if now - req < self.time_window]
        
        if len(user_requests) >= self.max_requests:
            return True
        
        user_requests.append(now)
        return False

def format_file_size(size_bytes):
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"

def get_invite_code(invite_url):
    if "/" in invite_url:
        return invite_url.split("/")[-1]
    return invite_url

async def get_audit_log_entry(guild, action, target=None, limit=1):
    try:
        async for entry in guild.audit_logs(action=action, limit=limit):
            if target is None or entry.target == target:
                return entry
    except discord.Forbidden:
        pass
    return None
