import discord
from discord import app_commands
from discord.ext import commands
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

@bot.tree.command(name="prompt")
@app_commands.describe(message="Message for OpenAI GPT")
async def prompt(interaction: discord.Interaction, message:str):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=message,
        max_tokens=2048,
        temperature=0.9,
        top_p=1,
    )
    embed = discord.Embed(title="Response", url="",
                          description=f"{response['choices'][0]['text']}",
                          color=discord.Color.blue())

    await interaction.response.send_message(f"{interaction.user.mention}: {message}", embed=embed)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')


bot.run(discord_key)