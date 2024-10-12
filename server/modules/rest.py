import aiohttp
from typing import Any

async def get(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

async def post(url: str, data: dict[Any, Any]):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            return await response.json()

async def patch(url: str, data: dict[Any, Any]):
    async with aiohttp.ClientSession() as session:
        async with session.patch(url, json=data) as response:
            return await response.json()