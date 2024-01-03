import pyxbmct
import xbmc
import socket
import threading
import json
import requests
import os
import difflib

MEDIA_DIR = r"C:\Users\user\Videos"

def log(stuff):
    xbmc.log(str(stuff), xbmc.LOGINFO)


def findFile(query):
    dr = [r for r in os.listdir(MEDIA_DIR) if os.path.join(MEDIA_DIR, r)]
    rs = difflib.get_close_matches(query, dr, n=1)
    if rs:
        path = os.path.join(MEDIA_DIR, rs[0])
    else:
        path = None
    return path

class Server:

    def __init__(self, port):
        self.player = xbmc.Player()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(("localhost", port))
        #self.socket.setblocking(False)
        threading.Thread(target=self.process).start()
    
    def process(self):
        while True:
            data = self.socket.recv(1024).decode("utf-8")
            if data:
                log(data)
                cmd = json.loads(data)
                if cmd[0] == "play":
                    path = findFile(cmd[1])
                    if path != None:
                        self.player.play(path)
                    self.playing = True
                elif cmd[0] == "pause":
                    if self.playing:
                        self.player.pause()
                        self.playing = False
                elif cmd[0] == "resume":
                    if not self.playing:
                        self.player.pause()
                        self.playing = True
                elif cmd[0] == "stop":
                    self.player.stop()
                    self.playing = False
    
    def __del__(self):
        self.socket.close()

class Window(pyxbmct.AddonDialogWindow):
    
    def __init__(self, bot_port):
        super().__init__("MIbot")
        self.bot_port = bot_port

        self.setGeometry(900, 700, 12, 6)

        self.submit_button = pyxbmct.Button('Send')
        self.placeControl(self.submit_button, 11, 5)

        self.chat_history = pyxbmct.List()
        self.placeControl(self.chat_history, 0, 0, rowspan=11, columnspan=6)

        self.edit = pyxbmct.Edit("")
        self.placeControl(self.edit, 11, 0, columnspan=5)

        self.setFocus(self.edit)

        self.connect(self.submit_button, self.submit)
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)

        self.doModal(pyxbmct.AddonDialogWindow)
    
    def requestResponse(self, msg):
        url = "http://localhost:%i/webhooks/rest/webhook" % self.bot_port
        payload = {"sender": "user", "message": msg}
        res = requests.post(url, json=payload)
        data = res.json()
        log(data)
        for botmsg in data:
            self.chat_history.addItem("MIbot: %s" % botmsg["text"])
    
    def submit(self):
        text = self.edit.getText()

        self.chat_history.addItem("You: %s" % text)
        threading.Thread(target=self.requestResponse, args=[text]).start()

        lastidx = self.chat_history.size() - 1
        self.setFocus(self.chat_history.getListItem(lastidx))

        self.edit.setText("")

server = Server(1234)
window = Window(5005)

del window
del server
