from flask import Flask, request
import requests
import os
import json
import uuid
from src.message_factories.chat_api_message_factory import ChatApiMessageFactory
from src.message_factories.rocket_message_factory import RocketMessageFactory
from src.urls.chat_api_urls import chat_api_url_factory
from src.urls.rocket_chat_urls import *
from src.visitor_management.visitor_map import *

app = Flask(__name__)


@app.route('/msg_snd', methods=["GET", "POST"])
def msg_snd():
    if request.method == 'POST':
        # Create a new message factory to handle different types of
        # possible messages incoming form RocketChat
        messageFactory = ChatApiMessageFactory()

        # Create the header to send along with our request
        headers = {"Content-type": "application/json"}

        # extract the payload received via post
        received_message = request.json

        # get hold of the messages array inside the payload sent by
        # rocket chat. Tipically this array contains only one message.
        # I don't know why...
        messages = received_message["messages"]

        # Extract the message destination from the object. It is in the
        # format 5551998121654-c.us
        message_destination = received_message["visitor"]["token"].split(
            "-")[0]

        # iterate through the messages array. Again, tipically this array
        # only contains one message... so a single iteration...
        for message in messages:
            # Use our message factory to create a message payload accordingly.
            message_dict = messageFactory.create_message(
                message, message_destination)

            # Build the url based on the message object
            url = chat_api_url_factory(message)

            print(json.dumps(message_dict))
            # send the message to Chat-Api
            answer = requests.post(url, data=json.dumps(
                message_dict), headers=headers)
            print(answer.text)
    return answer.text


# Endpoint that awaits a POST request from the chat-api
@app.route('/msg_recv', methods=["GET", "POST"])
def msg_recv():
    # only proceed if the request type is POST
    if request.method == 'POST':
        # If there is no message member inside the json,
        # ignore the request. Because it is probably a ACK
        # message.
        if not "messages" in request.json:
            return "ACK MESSAGE"

        # Get hold of the messages array
        messages = request.json["messages"]

        # for every message in the object, forward to Rocket.chat
        # tipically this is a size 1 array.
        for message in messages:
            # Check if the ack in the message is 0.
            # Ack zero means that the message was sent.
            # So we ignore anything that is not zero to avoid
            # sending duplicate messages to rocket chat.
            if "ack" in message and message["ack"] != 0 and message["ack"] != 1:
                return "ACK MESSAGE"

            # register visitor in rocket chat
            visitor_dict = create_visitor(message)
            register_visitor_request = requests.post(
                url=get_visitor_url(), data=json.dumps(visitor_dict))
            visitor = json.loads(register_visitor_request.text)
            visitor_token = visitor["token"]

            # Check if a file has already ben created for this visitor.
            # The file should contain his last rocket chat livechat room id.
            rid = create_visitor_rid_file(visitor)
            
            room = requests.get(url=get_room_url(visitor_token, rid))
            room = json.loads(room.text)["room"]

            # If the last room the visitor interacted with was closed, update
            # the file with the new rid, so that the next message will be 
            # forwarded correctly.
            update_visitor_rid_file(room, rid)

            # Use a message factory to create the fitting message object
            message_factory = RocketMessageFactory(message, room, visitor)
            converted_message = message_factory.build()

            headers = {
                "Content-Type": "application/json"
            }

            response = requests.post(url=get_rocket_message_url(
            ), data=json.dumps(converted_message), headers=headers)


    return(response.text)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
