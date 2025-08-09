# discord-logging-bot
🔍 Advanced Discord logging bot with comprehensive server monitoring, message tracking, and administrative controls


# Advanced Discord Logging Bot

A comprehensive Discord bot for server logging with message tracking, user activity monitoring, and administrative controls.

## Features

### Message Logging
- Real-time message logging from all channels
- Message edit tracking with before/after content
- Message deletion logging with original content
- Attachment tracking and logging

### User Activity Monitoring
- Member join/leave notifications
- Role change tracking
- Voice channel activity logging
- User status and activity monitoring

### Administrative Controls
- Configurable logging channels for different event types
- Toggle individual logging features on/off
- Customizable command prefixes
- Per-server configuration storage
- Setup wizard for easy initial configuration

### Advanced Features
- Multiple log channel support (separate channels for different log types)
- Rich embed formatting with timestamps and user avatars
- Comprehensive error handling and logging
- Rate limiting and permission checks
- Modular code structure for easy maintenance

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Discord.py library
- A Discord bot token from the Discord Developer Portal

### Installation

1. Clone the repository:
```bash
git clone https://github.com/duskdeveloper/discord-logging-bot.git
cd discord-logging-bot
```

2. Install dependencies:
```bash
pip install discord.py
```

3. Create a Discord Application and Bot:
   - Go to https://discord.com/developers/applications
   - Click "New Application" and give it a name
   - Go to the "Bot" section
   - Click "Add Bot"
   - Copy the bot token

4. Set up environment variables:
```bash
export DISCORD_BOT_TOKEN="your_bot_token_here"
```

Or create a `.env` file:
```
DISCORD_BOT_TOKEN=your_bot_token_here
```

5. Invite the bot to your server:
   - In the Discord Developer Portal, go to "OAuth2" > "URL Generator"
   - Select "bot" scope
   - Select required permissions: Administrator (or specific permissions)
   - Use the generated URL to invite the bot

6. Run the bot:
```bash
python main.py
```

## Configuration

### Quick Setup
Use the setup wizard for easy configuration:
```
!log setup
```

### Manual Configuration

#### Setting Log Channels
```
!log channel <type> #channel-name
```

Available log types:
- `messages` - Regular message logging
- `edits` - Message edit tracking
- `deletions` - Message deletion tracking
- `joins` - Member join notifications
- `leaves` - Member leave notifications
- `roles` - Role change tracking
- `voice` - Voice channel activity
- `default` - Fallback channel for all log types

#### Toggle Features
```
!log toggle <feature>
```

Available features:
- `main` - Enable/disable all logging
- `messages` - Message logging
- `edits` - Edit tracking
- `deletions` - Deletion tracking
- `joins` - Join notifications
- `leaves` - Leave notifications
- `roles` - Role changes
- `voice` - Voice activity

#### View Configuration
```
!log status
```

#### Change Prefix
```
!log prefix <new_prefix>
```

## Commands

### Administrative Commands (Administrator Required)
- `!log help` - Show all available commands
- `!log setup` - Run the setup wizard
- `!log status` - View current configuration
- `!log toggle <feature>` - Toggle logging features
- `!log channel <type> <channel>` - Set log channel for specific type
- `!log channels` - List all configured log channels
- `!log clear <type>` - Clear log channel setting
- `!log prefix <prefix>` - Change command prefix

### General Commands
- `!ping` - Check bot latency
- `!info` - Display bot information

## File Structure

```
├── bot/
│   ├── __init__.py
│   ├── core.py          # Main bot class
│   ├── events.py        # Event handlers
│   ├── commands.py      # Command handlers
│   ├── config.py        # Configuration manager
│   ├── logger.py        # Logging system
│   └── utils.py         # Utility functions
├── config/
│   └── default_config.json  # Default configuration
├── main.py              # Entry point
└── README.md
```

## Configuration Files

The bot automatically creates configuration files in the `config/` directory:
- `default_config.json` - Default settings for all servers
- `{guild_id}.json` - Per-server configuration files

## Logging Types

### Message Events
- New messages with content and attachments
- Message edits with before/after comparison
- Message deletions with original content
- Direct message tracking (optional)

### User Events
- Member joins with account age
- Member leaves with role information
- Role assignments and removals
- Nickname changes
- Status updates

### Voice Events
- Voice channel joins
- Voice channel leaves
- Voice channel switches
- Mute/deafen status changes

## Permissions

The bot requires the following Discord permissions:
- Read Messages
- Send Messages
- Embed Links
- Read Message History
- View Channels
- Manage Messages (for advanced features)
- View Audit Log (for detailed logging)

## Support

For issues and feature requests, please open an issue on GitHub.
