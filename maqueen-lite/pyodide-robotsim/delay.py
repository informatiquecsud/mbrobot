from asyncio import sleep
async def delay(ms):
    await sleep(ms / 1000)
    
