import discord
import openai
import os
from dotenv import load_dotenv

load_dotenv()
discord_token = os.getenv("DISCORD_TOKEN")
openai.api_key = os.getenv("OPENAI_API_KEY")

intents = discord.Intents.all()
client = discord.Client(intents=intents)


def generate_text(messages):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        max_tokens=1200,
        messages=messages,
    )
    return response


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    messages = [
        {"role": "system", "content": "You are now a coding copilot and knowledgeable database. Provide code blocks that can be easily copy-pasted, along with clear and extended explanations of how functions work and their applicability in different scenarios. Prioritize accuracy and clarity in your responses to coding questions."},
        {"role": "user", "content": message.content},
        {"role": "assistant", "content": ""},
    ]

    response = generate_text(messages)
    response_text = response.choices[0]['message']['content']
    tokens_used = response['usage']['total_tokens']
    prompt_cost = 0.03 / 1000 * tokens_used
    completion_cost = 0.06 / 1000 * tokens_used
    total_cost = prompt_cost + completion_cost

    cost_info = f"Tokens used: {tokens_used}, Cost: ${total_cost:.5f}"
    await message.channel.send(f"{response_text}\n\n{cost_info}")

client.run(discord_token)
