import time

videometadata_func = """
function getVideoMetadata(){
    let appId = Object.keys(netflix.appContext.state.playerApp.getState().videoPlayer.videoMetadata)[0];
    if (!appId) return '';
    let video = netflix.appContext.state.playerApp.getState().videoPlayer.videoMetadata[appId]._metadata.video;
    return [video.type, video.title, video.boxart[0].url].join('#');
}
"""

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
netflix_logo = "https://images.ctfassets.net/4cd45et68cgf/Rx83JoRDMkYNlMC9MKzcB/2b14d5a59fc3937afd3f03191e19502d/Netflix-Symbol.png"
check_time = 5

while running:
    if "netflix.com" not in runtime.url:
        time.sleep(check_time)
        continue
    if "browse" in runtime.url:
        update_rpc(details="Browsing...", large_image=netflix_logo)
        time.sleep(check_time)
        continue
    runtime.execute(videometadata_func)
    video_metadata = runtime.execute("getVideoMetadata()")
    if video_metadata == "":
        continue
    video_type, video_title, video_image = video_metadata.split("#")
    if video_type == "show":
        runtime.execute(showmetadata_func)
        info = runtime.execute(f"getShowMetadata()")
        update_rpc(
            details=info,
            state=video_title,
            large_image=video_image,
        )
    elif video_type == "movie":
        update_rpc(
            details=video_title,
            state="Watching a Movie",
            large_image=video_image,
        )
    time.sleep(check_time)
