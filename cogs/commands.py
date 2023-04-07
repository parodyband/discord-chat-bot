import discord
from discord.ext import commands
from utils import ai_utils, discord_utils
from personality import initial_prompt, classifier_system

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping")
    async def ping(self, ctx):
        latency = round(self.bot.latency * 1000)
        await ctx.send(f"pong! {latency}")

    @commands.command(name="clear_memory")
    async def clear_memory(self, ctx):
        ai_utils.clear_memory()
        await ctx.send("Cleared Memory")

    @commands.command(name="print_memory")
    async def print_memory(self, ctx):
        response = ai_utils.messages
        await ctx.send(f"{response}")

def setup(bot):
    bot.add_cog(Commands(bot))