import time

check_time = 12

while running:
    tab = None
    current_tab = runtime.current_tab
    ytm_tabs = runtime.tabs(url_pattern="music.youtube.com")

    if "music.youtube.com" in current_tab.url:
        # Current tab is a YouTube Music tab
        tab = current_tab
    elif len(ytm_tabs) > 0:
        # If the current tab is not a YouTube Music tab, but there are YouTube Music tabs open, use the first one
        tab = ytm_tabs[0]

    if tab is None:
        # No YouTube Music tabs open
        print("No tab found")
        time.sleep(check_time)
        continue

    media = tab.media_session()

    if media is None and "channel" in tab.url:
        # YouTube Music tab is on a channel page (not playing anything)
        update_rpc(
            state="Browsing...",
            buttons=[
                {
                    "label": "View Channel",
                    "url": tab.url,
                },
            ],
        )
        time.sleep(check_time)
        continue

    # selector to get the artist url
    artist_url = tab.execute(
        'document.querySelector("span.subtitle.style-scope.ytmusic-player-bar > yt-formatted-string > a:nth-child(1)").href'
    )
    is_playing = media.state == "playing"
    update_rpc(
        state=media.title,
        details=media.artist,
        large_image=media.image,
        small_image="playing" if is_playing else "pause",
        small_text=media.state.capitalize(),
        buttons=[
            {
                "label": "Listen on YouTube Music",
                "url": tab.url,
            },
            {
                "label": "View Artist",
                "url": artist_url,
            },
        ],
    )
    time.sleep(check_time)
