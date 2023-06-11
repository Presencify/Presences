import time

while running:
    url = runtime.url
    if not "www.youtube.com" in url:
        continue

    media = runtime.mediaSession()
    if not media:
        continue

    channel_url = runtime.execute("document.querySelector('#text > a').href")

    update_rpc(
        details=media.artist,
        state=media.title,
        large_image=media.image,
        buttons=[
            {"label": "Play Video", "url": url},
            {"label": "View Channel", "url": channel_url},
        ],
    )

    time.sleep(5)
