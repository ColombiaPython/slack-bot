from slackeventsapi import SlackEventAdapter
from slackclient import SlackClient
import os, json

with open('./config.json') as f:
    data = json.load(f)

config = data['config']

# Our app's Slack Event Adapter for receiving actions via the Events API
slack_signing_secret = config['signing_secret']
slack_events_adapter = SlackEventAdapter(slack_signing_secret, "/slack/events")

# Create a SlackClient for your bot to use for Web API requests
slack_bot_name = config['name']
slack_bot_token = config['token']
slack_client = SlackClient(slack_bot_token)

texts = data['text']

# New User added
@slack_events_adapter.on("team_join")
def user_added(event_data):
    event = event_data["event"]
    user = event["user"]["id"]
    
    direct_channel = slack_client.api_call("im.open", user=user)

    if direct_channel["ok"]:
        slack_client.api_call("chat.postMessage", channel=direct_channel["channel"]["id"], text=texts['welcome_private'])


@slack_events_adapter.on("message")
def handle_message(event_data):
    message = event_data["event"]
    print(message)

    # Private Message
    if message["channel_type"] == "im":
        if message.get("subtype") is None and "hola"  in message.get('text'):
            channel = message["channel"]
            message = "Hola <@%s>! :tada:" % message["user"]
            slack_client.api_call("chat.postMessage", channel=channel, text=message)
    # else:
    # Public Message
        # if message.get("subtype") is None and message['text'] == ("hola @<" + message['user'] + ">"):
        #     channel = message["channel"]
        #     message = "Hello <@%s>! :tada:" % message["user"]
        #     slack_client.api_call("chat.postMessage", channel=channel, text=message)


# Error events
@slack_events_adapter.on("error")
def error_handler(err):
    print("ERROR: " + str(err))

# Once we have our event listeners configured, we can start the
# Flask server with the default `/events` endpoint on port 3000
slack_events_adapter.start(port=3000)