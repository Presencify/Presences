import time

while running:
    media = runtime.mediaSession()
    update_rpc(
        details="Viewing a video",
        state=media.title,
        large_image=media.image,
    )
    time.sleep(2)
