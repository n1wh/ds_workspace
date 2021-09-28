TYPING_TIMEOUT = 2

# === DECORATORS ===
def send_bot_typing(func):
    """ Wrapper for sending "bot typing" action on each step """
    
    def wrapper(*args, **kwargs):
        update = args[0]
        context = args[1]
        
        # handling if an inline button with the callback data was clicked
        if update.callback_query != None:
            update = update.callback_query

        context.bot.send_chat_action(chat_id=update.message.chat_id, action='typing', timeout=TYPING_TIMEOUT)
        
        return func(*args, **kwargs)
        
    return wrapper


def collect_step_to_db(func):
    """ Wrapper for collecting step details on each step """
    
    def wrapper(*args, **kwargs):
        update = args[0]
        context = args[1]

        # handling if an inline button with the callback data was clicked
        if update.callback_query != None:
            update = update.callback_query
            user_data = update.to_dict()
            user_data['date'] = int(time.time()) # handle timestamp #user_data['message']['date'] # pop up this message timestamp on one level higher
            #logger.info('Callback update: %s'%str(update))           
            
        else:
            user_data = update.message.to_dict()

        #back.insert_user_activity(step_name=func.__name__, user_data=user_data)
        
        return func(*args, **kwargs)

    return wrapper