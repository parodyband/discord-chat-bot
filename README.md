# DiscordGPTChatBot

DiscordGPTChatBot is a Discord chatbot built using Discord.py and OpenAI GPT-X. The bot is capable of participating in text conversations, responding to specific commands, and has a memory feature to remember past interactions.

## Features
- Conversational AI using OpenAI GPT-X
- Slash command support
- Memory feature for maintaining the context of conversations
- Customizable command handling using cogs

## Installation
1. Make sure you have Python 3.8 or later installed on your system.
2. Clone the repository: `git clone https://github.com/parodyband/discord-chat-bot.git`
3. `cd DiscordGPTChatBot`
4. Install the required packages: `pip install -r requirements.txt`
5. Create a `.env` file in the root directory of the project with the following contents:
```
DISCORD_TOKEN=your_discord_bot_token
OPENAI_TOKEN=your_openai_api_key
```
Replace `your_discord_bot_token` with your bot's token, and `your_openai_api_key` with your OpenAI API key.
6. Run the bot: `python bot.py`

## Usage
DiscordGPTChatBot listens to chat messages and responds based on the input. The bot can be summoned using an @mention or using specific slash commands.

### Slash commands
- `/clear_memory`: Clears the AI memory.
- `/print_memory`: Prints the current AI memory.
- `/restart`: Restarts the bot (requires administrator permissions).

## Customization
DiscordGPTChatBot's command handling can be customized using cogs. To add a new command or functionality, create a new Python file in the `cogs` directory and implement your command as a class that inherits from `commands.Cog`. Use the `commands.py` file as a reference for creating new commands.

To register the new cog, import and add it to the bot in `bot.py`:
```python
bot.load_extension("cogs.your_new_cog")
```
Replace `your_new_cog` with the name of your new cog file (without the `.py` extension).