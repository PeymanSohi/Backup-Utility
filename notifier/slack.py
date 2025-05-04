import requests

def notify_slack(webhook_url, message):
    payload = {"text": message}
    response = requests.post(webhook_url, json=payload)
    print("Slack notification sent." if response.status_code == 200 else "Failed to send Slack notification.")
