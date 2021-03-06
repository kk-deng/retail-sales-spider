import telegram
from typing import Optional
from functools import wraps
from feapder.utils.log import log
import time


class TelegramBot:
    def __init__(self, token, chat_id, parse_mode: bool=True):
        self.token = token
        self.chat_id = chat_id
        self.bot = telegram.Bot(token=self.token)
        self.parse_mode = parse_mode

    def _send_action(action):
        def decorator(func):
            @wraps(func)
            def command_func(self, *args, **kwargs):
                self.bot.send_chat_action(chat_id=self.chat_id, action=action)

                return func(self, *args, **kwargs)
            
            return command_func
        
        return decorator

    @_send_action(telegram.ChatAction.TYPING)
    def send_bot_msg(
        self, 
        content_msg: str, 
        reply_to_msg_id: Optional[str]=None,
        markup_url: str=None,
    ) -> telegram.Message:
        """Given a string msg and msg_id, send msg to telegram chat_id.

        Args:
            content_msg (str): The string msg to send to telegram.
            reply_to_msg_id (str or None, optional): The msg_id to be quoted when sending msg. Defaults to None.

        Returns:
            telegram.Message: Return a Message object sent successfully
        """
        log_content = content_msg.replace("\n", "")
        log.warning(f'## Sending: {log_content}')

        if markup_url:
            keyboard = [
                [
                    telegram.InlineKeyboardButton("Open Direct Link", url=markup_url),
                ],
            ]
            reply_markup = telegram.InlineKeyboardMarkup(keyboard)
        else:
            reply_markup = None

        try:
            if self.parse_mode:
                returned_msg = self.bot.send_message(
                    text=content_msg, 
                    chat_id=self.chat_id,
                    reply_to_message_id=reply_to_msg_id,
                    reply_markup=reply_markup,
                    parse_mode=telegram.ParseMode.MARKDOWN
                )
            else:
                returned_msg = self.bot.send_message(
                    text=content_msg, 
                    chat_id=self.chat_id,
                    reply_to_message_id=reply_to_msg_id,
                    reply_markup=reply_markup,
                )
            
            log.info('## Msg was sent successfully!')
            time.sleep(3)

            return returned_msg
        except Exception as e:
            log.warning(f'## Msg failed sending with error:\n{e}')
            return False
            # raise Exception
    
    def pin_message(self, pin_message_id: int) -> bool:
        """Pin a telegram message with a pin_message_id.

        Args:
            pin_message_id (int): The message id to be pinned

        Returns:
            bool: Return True if the message is pinned successfully
        """
        return self.bot.pin_chat_message(
            chat_id=self.chat_id, 
            message_id=pin_message_id
        )

    def edit_message(
        self,
        content_msg: str, 
        edit_msg_id: str=None,
        markup_url: str=None,
    ) -> telegram.Message:
        """Given a string msg and msg_id, update the sent msg in chat_id.

        Args:
            content_msg (str): The string msg to send to telegram.
            edit_msg_id (str or None): The msg_id to be updated.

        Returns:
            telegram.Message: Return a Message object updated successfully
        """
        if markup_url:
            keyboard = [
                [
                    telegram.InlineKeyboardButton("Open Direct Link", url=markup_url),
                ],
            ]
            reply_markup = telegram.InlineKeyboardMarkup(keyboard)
        else:
            reply_markup = None
        
        # Try to send message to the telegram chat
        try:
            if self.parse_mode:
                returned_msg = self.bot.edit_message_text(
                    text=content_msg, 
                    chat_id=self.chat_id,
                    message_id=edit_msg_id,
                    reply_markup=reply_markup,
                    parse_mode=telegram.ParseMode.MARKDOWN
                )
            else:
                returned_msg = self.bot.edit_message_text(
                    text=content_msg, 
                    chat_id=self.chat_id,
                    message_id=edit_msg_id,
                    reply_markup=reply_markup,
                )
            
            # log.info('## Msg was edited successfully!')
            time.sleep(3)

            return returned_msg
        except Exception as e:
            log.warning(f'## Msg failed sending with error:\n{e}')

            raise Exception
