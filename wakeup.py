from drivers import make_image_driver
from notifications import make_notifier, Message
from services import HydrateService
from environment import Environment

if __name__ == '__main__':
    service = HydrateService()
    sentence = service.random_sentence()
    weather = service.get_weather(Environment.get_city())

    notifiers = []
    for channel in Environment.get_channels():
        # initialize notifiers first to check if the configuration is correct
        notifiers.append({"notifier": make_notifier(channel), "channel": channel})

    for d in Environment.get_drivers():
        message = Message(weather=weather, sentence=sentence)
        message.driver = d
        print("generating images for driver {}, sentence: {}".format(d, sentence))

        try:
            images = make_image_driver(d).generate_images(sentence)
            message.images = images
        except Exception as e:
            print("error generating images: ", e)
            if Environment.send_error() is False:
                print("error sending disabled")
                continue
            message.error = str(e)

        for notifier in notifiers:
            message.channel = notifier["channel"]
            notifier["notifier"].notify(message)

    print("done")
