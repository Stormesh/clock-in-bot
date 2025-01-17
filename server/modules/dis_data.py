import aiofiles, json

data: list[dict[str, str | int]] = []

async def read_data(file_path: str):
    global data
    async with aiofiles.open(file_path, 'r') as f:
        data = json.loads(await f.read())

async def save_data(file_path: str):
    async with aiofiles.open(file_path, 'w') as f:
        await f.write(json.dumps(data, indent=4))

def get_data():
    return data

async def add_data(new_data: dict[str, str | int], file_path: str):
    data.append(new_data)
    await save_data(file_path)