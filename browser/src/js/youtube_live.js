
export function getYouTubeLiveStream(channel_id = "UC5TaG-84yWqkwYU1NA1x5JQ", api_key = "AIzaSyBL2-f76mPBMWQ39UrJh1KIzSMJ86BDme4") {
    // let youTubeAPIURI = `https://www.googleapis.com/youtube/v3/search?part=snippet&channelId=${channel_id}&eventType=live&type=video&key=${api_key}`;
    // console.log(youTubeAPIURI);
    // fetch(youTubeAPIURI).then((response) => {
    //     let youTubeJsonResponse = response.json();
    //     console.log(youTubeJsonResponse);
    //     console.log(response);
        // if (youTubeJsonResponse.items.length !== 0) {
        //     console.log("Live Stream Available");
        // } else {
        //     console.log("Live Stream Unavailable")
        // }
    //
    // });
    let iFrame = document.getElementById("live-stream-frame");

    iFrame.addEventListener("load", () => {
        console.log("Player Loaded");
        console.log("Iframe: " + iFrame);
        let innerDoc = iFrame.contentDocument || iFrame.contentWindow.document;
        console.log("Inner: " + innerDoc);
        let player = document.getElementById("player");

        console.log("Player Elm: " + player);
    });
}