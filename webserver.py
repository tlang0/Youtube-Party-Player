# run server: twistd -y webserver.py -n
# served player: http://localhost:8880/player/?videoID=j2TDoGsA43Y

from pprint import pprint
from twisted.application.internet import TCPServer
from twisted.application.service import Application
from twisted.web.resource import Resource
from twisted.web.server import Site
from twisted.web.static import File
import socket
import sys

class PartyServer():
    
    def connect(self,server,port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((server, port))
    
    def send(self,cmd):
        self.client.send(cmd)
    
    def quit(self):    
        self.client.close()
        

class FormPage(Resource):
   	
    def render_GET(self, request):
        return ''

    def render_POST(self, request):
        request.setHeader('Access-Control-Allow-Origin', '*')
    	request.setHeader('Access-Control-Allow-Methods', 'GET')
    	request.setHeader('Access-Control-Allow-Headers','x-prototype-version,x-requested-with')
    	request.setHeader('Access-Control-Max-Age', 2520)
    	request.setHeader('Content-type', 'application/json') 
        pprint(request.__dict__)
        newdata = request.content.getvalue()
        print newdata
        
        ytplayer = PartyServer()
    	ytplayer.connect("127.0.0.1",3421) # lokaler yt-partyplayer server
    	ytplayer.send(newdata)
    	ytplayer.quit()
        
        return ''


root = Resource()
root.putChild("callback", FormPage()) # xhttprequest 
root.putChild("player", File("./")) # static player page
root.putChild("client", File("./client.html")) # client page
root.putChild("js", File("./js/"))
root.putChild("css", File("./css/"))
application = Application("My Web Service - PartyPlayer")
TCPServer(8880, Site(root)).setServiceParent(application)
