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

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content
    
    if msg.startswith("!quote"):
        quote = get_quote()
        await message.channel.send(quote)

    options = starter_encouragements
    if any(word in msg for word in sad_words):
        await message.channel.send(random.choice(options))

    if msg.startswith("!gay"):
        await message.channel.send("It's okay to be a homosexual!")


keep_alive()
client.run(os.environ['TOKEN'])
