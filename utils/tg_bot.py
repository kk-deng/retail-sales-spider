import telegram
from functools import wraps
from feapder.utils.log import log
import time


class TelegramBot:
    def __init__(self, token, chat_id):
        self.token = token
        self.chat_id = chat_id
        self.bot = telegram.Bot(token=self.token)

    def send_action(action):
        def decorator(func):
            @wraps(func)
            def command_func(self, *args, **kwargs):
                self.bot.send_chat_action(chat_id=self.chat_id, action=action)

                return func(self, *args, **kwargs)
            
            return command_func
        
        return decorator

    @send_action(telegram.ChatAction.TYPING)
    def send_bot_msg(
        self, 
        content_msg: str, 
        reply_to_msg_id: str or None=None
    ) -> telegram.Message or bool:
        """Given a string msg and msg_id, send msg to telegram chat_id.

        Args:
            content_msg (str): The string msg to send to telegram.
            reply_to_msg_id (str or None, optional): The msg_id to be quoted when sending msg. Defaults to None.

        Returns:
            telegram.Message or bool: Return a Message class or False
        """
        log_content = content_msg.replace("\n", "")
        log.warning(f'## Sending: {log_content}')

        try:
            returned_msg = self.bot.send_message(
                text=content_msg, 
                chat_id=self.chat_id,
                reply_to_message_id=reply_to_msg_id,
                # reply_markup=reply_markup,
                parse_mode=telegram.ParseMode.MARKDOWN
                )
            
            log.info('## Msg was sent successfully!')
            time.sleep(3)

            return returned_msg
        except Exception as e:
            log.warning(f'## Msg failed sending with error:\n{e}')

            raise Exception
