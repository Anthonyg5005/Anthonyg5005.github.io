// ==UserScript==
// @name         YouTube Shorts Blocker: My Attention Span's Last Hope
// @namespace    http://tampermonkey.net/
// @version      0.5
// @description  Outsmart the algorithm.  Restores your ability to watch single videos without falling into the Shorts abyss. (Still lets you click the Shorts button if you *want* to lose 3 hours.)
// @author       Gemini 1.5 Pro + Claude Sonnet + GPT o4
// @match        https://www.youtube.com/*
// @grant        none
// ==/UserScript==
// Make sure to have tampermonkey installed, if this was downloaded as a file then it's not installed/enabled

(function() {
    'use strict';

    function getVideoIdFromShortsUrl(url) {
        try {
            const urlObj = new URL(url);
            if (urlObj.pathname.startsWith('/shorts/')) {
                return urlObj.pathname.split('/shorts/')[1].split('?')[0];
            } else if (urlObj.searchParams.has('feature') && urlObj.searchParams.get('feature') === 'shorts') {
                // Handles URLs like https://www.youtube.com/watch?v=VIDEO_ID&feature=shorts
                return urlObj.searchParams.get('v');
            }
        } catch (e) {
            console.error("Error parsing URL:", e);
        }
        return null;
    }

    function redirectShorts() {
        const videoId = getVideoIdFromShortsUrl(window.location.href);
        if (videoId) {
            window.location.href = `https://www.youtube.com/watch?v=${videoId}`;
        }
    }

    function convertShortLinks(links) {
        links.forEach(link => {
            const videoId = getVideoIdFromShortsUrl(link.href);
            if (videoId && link.href !== `https://www.youtube.com/watch?v=${videoId}`) {
                link.href = `https://www.youtube.com/watch?v=${videoId}`;
            }
        });
    }

    function init() {
        redirectShorts();
        convertShortLinks(document.querySelectorAll('a[href*="/shorts/"], a[href*="&feature=shorts"]'));
    }

    // Initial check
    init();

    // Observe changes in the DOM with throttling
    let timeout;
    const observer = new MutationObserver(() => {
        clearTimeout(timeout);
        timeout = setTimeout(() => {
            convertShortLinks(document.querySelectorAll('a[href*="/shorts/"], a[href*="&feature=shorts"]'));
        }, 100);
    });

    observer.observe(document, { childList: true, subtree: true });
})();
