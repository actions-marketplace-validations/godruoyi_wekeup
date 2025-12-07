from .notifiable import Notifiable, Message
from environment import Environment
from slack_sdk.errors import SlackApiError
from slack_sdk import WebClient


class SlackNotifier(Notifiable):
    client: WebClient
    slack_chat_id: str

    def __init__(self):
        slack_token = Environment.get_slack_token()
        slack_chat_id = Environment.get_slack_chat_id()

        if not slack_token or slack_token == "":
            raise ValueError("SLACK_TOKEN env variable not set")
        if not slack_chat_id or slack_chat_id == "":
            raise ValueError("SLACK_CHAT_ID env variable not set")

        self.slack_chat_id = slack_chat_id
        self.client = WebClient(slack_token)
        pass

    def notify(self, message: Message):
        message.sentence = "*{}*".format(message.sentence)
        msg = message.format()
        print("sending message to slack", msg)

        try:
            images = []
            for image in message.images:
                images.append({"content": image, "alt_text": "image"})

            if len(images) <= 0:
                self.client.chat_postMessage(channel=self.slack_chat_id, text=msg)
            else:
                self.client.files_upload_v2(file_uploads=images, channel=self.slack_chat_id, initial_comment=msg)
        except SlackApiError as e:
            print("error sending message to slack", e.response["error"])
            raise ValueError(f'error sending message to slack {e.response["error"]}')
