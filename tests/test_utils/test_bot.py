import pytest
from utils.tg_bot import TelegramBot
from tools import file_input_output


# Get token and chat_id from file operator
file_operator = file_input_output.FileReadWrite()
newbot_token = file_operator.newbot_token
chat_id = file_operator.chat_id

rfd_token = file_operator.token
rfd_chat_id = file_operator.channel_id

@pytest.mark.utils
def test_tgbot():
    # Instantiate a tg bot instance
    tg_bot = TelegramBot(newbot_token, chat_id)

    # Set a testing msg content
    test_msg = 'Testing'
    return_msg = tg_bot.send_bot_msg(content_msg=test_msg)

    assert type(return_msg['message_id']) is int

    # Assert the return value of pin_message should be True
    returned_pin_bool = tg_bot.pin_message(pin_message_id=return_msg['message_id'])

    assert returned_pin_bool


@pytest.mark.utils
def test_bot_edit_msg():
    # Instantiate a tg bot instance
    tg_bot = TelegramBot(rfd_token, rfd_chat_id)
    
    test_msg = 'Testing'

    return_msg = tg_bot.send_bot_msg(content_msg=test_msg)

    msg_id = return_msg['message_id']
    
    test_msg_2 = 'Testing22222'

    return2_msg = tg_bot.edit_message(content_msg=test_msg_2, edit_msg_id=msg_id)

    assert type(return_msg['message_id']) is int