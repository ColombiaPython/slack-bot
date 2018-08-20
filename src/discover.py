import os, slackclient, json

with open('./config.json') as f:
    data = json.load(f)

config = data['config']

SLACK_TOKEN = config['token']

# initialize slack client
slack_client = slackclient.SlackClient(SLACK_TOKEN)

response = slack_client.api_call("api.test")

# find the id of our slack bot
if response["ok"] == True: print('Connected!')
else: print('No Response')