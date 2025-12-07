import pendulum

from abc import ABC, abstractmethod
from environment import Environment

NOTIFIER_TG = "tg"
NOTIFIER_SLACK = "slack"


def make_notifier(notifier: str):
    if notifier == NOTIFIER_TG:
        from .telegram_notifier import TelegramNotifier
        return TelegramNotifier()
    if notifier == NOTIFIER_SLACK:
        from .slack_notifier import SlackNotifier
        return SlackNotifier()
    else:
        raise ValueError(f'unknown notifier {notifier}')


class Message:
    images: []
    weather: str
    sentence: str
    error: str
    driver: str
    channel: str
    get_up_time: str

    def __init__(self, images: [] = None, weather: str = None, sentence: str = None,
                 error: str = None, driver: str = None, channel: str = None):
        self.images = images
        self.weather = weather
        self.sentence = sentence
        self.error = error
        self.get_up_time = pendulum.now("Asia/Shanghai").to_time_string()

    def format(self):
        if self.error is not None and self.error != "":
            return self.format_error_message()
        else:
            return self.format_success_message()

    def format_error_message(self):
        template = Environment.get_error_message_format()
        return self.replace_all(template)

    def format_success_message(self):
        template = Environment.get_message_format()
        return self.replace_all(template)

    def replace_all(self, template: str):
        return template.replace("{weather}", self.weather) \
            .replace("{sentence}", self.sentence) \
            .replace("{driver}", self.driver) \
            .replace("{channel}", self.channel) \
            .replace("{error}", self.error if self.error is not None else "") \
            .replace("{get_up_time}", self.get_up_time)


class Notifiable(ABC):
    @abstractmethod
    def notify(self, message: Message):
        pass
