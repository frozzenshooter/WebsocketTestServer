# Websocket server 

import asyncio
import websockets
import datetime
import time
import logging

# Config data
PORT = 8765
HOST = "localhost"
INTERVAL = 1
logIntoFile = 0

if logIntoFile:
    logging.basicConfig(filename='server.log', encoding='utf-8', level=logging.INFO)
else:
    logging.basicConfig(level=logging.INFO)

class Server:
    # Clients connected via the websocket
    clients = set()

    async def register(self, ws) -> None:
        self.clients.add(ws)
        logging.info(f" {ws.remote_address} connects.")

    async def unregister(self, ws) -> None:
        self.clients.remove(ws)
        logging.info(f" {ws.remote_address} disconnects.")

    # Handler when a new client connects to a websocket
    async def ws_handler(self, ws, uri) -> None:
        await self.register(ws)
        try:
            await self.send_messages(ws)
        except Exception as e:
            logging.warning(" A client is disconnected!")
        finally:
            await self.unregister(ws)
    
    # Send a new message to the connected client
    async def send_messages(self, ws) -> None:
        while 1:
            timestamp = time.time()
            timestampString = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            logging.info(f"{timestampString}")
            await ws.send(timestampString)
            await asyncio.sleep(INTERVAL)


# STart websocket server
server = Server()
start_server = websockets.serve(server.ws_handler, "" ,PORT)

# Start async handling of websockets
loop = asyncio.get_event_loop()
loop.run_until_complete(start_server)
loop.run_forever()
