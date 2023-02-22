import discord
import os
import openai

openai.api_key = os.getenv("GPTKEY")
discord_key = os.getenv("DISCORD_KEY")
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith("!prompt"):
        payload = message.content.lstrip("!prompt")
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=payload,
            max_tokens=2048,
            temperature=0.9,
            top_p=1,
        )
        embed = discord.Embed(title="Response", url="",
                              description=f"{response['choices'][0]['text']}",
                              color=discord.Color.blue())
        await message.channel.send(embed=embed)


client.run(discord_key)