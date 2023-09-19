import aiohttp
from io import BytesIO

async def get_photo_from_url(photo_url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(photo_url) as response:
                if response.status == 200:
                    photo_bytes = await response.read()
                    return BytesIO(photo_bytes)
                else:
                    return None
    except Exception as e:
        return None