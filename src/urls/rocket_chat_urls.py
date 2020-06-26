from src.constants import *

def create_visitor(message):
    return {
        "visitor":{
            "name": message["senderName"],
            "email": "",
            "token": message["chatId"].replace('@', '-'),
            "department": "",
            "customFields": [],
        }
    }

def get_visitor_url():
    return "{}{}".format(ROCKET_URL_PREFIX, ROCKET_VISITOR_POSTFIX)

def get_room_url(message):
    chat_id = message["chatId"].replace('@', '-')
    url="{}{}?token={}&rid={}".format(ROCKET_URL_PREFIX, ROCKET_GET_ROOM_POSTFIX, chat_id, chat_id)
    return url

def get_rocket_message_url():
    return "{}{}".format(ROCKET_URL_PREFIX, ROCKET_MESSAGE_URL_POSTFIX)

