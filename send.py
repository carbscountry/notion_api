import os
import datetime
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import requests
from dotenv import load_dotenv

# .envファイルの内容を読み込見込む
load_dotenv()


# Notion API設定
NOTION_API_TOKEN = os.environ["NOTION_API_TOKEN"]
RESERCH_TABLE_URL = os.environ["RESERCH_TABLE_URL"]
NOTE_TABLE_URL = os.environ["NOTE_TABLE_URL"]

#slack API設定
SLACK_API_TOKEN = os.environ["SLACK_API_TOKEN"]

def get_Member_dict():
  url = f"https://api.notion.com/v1/databases/{RESERCH_TABLE_URL}/query"
  headers = {
    "Authorization": f"Bearer {NOTION_API_TOKEN}",
    'Notion-Version': "2022-06-28",
    'Content-Type': 'application/json',
  }
  r = requests.post(url, headers=headers)
  data = r.json()
  Member_list = []
  for i in range(len(data['results'])):
    get_user = data['results'][i]['properties']['ユーザー']['people'][0]['name']
    if get_user not in Member_list:
      Member_list.append(get_user)

  return {key: 0 for key in Member_list}


def get_weekly_report_counts(Member_dict):
  # 今日の日付を取得
  today = datetime.date.today()
  def is_this_week(input_date):

    # 今週の最初の日（月曜日）を取得
    monday_of_this_week = today - datetime.timedelta(days=today.weekday())

    # 今週の最後の日（日曜日）を取得
    sunday_of_this_week = monday_of_this_week + datetime.timedelta(days=6)

    return monday_of_this_week <= input_date <= sunday_of_this_week

  url = f"https://api.notion.com/v1/databases/{NOTE_TABLE_URL}/query"
  headers = {
    "Authorization": f"Bearer {NOTION_API_TOKEN}",
    'Notion-Version': "2022-06-28",
    'Content-Type': 'application/json',
  }
  r = requests.post(url, headers=headers)
  data = r.json()

  for lengh in range(len(data['results'])):
    #生年月日をdatatime型に変換
    input_str = data['results'][lengh]['properties']['日付']['date']['start']
    input_date = datetime.datetime.strptime(input_str, '%Y-%m-%d').date()
    if is_this_week(input_date):
      Member_dict[data['results'][lengh]['properties']['作成者']['people'][0]['name']] =+ 1
  _txt = f"{str(today - datetime.timedelta(days=today.weekday()))}から{str(today)}の週\n\n"
  for k,v in Member_dict.items():
    _txt = _txt + f'{k}:  {v}回提出\n'
  return _txt



def main():
    _dict = get_Member_dict()
    Send_txt = get_weekly_report_counts(_dict)
    client = WebClient(SLACK_API_TOKEN)
    response = client.chat_postMessage(
        channel="#サボり通知",
        text=Send_txt,
    )
if __name__ == "__main__":
  schedule.every().monday.at(“15:40”).do(main)

