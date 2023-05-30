import time
import presencify

while running:
    url = presencify.Runtime.execute("window.location.href")
    if not "youtube.com" in url:
        update({"state": "Not watching a video", "details": "Browsing YouTube"})
    title = presencify.Runtime.execute("document.title")
    update({"state": title, "details": "Watching a video"})
    time.sleep(15)
