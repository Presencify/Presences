import time
import asyncio
from typing import Callable, Any
from .client import Client
from .runtime import Runtime


class Presence:

    __slots__ = ("__client_id", "__callbacks", "__running", "__name", "runtime")
    data = {
        "details": "Presencify",
        "state": "no state",
    }

    def __init__(self, client_id: str, name: str = "PresencifyRPC") -> None:
        self.__client_id = client_id
        self.__callbacks = {}
        self.__name = name
        self.__running = False
        self.runtime = Runtime()

    def on(self, event: str, callback: Callable[..., Any]) -> None:
        self.__callbacks[event] = callback

    def stop(self) -> None:
        if self.__running:
            self.__running = False
            asyncio.run(self.__close_rpc())

    async def __init_rpc(self) -> None:
        async with Client(port=6996) as client:
            await client.send(
                {
                    "opcode": 0,
                    "client_id": self.__client_id,
                    "name": self.__name,
                    "payload": self.data,
                }
            )
            res = await client.recv()
            if res == "OK":
                print("Successfully connected to Presencify")

    async def __update_rpc(self) -> None:
        async with Client(port=6996) as client:
            await client.send(
                {
                    "opcode": 1,
                    "name": self.__name,
                    "client_id": self.__client_id,
                    "payload": self.data,
                }
            )
            res = await client.recv()
            if res == "OK":
                print("Successfully updated to Presencify")

    async def __close_rpc(self) -> None:
        async with Client(port=6996) as client:
            await client.send(
                {
                    "opcode": 2,
                    "name": self.__name,
                    "client_id": self.__client_id,
                }
            )
            res = await client.recv()
            if res == "OK":
                print("Successfully closed connection to Presencify")

    def start(self) -> None:
        self.__running = True
        try:
            asyncio.run(self.__init_rpc())
        except Exception as exc:
            print("Could not connect to Presencify, you running it?")
            return
        try:
            self.__event_update()
        except KeyboardInterrupt:
            self.stop()

    def update(self, data: dict) -> None:
        self.data.update(data)

    def __event_update(self):
        while self.__running:
            if "update" in self.__callbacks:
                self.__callbacks["update"](self)
            asyncio.run(self.__update_rpc())
            time.sleep(15)
