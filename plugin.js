// ==UserScript==
// @name         Interactive Twitter Media Downloader
// @namespace    http://tampermonkey.net/
// @version      2024-08-07
// @description  Grabs all twitter media links and sends them to localhost:5000
// @author       S1monr3dst0ne07
// @match        https://x.com/*
// @match        https://twitter.com/*
// @grant        GM_registerMenuCommand
// @grant        GM_unregisterMenuCommand
// @grant        GM.xmlHttpRequest
// @icon         data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==
// ==/UserScript==

(function() {
    'use strict';

    var running = false;

    var linkPool = new Set();
    var count = 0;

    function getNewMediaLinks() {
        let imgs = document.getElementsByTagName("img");
        var links = [];

        for (let img of imgs) {
            var link = img.src;
            if (linkPool.has(link)) continue;

            if (link.includes("/media/") ||
                link.includes("/ext_tw_video_thumb/") ||
                link.includes("/tweet_video_thumb/")
               ) {
                links.push(link);
                count++;
            }
            else
                console.log("filtered: " + link)



            linkPool.add(link);
        }

        return links;
    }

    function download(links) {
        GM.xmlHttpRequest({
            method: "POST",
            url: "http://localhost:5000",
            data: JSON.stringify({
                count  : links.length,
                content: links,
            }),
            headers: {
                "Content-Type": "application/json"
            },
        });
    }


    function loop() {
        var links = getNewMediaLinks();
        if (links.length) download(links);

        console.log("media find: " + count);

        if (running) setTimeout(loop, 200);
    }


    var menu = GM_registerMenuCommand("start", toggle);
    function toggle() {
        running = !running;

        GM_unregisterMenuCommand(menu);
        menu = GM_registerMenuCommand(running ? "stop" : "start", toggle);

        if (running) loop();
    }


})();