import pytest
from utils.tg_bot import TelegramBot
from tools import file_input_output


# Get token and chat_id from file operator
file_operator = file_input_output.FileReadWrite()
newbot_token = file_operator.newbot_token
chat_id = file_operator.chat_id


@pytest.mark.utils
def test_tgbot():
    # Instantiate a tg bot instance
    tg_bot = TelegramBot(newbot_token, chat_id)

    # Set a testing msg content
    test_msg = 'Testing'
    return_msg = tg_bot.send_bot_msg(content_msg=test_msg)

    assert type(return_msg['message_id']) is int
