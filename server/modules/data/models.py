from sqlmodel import SQLModel, Field, Relationship, String, BigInteger, Column, ForeignKey  # type: ignore
from typing import Optional


class Server(SQLModel, table=True):
    """Represents a Discord server."""
    id: int = Field(sa_column=Column(BigInteger, primary_key=True))
    name: str
    channels: list["Channel"] = Relationship(back_populates="server")


class ChannelRoleLink(SQLModel, table=True):
    """Represents the link between a channel and a role."""
    channel_id: Optional[int] = Field(
        default=None,
        sa_column=Column(BigInteger, ForeignKey("channel.id"), primary_key=True),
    )
    role_id: Optional[int] = Field(
        default=None,
        sa_column=Column(BigInteger, ForeignKey("role.id"), primary_key=True),
    )

class Channel(SQLModel, table=True):
    """Represents a Discord channel."""
    id: int = Field(sa_column=Column(BigInteger, primary_key=True))
    server_id: int = Field(sa_column=Column(BigInteger, ForeignKey("server.id")))
    name: Optional[str] = Field(default=None, sa_column=Column(String, nullable=True))
    server: Server = Relationship(back_populates="channels")
    log_id: Optional[int] = Field(
        default=None, sa_column=Column(BigInteger, nullable=True)
    )
    sheet_url: Optional[str] = None
    message_id: Optional[int] = Field(
        default=None, sa_column=Column(BigInteger, nullable=True)
    )
    roles: list["Role"] = Relationship(
        back_populates="channels", link_model=ChannelRoleLink
    )


class Role(SQLModel, table=True):
    """Represents a Discord role."""
    id: int = Field(sa_column=Column(BigInteger, primary_key=True))
    type: str
    channels: list[Channel] = Relationship(
        back_populates="roles", link_model=ChannelRoleLink
    )
