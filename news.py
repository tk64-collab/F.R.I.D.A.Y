import requests
import os

# ニュースAPIキーを環境変数から取得
news_api_key = os.getenv("NEWS_API_KEY")


def get_news():
    url = f"https://newsapi.org/v2/top-headlines?country=jp&apiKey={news_api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        news_data = response.json()
        articles = news_data.get("articles", [])
        if not articles:
            return "最新のニュースが見つかりませんでした。"

        top_articles = articles[:5]
        news_summary = "最新のニュースです：\n"
        for article in top_articles:
            title = article.get("title", "タイトルなし")
            description = article.get("description", "説明なし")
            news_summary += f"・{title} - {description}\n"
        return news_summary
    else:
        return f"ニュース情報を取得できませんでした (エラーコード: {response.status_code})。"
