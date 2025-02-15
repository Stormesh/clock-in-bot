import discord
from modules.general_data import get_server

class LogManager:
    @staticmethod
    def get_log_channel(guild: discord.Guild):
        server = get_server(guild.id)
        if not server or not guild:
            return None
        
        log_id = int(server['logId'])
        log_channel = guild.get_channel(log_id)
        
        if not isinstance(log_channel, discord.TextChannel):
            return None
        
        return log_channel
    
    @staticmethod
    async def send_log_message(guild: discord.Guild, embed: discord.Embed):
        log_channel = LogManager.get_log_channel(guild)
        if isinstance(log_channel, discord.TextChannel):
            await log_channel.send(embed=embed)
