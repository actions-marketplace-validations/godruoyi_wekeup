import pyweathercn
import requests

USER_AGENT = ('Mozilla/5.0 (Linux; Android 10; SM-G9600) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.116 '
              'Mobile Safari/537.36')


# see https://github.com/BennyThink/pyweathercn for more info, thanks @BennyThink
def get_weather(city: str):
    w = pyweathercn.Weather(city)
    first_day = w.data['forecast'][0]

    # 重庆 星期五 小雨 19/15℃ 东北风3-4级
    return "{} {} {} {} {}".format(
        w.data['city'], first_day['date'], first_day['type'], first_day['temp'], first_day['wind'],
    )


def get_weather2(city: str):
    response = requests.get("https://wttr.in/{}?format=j1".format(city), headers={
        'Accept-Language': 'zh-cn',
        'User-Agent': USER_AGENT,
    })
    if response.status_code != 200:
        raise ValueError(f'failed to get weather from wttr.in, err: {response.text}')
    data = response.json()

    first_current_condition = data['current_condition'][0]
    first_weather = data['weather'][0]

    # 晴天 10C/10C
    return "{} {}°C/{}°C 湿度: {}%".format(
        first_current_condition['lang_zh'][0]['value'], # 晴天
        first_weather['mintempC'],
        first_weather['maxtempC'],
        first_current_condition['humidity'],
    )

