import os

ENV = 'dev'
bot_name = 'template'
bot_token = os.getenv(f'TG_BOT_TOKEN_{bot_name.upper()}_{ENV.upper()}')