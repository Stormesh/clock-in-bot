import discord
from .data.common import get_channel


class LogManager:
    def __init__(
        self,
        guild: discord.Guild | None = None,
        channel: discord.TextChannel | None = None,
    ):
        self.channel = channel
        self.guild = guild

    def get_log_channel(self):
        if not self.channel or not self.guild:
            return None

        clock_channel = get_channel(self.channel.id)
        if not clock_channel or not self.channel:
            return None

        log_id = clock_channel.log_id
        if not log_id:
            return None

        log_channel = self.guild.get_channel(log_id)

        if not isinstance(log_channel, discord.TextChannel):
            return None

        return log_channel

    def set_log_channel(self, channel: discord.TextChannel, guild: discord.Guild):
        self.channel = channel
        self.guild = guild

    async def send_log_message(self, embed: discord.Embed):
        log_channel = LogManager.get_log_channel(self)
        if isinstance(log_channel, discord.TextChannel):
            await log_channel.send(embed=embed)
