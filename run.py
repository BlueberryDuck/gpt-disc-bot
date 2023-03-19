import discord
import openai
from openai import APIError
import os
from dotenv import load_dotenv

load_dotenv()
discord_token = os.getenv("DISCORD_TOKEN")
openai.api_key = os.getenv("OPENAI_API_KEY")

intents = discord.Intents.all()
client = discord.Client(intents=intents)


def generate_text(messages, version):
    if version == 4:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            max_tokens=1200,
            messages=messages,
        )
    else:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            max_tokens=1200,
            messages=messages,
        )
    return response


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    content = message.content
    version = 3
    if content.startswith('4'):
        version = 4
        content = content[1:].lstrip()
    messages = [
        {"role": "system", "content": "You are now a coding copilot and knowledgeable database. Provide code blocks that can be easily copy-pasted, along with clear explanations of how functions work and their applicability in different scenarios. Prioritize accuracy and clarity in your responses to coding questions, while staying concise to reduce the amount of tokens used."},
        {"role": "user", "content": content},
        {"role": "assistant", "content": ""},
    ]

    try:
        response = generate_text(messages, version)
        response_text = response.choices[0]['message']['content']
        tokens_used = response['usage']['total_tokens']
        cost = 0.06 / 1000 * tokens_used
    except APIError as e:
        response_text = f"Error:{e}"
        tokens_used = 0
        cost = 0

    await message.channel.send(f"{response_text}\n\nVersion: {version}\nTokens used: {tokens_used}, Cost: ${cost:.5f}")

client.run(discord_token)
