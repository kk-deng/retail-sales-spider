import telegram
from feapder.utils.log import log

class TelegramBot:
    def __init__(self, token):
        self.token = token
        self.bot = telegram.Bot(token=self.token)

    def send_action(action):
        def decorator(func):
            @wraps(func)
            def command_func(self, *args, **kwargs):
                self.bot.send_action(chat_id=self.file_operator.chat_id, action=action)

                return func(self, *args, **kwargs)
            
            return command_func
        
        return decorator

    @send_action(telegram.ChatAction.TYPING)
    def send_bot_msg(
        self, content_msg: str, 
        reply_to_msg_id: str or None
    ) -> str or bool:
        log_content = content_msg.replace("\n", "")
        log.warning(f'## Sending: {log_content}')