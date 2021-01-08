#Websocket client

import asyncio
import websockets

URI = "ws://localhost:8765"

async def client():
    websocket = await websockets.connect(URI)
    while 1:            
            timestamp = await websocket.recv()
            print(f"Timestamp: {timestamp}")

asyncio.run(client())