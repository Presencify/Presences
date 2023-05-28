from presencify import Presence


def get_website(presence):
    res = presence.runtime.execute("document.title")
    presence.update(
        {
            "details": res.value,
            "state": "In a website",
        }
    )


presence = Presence(client_id="yourclientid", name="Website")
presence.runtime.enable()
presence.on("update", get_website)
presence.start()
