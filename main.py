import os
import requests
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

api_key = "54f4900015f8524bbb6274d4aba61701"
account_sid = "AC&c357bb2c70d78979800071781270f39" #this is random. please put your correct code
auth_token = "052987392hfkwjbBBHdiuhw932u98389"
parameters ={
    "lat": 42.712349,
    "lon": -73.203796
    "appid": api_key,
    "exclude":  "currently,minutely,daily"
}

response = requests.get(url="https://api.openweathermap.org/data/3.0/onecall",
                        params= parameters)
response.raise_for_status()
data = response.json()

will_rain = False

for hour_data in data["hourly"][:12]:
    condition = int(hour_data["weather"][0]["id"])
    if condition < 700:
        will_rain = True

if will_rain:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {"https": os.environ["https_proxy"]}

    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages \
    .create(
        body="It's going to rain today. Remember to take your umbrella out with you",
        from="+1234567890",                                         #this number is random. put your correct number here
        to="Your verified number",
    )

    print(message.status)
