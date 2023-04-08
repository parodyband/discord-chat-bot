import discord
import aiohttp
from discord.ext import commands
from config import discord_token
from utils import ai_utils, discord_utils

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="$", intents=intents)

# Load cogs
bot.load_extension("cogs.commands")
bot.load_extension("cogs.events")


@bot.event
async def on_message(message):

    incoming_message = await discord_utils.replace_mentions_with_usernames(message.content,bot)

    print(f"{message.author.name}: {incoming_message}")

    if message.author == bot.user:
        return
    
    # Check for Instagram links
    if "instagram.com" in message.content:
        emoji = discord.utils.get(message.guild.emojis, name="handpussykaijitsu");
        await message.channel.send(f"Get that shit out of here, aint no one clickin that. {emoji}")
        return

    message_context = 5
    check_msgs = await discord_utils.read_last_n_responses(message_context, message, bot)
    ai__should_respond, reasoning = ai_utils.should_respond(check_msgs)

    print(f"Thinking: Will I respond? [{ai__should_respond}] | Message Context [{message_context}] | Reasoning: {reasoning}")

    if ai__should_respond:
        ai_utils.clear_memory()
        ai_utils.messages.append(check_msgs)
        await message.channel.send(ai_utils.generate_response(ai_utils.messages, message.author.name))

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

    # Check if the message is from Zee#5246
    if message.author.name == "Zee" and message.author.discriminator == "5246":
        # Get the custom emoji from the guild
        emoji = discord.utils.get(message.guild.emojis, name="handpussykaijitsu")
        # if emoji:
        # await message.add_reaction(emoji)

    # Process other commands
    await bot.process_commands(message)


bot.run(discord_token)
