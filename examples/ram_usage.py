from presencify import Presence
import psutil


def get_ram_usage(presence):
    ram = psutil.virtual_memory()
    presence.update(
        {
            "details": f"{ram.percent}%",
            "state": "RAM Usage",
        }
    )

presence = Presence(client_id="yourclientid", name="RAM Usage")
presence.on("update", get_ram_usage)
presence.start()
