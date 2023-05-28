import asyncio
import json
import websockets as ws


class Client:
    def __init__(self, host: str = "localhost", port: str = 6969, url: str = None):
        self.__url = url
        self.__host, self.__port = host, port
        self.__websocket = None

    async def __aenter__(self) -> "WebSocketClient":
        self.__websocket = await ws.connect(
            f"ws://{self.__host}:{self.__port}" if not self.__url else self.__url
        )
        return self

    async def __aexit__(
        self, exc_type: type, exc_value: Exception, traceback: type
    ) -> None:
        if exc_type is not None:
            print(f"Exception: {exc_type.__name__}")
        await self.__websocket.close()

    async def send(self, data: dict) -> None:
        await self.__websocket.send(json.dumps(data))

    async def recv(self) -> dict:
        data = await self.__websocket.recv()
        return data
