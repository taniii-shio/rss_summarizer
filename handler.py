import feedparser
import openai
import os
import requests

def lambda_handler(event, context):
    # TechCrunchのRSSフィードのURL
    feed_url = 'https://techcrunch.com/rssfeeds/'

    # RSSフィードを取得
    feed = feedparser.parse(feed_url)

    # フィードのエントリーごとに処理
    for entry in feed.entries:
        title = entry.title
        link = entry.link
        summary = summarize_text(entry.summary)  # 要約を取得

        # Slackに通知するなど、必要な処理を行う
        send_to_slack(title, link, summary)
        break

def summarize_text(text):
    # ChatGPT APIを使用して要約を生成
    openai.api_key = os.environ.get('OPENAI_APIKEY')

    response = openai.Completion.create(
        model='text-davinci-003',
        prompt=text,
        max_tokens=800,  # 要約の長さを調整
        temperature=0.3,  # 要約の生成バリエーションを調整
        n=1,  # 要約の生成数を調整
        stop=None,  # 要約の終了条件を設定（必要に応じて変更）
    )

    # ChatGPTの応答から要約を取得
    summary = response.choices[0].text.strip()
    return summary

def send_to_slack(title, link, summary):
    # Slackに通知する処理を実装する
    # 例えば、SlackのWebhookを使用してメッセージを送信するなど

    # Slackへの通知例（Webhookを使用する場合）
    slack_webhook_url = os.environ.get('SLACK_WEBHOOK_URL')
    payload = {
        'text': f'【{title}】\n{summary}\n{link}'
    }
    response = requests.post(slack_webhook_url, json=payload)
    print(response.text)
