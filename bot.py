import discord
import aiohttp
from discord.ext import commands
from settings import discord_token, openai_token
from personality import initial_prompt, classifier_system
import openai
import re

openai.api_key = openai_token

messages = list()

messages.append(initial_prompt)

def generate_response(p, last_username):
    messages.append(f"\n{p}\n GentryBot:")
    response = openai.Completion.create(
    #model="davinci:ft-strange-ape-games-2023-04-07-03-40-18",
    model="text-davinci-003", 
    prompt="".join(messages),
    temperature=0.9,
    max_tokens=500,
    top_p=1,
    frequency_penalty=0.2,
    presence_penalty=0.5,
    stop=[f"{last_username}:", "GentryBot:", "Friend:"],
    )
    print(messages[-1])
    messages.append(response.choices[0].text)
    return response.choices[0].text

def should_respond(message_string):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"{classifier_system}"},
            {"role": "user", "content": f'Should the user "GentryBot" reply to this conversation?\n{message_string}'}
    ]
    )

    decision_text = completion['choices'][0]['message']['content']

    if "Yes" in decision_text or "yes" in decision_text:
        return True
    else:
        return False
  

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

async def mention_to_username(mention_str):
    # Extract the user ID from the mention string using a regex
    user_id_match = re.search(r'<@(\d+)>', mention_str)
    
    if user_id_match:
        user_id = int(user_id_match.group(1))
        
        # Fetch the user object using the user ID
        user = await bot.fetch_user(user_id)
        
        # Return the user's display name
        return "@" + user.display_name
    else:
        return None

async def replace_mentions_with_usernames(message):
    # Find all mentions in the message
    mention_matches = re.finditer(r'<@!?(\d+)>', message)

    # Create a list of tuples with the start and end positions of each mention
    mention_ranges = [(m.start(), m.end()) for m in mention_matches]

    # Replace each mention with the corresponding username
    new_message_parts = []
    prev_end = 0
    for start, end in mention_ranges:
        new_message_parts.append(message[prev_end:start])
        user_id = int(message[start + 2:end - 1].lstrip('!'))
        user = await bot.fetch_user(user_id)
        new_message_parts.append("@" + user.display_name)
        prev_end = end

    new_message_parts.append(message[prev_end:])
    new_message = "".join(new_message_parts)

    return new_message

def clear_memory():
    messages.clear()
    messages.append(initial_prompt)

async def read_last_n_responses(num, message):
    # Fetch the last 3 messages before the bot was mentioned
    previous_messages = await get_history_messages(message, num)

    # Combine the previous messages into a single string
    previous_messages_str = "\n".join(previous_messages)

    #mes = message.content.split(f'<@{bot.user.id}>')[1].strip()

    final_str = f"{previous_messages_str}\n{message.author.name}: {message.content}"
    final_str = await replace_mentions_with_usernames(final_str)

    print(message.author.name)
    if "GentryBot" in message.author.name:
        final_str = "NoUsername:"
    
    print(final_str)
    
    # Add the previous messages to the message content
    return final_str
       
# separate function to get messages history 
async def get_history_messages(message, num):
    previous_messages = [] 
    async for msg in message.channel.history(limit=num, before=message): 
        previous_messages.append(f"{msg.author.name}: {msg.content}")

    previous_messages.reverse() 
    
    return previous_messages

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send('Hello!')

@bot.slash_command(name="ping", description="replies with ping")
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.respond(f"pong! {latency}")

@bot.slash_command(name="clear_memory", description="clear memory")
async def ping(ctx):
    response = "Cleared Memory"
    clear_memory()
    await ctx.respond(f"{response}")

@bot.slash_command(name="print_memory", description="print memory")
async def ping(ctx):
    response = messages
    await ctx.respond(f"{response}")

@bot.event
async def on_message(message):

    check_msgs = await read_last_n_responses(5,message)
    print(should_respond(check_msgs))
    if should_respond(check_msgs):
        clear_memory()
        messages.append(check_msgs)
        await message.channel.send(generate_response(messages,message.author.name))

    if message.author == bot.user:
        return

    # Check if the bot was mentioned
    if bot.user in message.mentions:
        
        mes = message.content.split(f'<@{bot.user.id}>')[1].strip()
        
        # Check for text file attachments
        txt_attachment = None
        if message.attachments:
            for attachment in message.attachments:
                if attachment.filename.endswith('.txt'):
                    txt_attachment = attachment
                    break

        # If a text file is found, download and read its contents
        if txt_attachment:
            async with aiohttp.ClientSession() as session:
                async with session.get(txt_attachment.url) as response:
                    if response.status == 200:
                        txt_content = await response.text()
                        mes = f"{mes} {txt_content}"

        
        #clear_memory()
        #await message.channel.send(generate_response(message.author.name, mes))

    # Check if the message is from Zee#5246
    if message.author.name == "Zee" and message.author.discriminator == "5246":
        # Get the custom emoji from the guild
        emoji = discord.utils.get(message.guild.emojis, name="handpussykaijitsu")
        if emoji:
            await message.add_reaction(emoji)

    # Process other commands
    await bot.process_commands(message)

bot.run(discord_token)