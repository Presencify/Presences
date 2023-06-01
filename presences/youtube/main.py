import time

"""
In this example, "runtime" is used to first retrieve the "mediaSession", which allows us to obtain information such as author, image, etc.
Then, the URL is checked to see if it is from YouTube to continue updating the presence.
Note this example updates every 2 seconds but the real presence updates every 15 seconds.
"""

while running:
    media = runtime.mediaSession()
    url = runtime.url
    if not "youtube.com" in url:
        continue
    if media is None:
        continue
    update_rpc(
        details="Viewing a video",
        state=media.title,
        large_image=media.image,
    )
    time.sleep(2)
