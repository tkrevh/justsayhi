import logging
from celery import shared_task
from slack_sdk import WebClient

logger = logging.getLogger()

@shared_task()
def post_message(user_id, access_token, text, real_name):
    logger.debug(f'[tasks.post_message] posting message "{text}" to {real_name}')
    client = WebClient(token=access_token)
    text = text.replace('@username', real_name)
    client.chat_postMessage(channel=user_id, text=text, as_user=True)
    logger.debug(f'[tasks.post_message] message posted')