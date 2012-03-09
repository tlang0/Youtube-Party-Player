import socket
from socket import AF_INET, SOCK_STREAM
import webbrowser
import gdata
import gdata.youtube
import gdata.youtube.service

OPENURL = "url "
SEARCH = "play "

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
    print "Opening URL: {0}\n".format(url)
    webbrowser.open(url, new=0)

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
        print "{0} connected".format(addr)
        data = c.recv(1024)
        if not data:
            print "Failed to receive data, try again."
            c.close()
            continue
        print "<< " + data
        if data.startswith(OPENURL):
            url = data[len(OPENURL):]
            open_url(url)
        elif data.startswith(SEARCH):
            subject = data[len(SEARCH):]
            print "Searching on youtube for {0}...".format(subject)
            feed = search_youtube(subject)
            if not feed or len(feed.entry) == 0:
                c.close()
                continue
            firstentry = feed.entry[0]
            url = firstentry.media.player.url
            open_url(url)
        c.close()

if __name__ == "__main__":
    main()
