#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

import logging.config
import os

# generate directory for logs
log_dir = 'logs'
if os.path.isdir(log_dir) == False:
    os.mkdir(log_dir)

logging.config.fileConfig('logging.ini', disable_existing_loggers=False)
logger = logging.getLogger('bot_frontend')


import datetime as dt
import time
import json
import copy
import os
import sys
import traceback as tb
import re

import pandas as pd
import numpy as np

from telegram import (CallbackQuery, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardMarkup, 
                      InlineKeyboardButton, LabeledPrice)

from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler, CallbackQueryHandler, PreCheckoutQueryHandler,
                         PicklePersistence)

import config as cfg
from decorators import send_bot_typing, collect_step_to_db


# init globals
CONFIG_PATH = "config.yaml"
MENU_KEYBOARD = ReplyKeyboardMarkup([
        ['Test']
    ], resize_keyboard=True)

PARSE_MODE = 'HTML'


@send_bot_typing
def start_command(update, context):
    
    user_data = update.message.to_dict()
    logger.info('New user: ' + str(user_data))
    
    update.message.reply_text(
        text='''Hello, my friend! 👋''',
        parse_mode=PARSE_MODE,
        reply_markup=MENU_KEYBOARD
    )
    
    return 'START'


@send_bot_typing
def cancel_command(update, context):

    user_data = context.user_data
    user_data.clear()
    
    update.message.reply_text( 
        text='Bot stopped ⭕️', 
        parse_mode=PARSE_MODE,
        reply_markup=ReplyKeyboardRemove()
        )

    return ConversationHandler.END


@send_bot_typing
def error_callback(update, context):

    message = tb.format_exc()
    logger.error('Error traceback: %s'%message)
    
    logger.warning('Update "%s" caused error "%s"', update, context.error)

    
@send_bot_typing
def test_button(update, context):
    message_text = '"Test" button was pressed 👆'
    logger.info(message_text)
    update.message.reply_text(text=message_text, parse_mode=PARSE_MODE)
    
    return 'START'


@send_bot_typing
def echo(update, context):
    user_text = update.message.text
    logger.info(f'Echo: "{user_text}"')
    
    update.message.reply_text(text=user_text, parse_mode=PARSE_MODE)
    
    return 'START'
        



def main():

    system_dir = 'system_files'
    if os.path.isdir(system_dir) == False:
        os.mkdir(system_dir)
    
    # save conversations states with users
    persistence = PicklePersistence(filename=f'{system_dir}/conversation_states')
    
    updater = Updater(cfg.bot_token, persistence=persistence)
    dp = updater.dispatcher
    
    
    available_commands = [
        CommandHandler('start', start_command),
        CommandHandler('cancel', cancel_command),
    ]

    conv_handler = ConversationHandler(
        entry_points=available_commands,

        states={
            
            'START': [
                MessageHandler(Filters.regex('Test'), test_button),
                MessageHandler(Filters.text, echo),
            ],
            
        },

        fallbacks=[CommandHandler('cancel', cancel_command)],
        name="user_conversation",
        persistent=True,
        allow_reentry=True,
        #run_async=True
        #per_message=True

    )

    dp.add_handler(conv_handler)
    dp.add_error_handler(error_callback)

    # Start the Bot
    try:
        updater.start_polling(poll_interval=1)
    except:
        logger.error('Polling error', exc_info=True)

    updater.idle()

    
if __name__ == '__main__':
    try:
        main()
    except:
        logger.error('General error', exc_info=True)