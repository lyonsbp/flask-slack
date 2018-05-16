from flask import render_template, jsonify
from app import app
import requests, os

slack_token = os.environ.get("slack_token")
general_id = "C7Y9H6UR0"

@app.route('/')
def index():
  return "Hello"

@app.route('/slack/users')
def get_user_list():
  url = ("https://slack.com/api/conversations.members?token={0}&channel={1}").format(slack_token, general_id)
  res = requests.get(url)
  json = res.json()
  return json["members"]

def get_user_presence(user_id):
  url = ("https://slack.com/api/users.getPresence?token={0}&user={1}").format(slack_token, user_id)
  res = requests.get(url)
  json = res.json()
  return json

@app.route('/slack/status')
def get_user_status():
  members = get_user_list()
  status_arr = []
  for member in members:
    json = get_user_presence(member)
    presence = json["presence"]
    status_arr.append({
      "id": member,
      "presence": presence
    })
  print(status_arr)
  return jsonify(status_arr)

@app.route('/slack/channels')
def get_channel_list():
  url = ("https://slack.com/api/channels.list?token={0}&pretty=1").format(slack_token)
  res = requests.get(url)
  json = res.json()
  id = "placeholder"
  for channel in json["channels"]:
    if channel["name"] == "general":
      id = channel["id"]
  return id