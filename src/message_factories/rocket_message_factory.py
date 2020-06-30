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
        get_file_endpoint = CHAT_API_URL + CHAT_GET_FILE.format(self.message["id"], CHAT_API_TOKEN)
        file = requests.get(get_file_endpoint)
        media_url = json.loads(file.text)["url"]
        body = "{}\n{}".format(self.message["body"], media_url)
        return {
            "token": self.visitor["visitor"]["token"],
            "rid": self.room["_id"],
            "msg": body,
        }


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
