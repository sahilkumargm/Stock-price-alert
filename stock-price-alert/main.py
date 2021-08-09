import requests
import datetime as dt
from twilio.rest import Client

STOCK = "TSLA" # Edit stock symbol here
COMPANY_NAME = "Tesla Inc" # Edit Company name here

today = dt.datetime.today()
current = today - dt.timedelta(days=1)
current_date = current.date()

yesterday = today - dt.timedelta(days=2)
yesterday_date = yesterday.date()

print(current_date)
print(yesterday_date)

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

stock_price_api_parameters = {
    "apikey": "0TUVHAJNKZTVAUE6",
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": "TSLA", # Change the symbol to a stock of your preference.
    "outputsize": "compact"
}
stock_price_api_url = "https://www.alphavantage.co/query"

#url would look something like: https://www.alphavantage.co/query?apikey=0TUVHAJNKZTVAUE6&function=TIME_SERIES_DAILY_ADJUSTED&symbol=TSLA&outputsize=compact

stock_data_response = requests.get(url=stock_price_api_url, params=stock_price_api_parameters)
stock_data_response.raise_for_status()

response = stock_data_response.json()

today_closing_price = float(response["Time Series (Daily)"][str(current_date)]['4. close'])
yesterday_closing_price = float(response["Time Series (Daily)"][str(yesterday_date)]['4. close'])

print(yesterday_closing_price)
print(today_closing_price)

# Percentage calculations:
is_stock_up = False
is_stock_down = False

if yesterday_closing_price > today_closing_price:
    is_stock_down = True
else:
    is_stock_up = True

percentage_diff = round((abs((yesterday_closing_price - today_closing_price)/yesterday_closing_price)*100))
print(percentage_diff)


## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

news_api_url = "https://newsapi.org/v2/top-headlines"
# https://newsapi.org/v2/top-headlines?q=tesla&apiKey=0313dd380be04c1ab71ba8b9bea35d71

news_api_parameters = {
    "apiKey": "0313dd380be04c1ab71ba8b9bea35d71",
    "q": "tesla"
}


news_api_response = requests.get(url=news_api_url, params=news_api_parameters)
news_api_response.raise_for_status()
news_api_data = news_api_response.json()

news_title = news_api_data["articles"][0]["title"]
news_description = news_api_data["articles"][0]["description"]
news_provider = news_api_data["articles"][0]["source"]["name"]


stock_info_message = ""
if percentage_diff >= 1.00: #CHANGE THIS VALUE TO A VALUE THAT YOU PERFER
    # print("Get News")
    message = ""
    if is_stock_up:
        # stock_info_message = f"TSLA: 🔺{percentage_diff}%\n\nBrief: {news_title}\nDescription: {news_description}\nBy: {news_provider}"
        stock_info_message = f"TSLA: up {percentage_diff}%\n\nBrief: {news_title}\nDescription: {news_description}\nBy: {news_provider}"
    else:
        # stock_info_message = f"TSLA: 🔻{percentage_diff}%\n\nBrief: {news_title}\nDescription: {news_description}\nBy: {news_provider}"
        stock_info_message = f"TSLA: down {percentage_diff}%\n\nBrief: {news_title}\nDescription: {news_description}\nBy: {news_provider}"
    print(stock_info_message)


## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 
account_sid = "AC2b8d64978c2d736f51b6c1aa6853e864" # Kindly use your own account sid and auth token
auth_token = "9b6e8cf2c66e62eb8ccbe9a6fef0d519"

client = Client(account_sid, auth_token)

recipients = ["+919999999999", "+910000000000"] # EDIT THIS LIST TO GIVE IT YOUR PHONE NUMBER IN THE FORMAT PROVIDED.
for contact in recipients:
    message = client.messages \
                    .create(
                         body=stock_info_message,
                         from_='+17327163353', # Enter the phone number you were provided from the twillio client here
                         to=contact
                     )
    print(message.sid)


