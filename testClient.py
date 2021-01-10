#Websocket client

import datetime
import asyncio
import websockets

URI = "ws://localhost:8765"

async def client():
    websocket = await websockets.connect(URI)
    while 1:            
            timestamp = await websocket.recv()
            timestampString = datetime.datetime.fromtimestamp(float(timestamp)).strftime('%Y-%m-%d %H:%M:%S')
            print(f"Timestamp: {timestampString}")

asyncio.run(client())