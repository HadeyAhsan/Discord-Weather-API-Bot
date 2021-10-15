import os
import discord
import requests
import json
import random
from keep_alive import keep_alive

client = discord.Client()

sad_words = ["!sad", "!hurt", "!depressed", "!angry", "!unhappy", "!mad", "!cheesed", "miserable", "!pissed"]

starter_encouragements = ["Cheer up buttercup!", "Hang in there homeslice.", "Turn that frown upside down!", "Keep moving forward."]

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return(quote)


def get_weather(city):
    url = "https://api.openweathermap.org/data/2.5/weather?q={}&APPID=d3a8904ccbb0c1710857b2ce8fc0353e"
    url = url.format(city)
    response = requests.get(url)
    data = json.loads(response.text)  
    for majorkey, subdict in data.items():
        if majorkey == 'main':
            for subkey, value in subdict.items():
                if subkey == "temp":
                    temp = value
    for majorkey, subdict in data.items():
        if majorkey == "sys":
            for subkey, value in subdict.items():
                if subkey == "country":
                    country = value
    return (temp, country)

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content
    city = msg.split()[1]
    if msg.startswith("!quote") and msg.endswith("te"):
        quote = get_quote()
        await message.channel.send(quote)

    options = starter_encouragements
    if any(word in msg for word in sad_words):
        await message.channel.send(random.choice(options))

    if msg.startswith("!weather"):
        getWeather = get_weather(city)
        temp = getWeather[0]
        country = getWeather[1]
        temp = temp - 273.15
        far = temp * 1.8 + 32
        await message.channel.send("The weather in {}, {} is {:0.2f}°C or {:0.2f}°F".format(city,country,temp,far))

    # if msg.startswith("!weather") and msg.endswith("Milton") or msg.endswith("milton"):
    #     getWeather = get_weatherMilton()
    #     temp = getWeather[1]
    #     temp = temp - 273.15
    #     far = temp * 1.8 + 32
    #     await message.channel.send("The weather in Milton Ontario is {:0.2f}°C or {:0.2f}°F".format(temp,far))

keep_alive()
client.run(os.environ['TOKEN'])