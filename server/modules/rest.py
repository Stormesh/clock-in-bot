from aiohttp import ClientError
from typing import Any
from aiohttp import ClientSession, ClientTimeout

_session: ClientSession | None = None


def get_session():
    global _session
    if not _session or _session.closed:
        _session = ClientSession(timeout=ClientTimeout(total=10))
    return _session


async def get(url: str):
    session = get_session()
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.json()
    except (ClientError, TimeoutError) as e:
        print(f"Error getting data from {url}: {e}")
    return None


async def post(url: str, data: dict[Any, Any]):
    session = get_session()
    try:
        async with session.post(url, json=data) as response:
            response.raise_for_status()
            return await response.json()
    except (ClientError, TimeoutError) as e:
        print(f"Error posting data to {url}: {e}")
    return None


async def patch(url: str, data: dict[Any, Any]):
    session = get_session()
    try:
        async with session.patch(url, json=data) as response:
            response.raise_for_status()
            return await response.json()
    except (ClientError, TimeoutError) as e:
        print(f"Error patching data to {url}: {e}")
    return None
