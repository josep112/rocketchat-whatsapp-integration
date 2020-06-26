import json
import requests
from src.constants import *
class RocketMessageFactory:
    def __build_text_message(self):
        return {
            "token": self.visitor["visitor"]["token"],
            "rid": self.room["_id"],
            "msg": self.message["body"],
        }

    def __build_media_message(self):
        file_url = CHAT_GET_FILE.format(INSTANCE_ID, self.message["id"], self.message["type"], CHAT_API_TOKEN_MD5)
        file = requests.get(file_url)
        return file


    def __init__(self, message, room, visitor):
        self.message = message
        self.room = room
        self.visitor = visitor

    def build(self):
        if "file" in self.message and self.message["file"] is True:
            final_message = self.__build_media_message()
        else:
            final_message = self.__build_text_message()
        return final_message
