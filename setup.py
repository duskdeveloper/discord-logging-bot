#!/usr/bin/env python3
"""
Setup script for Advanced Discord Logging Bot
"""

import os
import sys
import subprocess
import shutil

def install_dependencies():
    """Install required Python packages"""
    print("Installing discord.py...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "discord.py"])
        print("✓ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("✗ Failed to install dependencies")
        return False
    return True

def create_directories():
    """Create necessary directories"""
    directories = ["config", "logs"]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✓ Created {directory}/ directory")
        else:
            print(f"✓ {directory}/ directory already exists")

def setup_env_file():
    """Setup environment file from example"""
    if not os.path.exists(".env") and os.path.exists("example.env"):
        shutil.copy("example.env", ".env")
        print("✓ Created .env file from example")
        print("⚠ Please edit .env file and add your Discord bot token")
        return False
    elif os.path.exists(".env"):
        print("✓ .env file already exists")
        return True
    else:
        print("⚠ Please create a .env file with your Discord bot token")
        return False

def main():
    """Main setup function"""
    print("Setting up Advanced Discord Logging Bot...")
    print("=" * 50)
    
    success = True
    
    if not install_dependencies():
        success = False
    
    create_directories()
    
    if not setup_env_file():
        success = False
    
    print("=" * 50)
    
    if success:
        print("✓ Setup completed successfully!")
        print("\nNext steps:")
        print("1. Edit .env file and add your Discord bot token")
        print("2. Run: python main.py")
        print("3. Use !log setup in your Discord server")
    else:
        print("⚠ Setup completed with warnings")
        print("Please check the messages above and resolve any issues")

if __name__ == "__main__":
    main()