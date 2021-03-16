import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

api_key = os.environ.get("OWM_API_KEY")
account_sid = os.environ.get("ACCOUNT_SID")
auth_token = os.environ.get("AUTH_TOKEN")

parameter = {
    "lat":28.704060,
    "lon":77.102493,
    "exclude":"current,minutely,daily,alerts",
    "appid":api_key

}
url = f"https://api.openweathermap.org/data/2.5/onecall"
response = requests.get(url=url,params=parameter)
response.raise_for_status()
weather_data = response.json()["hourly"]


today_weather_condition = [weather_data[i]["weather"][0]["id"]  for i in range(0,12)]

for i in today_weather_condition:
    if i < 700:
        proxy_client = TwilioHttpClient()
        proxy_client.session.proxies = {'https':os.environ['https_proxy']}
        client = Client(account_sid,auth_token,http_client=proxy_client)
        message = client.messages \
            .create(
            body="It's going to rain today.Remember to bring an Umbrella",
            from_=os.environ.get("FROM_NO"),
            to=os.environ.get("TO_NO"),
        )
        print(message.status)
        break