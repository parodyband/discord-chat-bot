import subprocess
import sys
from discord.ext import commands
from utils import ai_utils

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Commands Cog is loaded")

    @commands.slash_command(name="ping")
    async def ping_legacy(self, ctx):
        if ctx.author.guild_permissions.administrator:
            latency = round(self.bot.latency * 1000)
            await ctx.respond(f"pong! {latency}")
        else:    
            await ctx.respond("You do not have permission to ping the bot.")

    @commands.slash_command(name="clear_memory")
    async def clear_memory_legacy(self, ctx):
        if ctx.author.guild_permissions.administrator:
            ai_utils.clear_memory()
            await ctx.respond("Cleared Memory")
        else:
            await ctx.respond("You do not have permission to clear the memory.")

    @commands.slash_command(name="print_memory")
    async def print_memory_legacy(self, ctx):
        if ctx.author.guild_permissions.administrator:
            response = ai_utils.messages
            await ctx.respond(f"{response}")
        else:
            await ctx.respond("You do not have permission to print the memory.")

    @commands.slash_command(name="restart")
    async def restart(self, ctx):
        # Check if the command issuer has the administrator permission
        if ctx.author.guild_permissions.administrator:
            await ctx.respond("Restarting...")
            subprocess.call([r'restart_bot.bat'])
            await self.bot.close()
            sys.exit(0)  # Terminate the script gracefully
        else:
            await ctx.respond("You do not have permission to restart the bot.")

def setup(bot):
    bot.add_cog(Commands(bot))