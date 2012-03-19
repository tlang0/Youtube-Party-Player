#!/usr/bin/python3
# -*- coding: utf8 -*-

import socket
import webbrowser
import gdata
import gdata.youtube
import gdata.youtube.service
import re
from collections import deque
from socket import AF_INET, SOCK_STREAM

class Logger:
    """Simple Logger"""
    
    def info(self, data):
        print("log: {0}".format(data))

    def warning(self, data):
        print("warning: {0}".format(data))

    def error(self, data):
        print("error: {0}".format(data))

    def debug(self, data):
        print("debug: {0}".format(data))

    def recv(self, data):
        print("<< {0}".format(data))

OPENURL = "url "
SEARCH = "play "
END = "fin "

playlist = deque([])
log = Logger()
currently_playing = False

def search_youtube(search_terms, orderby="relevance", racy="include"):
    """Returns a feed containing the entrys"""
    service = gdata.youtube.service.YouTubeService()
    query = gdata.youtube.service.YouTubeVideoQuery()
    query.vq = search_terms
    query.orderby = orderby
    query.racy = racy
    feed = service.YouTubeQuery(query)
    return feed

def open_url(url):
    log.info("Opening URL: {0}\n".format(url))
    webbrowser.open(url, new=0)

def get_youtube_id_from_url(url):
    match = re.match(".*[&|\?]v=([A-Za-z0-9]{11}).*", url)
    video_id = None
    if match:
        video_id = match.groups()[0]
    return video_id

def open_webplayer_with_id(video_id):
    webplayer_url = "http://localhost:8880/player/?videoID={0}".format(video_id)
    webbrowser.open(webplayer_url, new=0)
    currently_playing = True

def main():
    s = socket.socket(AF_INET, SOCK_STREAM)
    host = socket.gethostname()
    port = 3421
    s.bind(("", port))

    # wait for client
    s.listen(1)

    # receive
    while True:
        c, addr = s.accept()
        log.info("{0} connected".format(addr))
        data = c.recv(1024)
        if not data:
            log.warning("Failed to receive data, try again.")
            c.close()
            continue
        log.recv(data)
        url = ""

        if data.startswith(OPENURL):
            url = data[len(OPENURL):]
        elif data.startswith(SEARCH):
            subject = data[len(SEARCH):]
            log.info("Searching on youtube for {0}...".format(subject))
            feed = search_youtube(subject)
            if not feed or len(feed.entry) == 0:
                c.close()
                continue
            firstentry = feed.entry[0]
            url = firstentry.media.player.url
        elif data.startswith(END):
            currently_playing = False
            if len(playlist) > 0:
                open_webplayer_with_id(playlist.popleft())

        if url:
            video_id = get_youtube_id_from_url(url)
            if currently_playing:
                playlist.append(video_id)
            else:
                open_webplayer_with_id(video_id)

        c.close()

if __name__ == "__main__":
    main()
