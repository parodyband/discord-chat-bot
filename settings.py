import os
import dotenv

dotenv.load_dotenv()

discord_token = str(os.getenv("DISCORDTOKEN"))
openai_token = str(os.getenv("OPENAITOKEN"))