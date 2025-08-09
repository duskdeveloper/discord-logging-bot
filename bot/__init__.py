"""
Advanced Discord Logging Bot

A comprehensive Discord bot for server logging with message tracking,
user activity monitoring, and administrative controls.
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__license__ = "MIT"

from .core import DiscordBot
from .config import ConfigManager
from .events import EventHandler
from .commands import CommandHandler
from .logger import BotLogger
from .utils import *

__all__ = [
    "DiscordBot",
    "ConfigManager", 
    "EventHandler",
    "CommandHandler",
    "BotLogger"
]