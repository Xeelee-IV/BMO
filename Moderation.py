import discord 
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import bot_has_permissions, BotMissingPermissions

class Moderation(commands.Cog):
    """Commands for server administration and moderation"""
    def __init__(self, bot):
        self.bot = bot

        

    @commands.hybrid_command(name="kick", help="Kicks a member from the server.")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason: str = "No reason stated"):
        try:
            await member.kick(reason=reason)
            await ctx.send(f"user {member.display_name} has been kicked from the server. Reason: {reason or ""}")
        except discord.Forbidden:
            await ctx.send("No permision for execution")

    
    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.BotMissingPermissions):
            await ctx.send("You do not have permission to kick members.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please mention a member to kick (`!kick @User` ).")


    @commands.hybrid_command(name="ban", help="bans a member from the server.")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        try:
            await member.ban(reason=reason)
            await ctx.send(f"User {member.display_name} has been banned from the server. Reason: {reason or ""}")
        except discord.Forbidden:
            await ctx.send("Missing permission to banm the user")

    @ban.error
    async def unban_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have permission to ban members.")
        
    

    @commands.hybrid_command(name="unban", description="Unban a user by name or user ID")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, target: str):
        bans = [entry async for entry in ctx.guild.bans()]
        
        if not bans:
            return await ctx.send("The ban list is empty.")
        
        target_clean = target.replace("@", "").strip().lower()

        for ban_entry in bans:
            user = ban_entry.user
            if (target_clean == str(user.id) or
                target_clean == user.name.lower() or
                target_clean == str(user).lower()):

                await ctx.guild.unban(user)
                await ctx.send(f"{user.name} has been unbanned.")
                return
        await ctx.send(f"Could not find a banned user: {target}. Make sure the ID is correct.")



async def setup(bot):
    await bot.add_cog(Moderation(bot))


    





