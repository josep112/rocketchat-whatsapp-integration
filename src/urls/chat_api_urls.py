from src.constants import CHAT_API_URL, CHAT_API_TOKEN
def chat_api_url_factory(message):
    method = ""
    if "fileUpload" in message:
        if message["fileUpload"]["type"] == "audio/ogg":
            method = "sendPTT"
        else:
            method = "sendFile"
    else:
        method = "sendMessage"
    url = '{}/{}/?token={}'.format(CHAT_API_URL, method, CHAT_API_TOKEN)
    return url
