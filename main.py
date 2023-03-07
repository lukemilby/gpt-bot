import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import os
import openai

openai.api_key = os.getenv("GPTKEY")
discord_key = os.getenv("DISCORD_KEY")
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands(s)")
    except Exception as e:
        print(e)

@bot.tree.command(name="hello")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("Hello", ephemeral=True)

@bot.tree.command(name="models")
async def models(interaction: discord.Interaction):
    response = openai.Model.list()
    print(response)

@bot.tree.command(name="prompt")
@app_commands.describe(message="Message for OpenAI GPT")
async def prompt(interaction: discord.Interaction, message:str):
    try:
        await interaction.response.defer()
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "you are a helpful assistant"},
                {"role": "user", "content": message}
            ],
        )
        print(response)
        embed = discord.Embed(title="Response", url="",
                              description=f"{response['choices'][0]['message']['content']}",
                              color=discord.Color.blue())
        await asyncio.sleep(4)
        await interaction.followup.send(f"{interaction.user.mention}: {message}", embed=embed)
    except Exception as e:
        print(e)
        await interaction.followup.send("There seems to be an issue with Open AI, please contact one of the Discord Admins", ephemeral=True)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')


bot.run(discord_key)