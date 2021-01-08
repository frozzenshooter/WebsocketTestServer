# Websocket server 

import asyncio
import websockets
import datetime
import time
import logging


PORT = 8765
INTERVAL = 1

logging.basicConfig(level=logging.INFO)


class Server:
    clients = set()

    async def register(self, ws) -> None:
        self.clients.add(ws)
        logging.info(f"{ws.remote_address} connects.")

    async def unregister(self, ws) -> None:
        self.clients.remove(ws)
        logging.info(f"{ws.remote_address} disconnects.")

    async def ws_handler(self, ws, uri) -> None:
        await self.register(ws)
        try:
            await self.distribute(ws)
        except Exception as e:
            logging.fatal("DISCONNECTED")
        finally:
            await self.unregister(ws)
    
    async def distribute(self, ws) -> None:
        while 1:
            timestamp = time.time()
            timestampString = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            logging.info(f"{timestampString}")
            await ws.send(timestampString)
            await asyncio.sleep(INTERVAL)



server = Server()
start_server = websockets.serve(server.ws_handler, "localhost", PORT)
loop = asyncio.get_event_loop()
loop.run_until_complete(start_server)
loop.run_forever()
