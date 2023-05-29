"""
This is a simple example of how to use Presencify and create your own presence.

Author:
    Leo Araya (https://www.github.com/leoarayav)
"""
from presencify import Presence
from datetime import datetime

# Lets create a new function to get the current time
def get_current_time(presence: Presence) -> None:
    """
    This function will be called every 15 seconds 
    by default and will update the presence with the current time

    Args:
        presence (Presence): The presence object
    """
    presence.update(
        {
            "details": datetime.now().strftime("%H:%M:%S"),
            "state": "Current Time",
        }
    )

if __name__ == '__main__':
    # Create a new presence object
    presence = Presence(client_id="yourclientid", name="Current Time")

    # Bind the function to the update event
    presence.on("update", get_current_time)

    # Start the presence
    presence.start()