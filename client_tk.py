from Tkinter import *
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

master = Tk()
master.title("Youtube Party Player") 
master.geometry("%dx%d%+d%+d" % (380, 80, 0, 0))

input_entry = Entry(master)
input_entry.pack()
input_entry.place(x=10, y=10, width=250)

input_entry.focus_set()

ip_entry = Entry(master)
ip_entry.pack()
ip_entry.place(x=10, y=45, width=250)
ip_entry.insert(0, "192.168.1.109")

port_entry = Entry(master)
port_entry.pack()
port_entry.place(x=265, y=45, width=105)
port_entry.insert(0, "3421")

def callback_play():
    ytplayer = PartyServer()
    ytplayer.connect(ip_entry.get(),int(port_entry.get()))
    ytplayer.send('play ' + input_entry.get())
    ytplayer.quit()
def callback_url():
    ytplayer = PartyServer()
    ytplayer.connect(ip_entry.get(),int(port_entry.get()))
    ytplayer.send('url ' + input_entry.get())
    ytplayer.quit()

btn_play = Button(master, text="Play", width=10, command=callback_play)
btn_play.pack()
btn_play.place(x=265,y=10, width=50)

btn_url = Button(master, text="URL", width=10, command=callback_url)
btn_url.pack()
btn_url.place(x=260+60,y=10, width=50)

mainloop()
input_entry = Entry(master, width=300)
input_entry.pack()



