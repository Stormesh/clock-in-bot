from aiohttp import ClientSession, ClientTimeout

_session: ClientSession | None = None

def get_session():
    global _session
    if not _session or _session.closed:
        _session = ClientSession(timeout=ClientTimeout(total=10))
    return _session
