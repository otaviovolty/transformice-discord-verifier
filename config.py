import os
from dotenv import load_dotenv

load_dotenv()

# Discord Configuration
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID', 0))
VERIFIED_ROLE_ID = int(os.getenv('VERIFIED_ROLE_ID', 0))
VERIFICATION_CHANNEL_ID = int(os.getenv('VERIFICATION_CHANNEL_ID', 0))

# Database Configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///verification.db')

# Code Configuration
CODE_EXPIRATION_MINUTES = int(os.getenv('CODE_EXPIRATION_MINUTES', 60))
CODE_LENGTH = int(os.getenv('CODE_LENGTH', 12))

# Security
MAX_VERIFICATION_ATTEMPTS = 5
RATE_LIMIT_SECONDS = 300  # 5 minutes
