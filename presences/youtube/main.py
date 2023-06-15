"""
This version only updates the presence when the tab is active.
So if you have multiple Youtube tabs open, it will only update the active one.
"""
import time

while running:
    tab = runtime.current_tab
    if not "www.youtube.com" in tab.url:
        time.sleep(10)
        continue

    media = tab.media_session()
    if not media:
        time.sleep(10)
        continue

    channel_url = tab.execute("document.querySelector('#text > a').href")
    paused = media.state == "paused"
    update_rpc(
        details=media.artist,
        state=media.title,
        large_image=media.image,
        small_image="pause" if paused else "play",
        small_text=media.state.capitalize(),
        buttons=[
            {"label": "Play Video", "url": tab.url},
            {"label": "View Channel", "url": channel_url},
        ],
    )

    time.sleep(10)
