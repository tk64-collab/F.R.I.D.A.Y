import json
import os
import requests
from city_translation import city_translation  # 別ファイルにしている場合

# 環境変数からAPIキーを取得
api_key = os.getenv("OPENWEATHER_API_KEY")

# city.list.jsonファイルを読み込む
city_data_path = os.path.join(os.path.dirname(__file__), 'city.list.json')
with open(city_data_path, 'r', encoding='utf-8') as f:
    city_data = json.load(f)


def translate_city_name(city_name):
    return city_translation.get(city_name, city_name)


def get_city_id(city_name, city_data):
    translated_city_name = translate_city_name(city_name)
    for city in city_data:
        if city["name"].lower() == translated_city_name.lower():
            return city["id"]
    return None


def get_weather_by_city_id(city_id):
    if city_id is None:
        return "都市IDが見つかりませんでした。"

    url = f"http://api.openweathermap.org/data/2.5/weather?id={city_id}&appid={api_key}&units=metric&lang=ja"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        return f"現在の天気は {weather} で、気温は {temp}°C です。"
    elif response.status_code == 401:
        return "天気情報を取得できませんでした。APIキーが無効です。"
    else:
        return f"天気情報を取得できませんでした (エラーコード: {response.status_code})。"


def get_weather(question):
    location = None
    if "の天気" in question:
        location = question.split("の天気")[0].strip()
    elif "天気" in question:
        location = question.split("天気")[0].strip()

    if location:
        city_id = get_city_id(location, city_data)
        return get_weather_by_city_id(city_id)
    else:
        return "場所を特定できませんでした。"
