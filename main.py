import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
TWILIO_SID = "ACe4b58ee34aa04b2ec85d62980af44a84"
TWILIO_AUTH_TOKEN = "6d775bee6f548923616b237f29891d98"

parameters1 = {
    "function" : "TIME_SERIES_DAILY",
    "symbol" : STOCK_NAME,
    "apikey" : "BYHJDO4Y9QXKSFCX"
}

data = requests.get(url="https://www.alphavantage.co/query", params=parameters1)
stock = data.json()["Time Series (Daily)"]
stock_list = [value for (key, value) in stock.items()]
yesterdays_closing_stock = stock_list[0]["4. close"]

dby_closing_stock = stock_list[1]["4. close"]

difference = float(yesterdays_closing_stock) - float(dby_closing_stock)
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

percentage = round((difference/(float(yesterdays_closing_stock)))*100)

parameters2 = {
    "qInTitle" : "tesla",
    "apiKey" : "df52c3cf23d74400a499e4fd439b252e",

}
if abs(percentage) >= 5:
    data = requests.get(url="https://newsapi.org/v2/everything", params=parameters2)
    news = data.json()["articles"]
    articles = news[:3]
    article_list = [f"{COMPANY_NAME}:{up_down}{percentage}% \nHeadline: {article['title']}. \nBrief: {article['description']}" for article in articles]


    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    for article in article_list:
        message = client.messages \
            .create(
            body=article,
            from_='+18643852464',
            to='+16464099334'
        )

        print(message.sid)