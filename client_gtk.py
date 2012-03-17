# python3
# gtk3

import socket
import sys
from gi.repository import Gtk

class PartyConnecter():

    def connect(self, server, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((server, port))

    def send(self, cmd):
        self.client.send(cmd.decode("UTF-8"))

    def quit(self):
        self.client.close()

class PartyWindow(Gtk.Window):
    
    def __init__(self):
        Gtk.Window.__init__(self, title="Youtube Party Player")

        self.vboxMain = Gtk.Box(spacing=6, orientation=Gtk.Orientation.VERTICAL)
        self.add(self.vboxMain)

        # search box
        self.hboxSearch = Gtk.Box(spacing=6)
        self.entrySubject = Gtk.Entry()
        self.btnSearch = Gtk.Button(label="Search")
        self.btnURL = Gtk.Button(label="Open URL")
        self.hboxSearch.pack_start(self.entrySubject, True, True, 0)
        self.hboxSearch.pack_start(self.btnSearch, True, True, 0)
        self.hboxSearch.pack_start(self.btnURL, True, True, 0)

        self.btnSearch.connect("clicked", self.on_btnSearch_clicked)
        self.btnURL.connect("clicked", self.on_btnURL_clicked)
        
        # connection box
        self.hboxConnection = Gtk.Box(spacing=6)
        self.entryAddr = Gtk.Entry()
        self.entryAddr.set_text("192.168.1.10")
        self.entryPort = Gtk.Entry()
        self.entryPort.set_width_chars(5)
        self.entryPort.set_text("3421")
        self.hboxConnection.pack_start(self.entryAddr, True, True, 0)
        self.hboxConnection.pack_start(self.entryPort, True, True, 0)
        
        self.vboxMain.pack_start(self.hboxSearch, True, True, 0)
        self.vboxMain.pack_start(self.hboxConnection, True, True , 0)

    def send_to_server(self, msg):
        player = PartyConnecter()
        player.connect(self.entryAddr.get_text(), int(self.entryPort.get_text()))
        player.send(msg)
        player.quit()

    def on_btnSearch_clicked(self, widget):
        self.send_to_server("play {}".format(self.entrySubject.get_text()))

    def on_btnURL_clicked(self, widget):
        self.send_to_server("url {}".format(self.entrySubject.get_text()))

def main():
    win = PartyWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()
