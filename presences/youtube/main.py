import time

while running:
    url = runtime.url
    if not "youtube.com" in url:
        continue
    media = runtime.mediaSession()
    if media is None:
        continue
    update_rpc(
        details="Viewing a video",
        state=media.title,
        large_image=media.image,
    )
    time.sleep(2)
