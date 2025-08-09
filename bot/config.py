import json
import os
import logging
from typing import Dict, Any

class ConfigManager:
    def __init__(self, config_dir="config"):
        self.config_dir = config_dir
        self.logger = logging.getLogger(__name__)
        
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        
        self.default_config_path = os.path.join(config_dir, "default_config.json")
        self.guild_configs = {}
        
        self.load_default_config()
    
    def load_default_config(self):
        try:
            with open(self.default_config_path, 'r') as f:
                self.default_config = json.load(f)
        except FileNotFoundError:
            self.default_config = self.get_default_config_template()
            self.save_default_config()
        except json.JSONDecodeError as e:
            self.logger.error(f"Error loading default config: {e}")
            self.default_config = self.get_default_config_template()
    
    def get_default_config_template(self):
        return {
            "prefix": "!",
            "logging_enabled": True,
            "log_messages": True,
            "log_edits": True,
            "log_deletions": True,
            "log_joins": True,
            "log_leaves": True,
            "log_role_changes": True,
            "log_voice": True,
            "log_channels": {}
        }
    
    def save_default_config(self):
        try:
            with open(self.default_config_path, 'w') as f:
                json.dump(self.default_config, f, indent=4)
        except Exception as e:
            self.logger.error(f"Error saving default config: {e}")
    
    def get_guild_config_path(self, guild_id):
        return os.path.join(self.config_dir, f"{guild_id}.json")
    
    def load_guild_config(self, guild_id):
        config_path = self.get_guild_config_path(guild_id)
        
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                self.guild_configs[guild_id] = config
                return config
        except FileNotFoundError:
            config = self.default_config.copy()
            self.guild_configs[guild_id] = config
            self.save_guild_config(guild_id, config)
            return config
        except json.JSONDecodeError as e:
            self.logger.error(f"Error loading guild config for {guild_id}: {e}")
            config = self.default_config.copy()
            self.guild_configs[guild_id] = config
            return config
    
    def save_guild_config(self, guild_id, config):
        config_path = self.get_guild_config_path(guild_id)
        
        try:
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=4)
            self.guild_configs[guild_id] = config
        except Exception as e:
            self.logger.error(f"Error saving guild config for {guild_id}: {e}")
    
    def get_guild_config(self, guild_id):
        if guild_id not in self.guild_configs:
            return self.load_guild_config(guild_id)
        return self.guild_configs[guild_id]
    
    def create_default_config(self, guild_id):
        config = self.default_config.copy()
        self.save_guild_config(guild_id, config)
        return config
    
    def update_guild_config(self, guild_id, updates):
        config = self.get_guild_config(guild_id)
        config.update(updates)
        self.save_guild_config(guild_id, config)
        return config
    
    def delete_guild_config(self, guild_id):
        config_path = self.get_guild_config_path(guild_id)
        
        try:
            if os.path.exists(config_path):
                os.remove(config_path)
            
            if guild_id in self.guild_configs:
                del self.guild_configs[guild_id]
                
            self.logger.info(f"Deleted config for guild {guild_id}")
        except Exception as e:
            self.logger.error(f"Error deleting guild config for {guild_id}: {e}")
    
    def get_all_guild_configs(self):
        configs = {}
        
        for filename in os.listdir(self.config_dir):
            if filename.endswith('.json') and filename != 'default_config.json':
                try:
                    guild_id = int(filename[:-5])
                    configs[guild_id] = self.get_guild_config(guild_id)
                except ValueError:
                    continue
        
        return configs
    
    def backup_configs(self, backup_path="config_backup"):
        import shutil
        
        try:
            if os.path.exists(backup_path):
                shutil.rmtree(backup_path)
            
            shutil.copytree(self.config_dir, backup_path)
            self.logger.info(f"Configs backed up to {backup_path}")
            return True
        except Exception as e:
            self.logger.error(f"Error backing up configs: {e}")
            return False
    
    def restore_configs(self, backup_path="config_backup"):
        import shutil
        
        try:
            if not os.path.exists(backup_path):
                self.logger.error(f"Backup path {backup_path} does not exist")
                return False
            
            if os.path.exists(self.config_dir):
                shutil.rmtree(self.config_dir)
            
            shutil.copytree(backup_path, self.config_dir)
            
            self.guild_configs.clear()
            self.load_default_config()
            
            self.logger.info(f"Configs restored from {backup_path}")
            return True
        except Exception as e:
            self.logger.error(f"Error restoring configs: {e}")
            return False
