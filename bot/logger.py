import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

class BotLogger:
    def __init__(self, log_dir="logs", max_file_size=10*1024*1024, backup_count=5):
        self.log_dir = log_dir
        self.max_file_size = max_file_size
        self.backup_count = backup_count
        
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        self.setup_loggers()
    
    def setup_loggers(self):
        log_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        self.setup_main_logger(log_format)
        self.setup_command_logger(log_format)
        self.setup_event_logger(log_format)
        self.setup_error_logger(log_format)
    
    def setup_main_logger(self, formatter):
        main_handler = RotatingFileHandler(
            os.path.join(self.log_dir, "bot.log"),
            maxBytes=self.max_file_size,
            backupCount=self.backup_count
        )
        main_handler.setFormatter(formatter)
        main_handler.setLevel(logging.INFO)
        
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.INFO)
        
        main_logger = logging.getLogger("bot")
        main_logger.setLevel(logging.INFO)
        main_logger.addHandler(main_handler)
        main_logger.addHandler(console_handler)
        
        logging.getLogger().addHandler(main_handler)
    
    def setup_command_logger(self, formatter):
        command_handler = RotatingFileHandler(
            os.path.join(self.log_dir, "commands.log"),
            maxBytes=self.max_file_size,
            backupCount=self.backup_count
        )
        command_handler.setFormatter(formatter)
        command_handler.setLevel(logging.INFO)
        
        command_logger = logging.getLogger("commands")
        command_logger.setLevel(logging.INFO)
        command_logger.addHandler(command_handler)
    
    def setup_event_logger(self, formatter):
        event_handler = RotatingFileHandler(
            os.path.join(self.log_dir, "events.log"),
            maxBytes=self.max_file_size,
            backupCount=self.backup_count
        )
        event_handler.setFormatter(formatter)
        event_handler.setLevel(logging.INFO)
        
        event_logger = logging.getLogger("events")
        event_logger.setLevel(logging.INFO)
        event_logger.addHandler(event_handler)
    
    def setup_error_logger(self, formatter):
        error_handler = RotatingFileHandler(
            os.path.join(self.log_dir, "errors.log"),
            maxBytes=self.max_file_size,
            backupCount=self.backup_count
        )
        error_handler.setFormatter(formatter)
        error_handler.setLevel(logging.ERROR)
        
        error_logger = logging.getLogger("errors")
        error_logger.setLevel(logging.ERROR)
        error_logger.addHandler(error_handler)
        
        logging.getLogger().addHandler(error_handler)
    
    def log_command(self, ctx, command_name, success=True):
        command_logger = logging.getLogger("commands")
        
        status = "SUCCESS" if success else "FAILED"
        message = (
            f"{status} - Command: {command_name} | "
            f"User: {ctx.author} ({ctx.author.id}) | "
            f"Guild: {ctx.guild.name if ctx.guild else 'DM'} ({ctx.guild.id if ctx.guild else 'N/A'}) | "
            f"Channel: {ctx.channel.name if hasattr(ctx.channel, 'name') else 'DM'} ({ctx.channel.id})"
        )
        
        command_logger.info(message)
    
    def log_event(self, event_name, details):
        event_logger = logging.getLogger("events")
        event_logger.info(f"{event_name} - {details}")
    
    def log_error(self, error, context=None):
        error_logger = logging.getLogger("errors")
        
        if context:
            error_logger.error(f"Context: {context} | Error: {error}")
        else:
            error_logger.error(f"Error: {error}")
    
    def log_guild_action(self, guild, action, details):
        main_logger = logging.getLogger("bot")
        message = f"Guild: {guild.name} ({guild.id}) | Action: {action} | Details: {details}"
        main_logger.info(message)
    
    def log_user_action(self, user, action, details):
        main_logger = logging.getLogger("bot")
        message = f"User: {user} ({user.id}) | Action: {action} | Details: {details}"
        main_logger.info(message)
    
    def get_log_stats(self):
        stats = {}
        
        for log_file in ["bot.log", "commands.log", "events.log", "errors.log"]:
            file_path = os.path.join(self.log_dir, log_file)
            
            if os.path.exists(file_path):
                stats[log_file] = {
                    "size": os.path.getsize(file_path),
                    "modified": datetime.fromtimestamp(os.path.getmtime(file_path))
                }
            else:
                stats[log_file] = {
                    "size": 0,
                    "modified": None
                }
        
        return stats
    
    def clear_logs(self):
        try:
            for log_file in os.listdir(self.log_dir):
                if log_file.endswith('.log'):
                    file_path = os.path.join(self.log_dir, log_file)
                    open(file_path, 'w').close()
            
            main_logger = logging.getLogger("bot")
            main_logger.info("All log files cleared")
            return True
        except Exception as e:
            main_logger = logging.getLogger("bot")
            main_logger.error(f"Error clearing logs: {e}")
            return False
