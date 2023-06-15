import time

# Function to get the current video metadata
videometadata_func = """
function getVideoMetadata(){
    let appId = Object.keys(netflix.appContext.state.playerApp.getState().videoPlayer.videoMetadata)[0];
    if (!appId) return '';
    let video = netflix.appContext.state.playerApp.getState().videoPlayer.videoMetadata[appId]._metadata.video;
    return [video.type, video.title, video.boxart[0].url].join('#');
}
"""

# Function to get the current show metadata
showmetadata_func = """
function getShowMetadata(){
    let appId = Object.keys(netflix.appContext.state.playerApp.getState().videoPlayer.videoMetadata)[0];
    let seasons = netflix.appContext.state.playerApp.getState().videoPlayer.videoMetadata[appId]._metadata.video.seasons;
    let foundEpisode = null;
    let foundSeason = null;
    seasons.some(season => {
        return season.episodes.some((episode, index) => {
            if (episode.episodeId === parseInt(appId)) {
                foundSeason = season;
                foundEpisode = episode;
                episodeNumber = index + 1;
                return;
            }
        });
        if (foundEpisode && foundSeason && episodeNumber)
            return;
    });
    return `${foundSeason.shortName} E${episodeNumber}: ${foundEpisode.title}`;
}
"""

# Not uses assets
netflix_logo = "https://images.ctfassets.net/4cd45et68cgf/Rx83JoRDMkYNlMC9MKzcB/2b14d5a59fc3937afd3f03191e19502d/Netflix-Symbol.png"
check_time = 10  # Time to check for updates (in seconds)

while running:
    tab = runtime.current_tab

    # Not on Netflix
    if "netflix.com" not in tab.url:
        time.sleep(check_time)
        continue

    # Not watching anything, just browsing
    if "browse" in tab.url:
        update_rpc(details="Browsing...", large_image=netflix_logo)
        time.sleep(check_time)
        continue

    # Watching something
    tab.execute(videometadata_func)
    video_metadata = tab.execute("getVideoMetadata()")

    # Skip if no metadata
    if video_metadata == "":
        continue

    # Extract each metadata
    video_type, video_title, video_image = video_metadata.split("#")
    is_paused = tab.execute("document.querySelector('video').paused")

    if len(video_image) > 128:
        print("[Netflix] Video image is too large, skipping")
        video_image = netflix_logo

    if len(video_title) > 128:
        video_title = video_title[:125] + "..."

    # If watching a show
    if video_type == "show":
        tab.execute(showmetadata_func)
        info = tab.execute("getShowMetadata()")
        update_rpc(
            details=info,
            state=video_title,
            large_image=video_image,
            small_image="pause" if is_paused else "play",
            small_text="Paused" if is_paused else "Playing",
        )

    # If watching a movie
    elif video_type == "movie":
        update_rpc(
            details=video_title,
            state="Watching a Movie",
            large_image=video_image,
            small_image="pause" if is_paused else "play",
            small_text="Paused" if is_paused else "Playing",
        )

    # Wait for next check
    time.sleep(check_time)
