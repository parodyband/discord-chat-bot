import os
import dotenv

dotenv.load_dotenv()

discord_token = str(os.getenv("DISCORDTOKEN"))
openai_token = str(os.getenv("OPENAITOKEN"))
bot_name = str(os.getenv("BOTNAME"))