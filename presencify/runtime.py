import urllib.request as req
from .client import Client
from .logger import Logger
import json
import asyncio


class Runtime:
    __pages = []
    __ENDPOINT = "http://localhost:9222/json"
    __CURRENT_PAGE = None

    def __init__(self):
        self.__ws = None
        self.__enabled = False

    def get_pages(self):
        res = req.urlopen(self.__ENDPOINT)
        return res.read().decode("utf-8")

    def update_pages(self):
        loaded_pages = json.loads(self.get_pages())
        self.__pages = list(filter(lambda x: x["type"] == "page", loaded_pages))
        self.__CURRENT_PAGE = self.__pages[0]
        print("Updated pages")

    def enable(self):
        try:
            self.get_pages()
        except Exception as exc:
            Logger.write(
                msg="Could not connect to Remote Debugging, is it running?",
                level="error",
                origin=self,
            )
            exit(1)
        Logger.write(msg="Runtime connected to Remote Debugging successfully")
        self.__enabled = True
        self.update_pages()

    async def __send(self, data) -> None:
        async with Client(url=self.__CURRENT_PAGE["webSocketDebuggerUrl"]) as client:
            await client.send(data)
            data = await client.recv()
            return data

    # browser.exe --remote-debugging-port=9222 --allowed-origin=*
    def execute(self, script: str) -> None:
        if not self.__enabled:
            Logger.write(
                msg="Not enabled, cannot execute script", level="warning", origin=self
            )
            return
        self.update_pages()
        response = asyncio.run(
            self.__send(
                {
                    "id": 1,
                    "method": "Runtime.evaluate",
                    "params": {"expression": script},
                }
            )
        )
        data = json.loads(response)
        return data["result"]["result"]
