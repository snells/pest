from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput

from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.stacklayout import StackLayout
import livestreamer
import os
import subprocess
import sys
import threading

player = ""
if(len(sys.argv) == 2):
    player = sys.argv[1]

class Pest(Widget):
    pass

class PestApp(App):
    pass

class Qbut(Button):
    def __init__(self, **kwargs):
        super(Qbut, self).__init__(**kwargs)
    link = ""
    btype = 0
    def start(self):
        global player
        cmd = "livestreamer " + self.link + " --player " + player #" --player mpv"
        if(self.btype == 2):
            print(cmd)
            subprocess.Popen(cmd.split())
        elif(self.btype == 1):
            self.parent.rem()
        elif(self.btype == 0):
            self.parent.refresh()

        

class But(Button):
    def __init__(self, **kwargs):
        super(But, self).__init__(**kwargs)

class StreamRow(BoxLayout):
    def __init__(self, **kwargs):
        super(StreamRow, self).__init__(**kwargs)
    online = False
    link = ""
    name = ""
    state = ""
    qualities = []
    cq = ""
    def rem(self):
        self.parent.rem(self)
    def refresh(self):
        self.clear_widgets()
#        for key, val in self.ids.items():
#                self.remove_widget(val)
        x = Qbut(width = 300)
        x.btype = 0
        x.text = self.name
        y = Qbut(width = 50)
        y.btype = 1
        y.text = "del"
        self.link = "www.twitch.tv/" + self.name[:-1]
        self.add_widget(x)
        self.add_widget(y)
        links = livestreamer.streams(self.link)
        if(links):
            self.qualities = links.keys()
            self.online = True
            self.state = "online"
            for a in self.qualities:
                b = Qbut(text=a, width = 100)
                b.link = self.link + " " + a
                b.btype = 2
                self.add_widget(b)
        else:
            self.online = False
            self.state = "offline"
            self.qualities = []

        x.text = self.name + " " + self.state
        
        
        
class Cont(StackLayout):
    def __init__(self, **kwargs):
        super(Cont, self).__init__(**kwargs)
        path = os.path.abspath(os.path.expanduser("~") + "/.pest")
        self.path = path
        self.names = []
        if(os.path.isfile(path)):
            self.read()
        else:
            f = open(path, 'a+')
            f.close()
        for a in self.names:
            self.add_row(a)

    def refresh(self):
        for w in self.walk():
            if(isinstance(w, StreamRow)):
                threading.Thread(target=w.refresh)
                #w.refresh()
        
    def read(self):
        f = open(self.path)
        l = f.readline()
        while(l):
            self.names.append(l)
            l = f.readline() 
        f.close()

    def add_name(self, name):
        f = open(self.path, 'a+')
        f.write(name)
        f.write(os.linesep)
        f.close()

    def rem_name(self, name):
        f = open(self.path, 'r+')
        lines = f.readlines()
        f.seek(0)
        for line in lines:
            if(line != name):
                f.write(line)
        f.truncate()
        f.close()
    def add_row(self, name):
        link = "http://www.twitch.tv/" + name
        b = StreamRow()
        b.size_hint = (1, 0.1)
        b.link = link
        b.name = name
        #threading.Thread(target=b.refresh)
        b.refresh()
        self.add_widget(b)

    def rem(self, row):
        self.rem_name(row.name)
        self.remove_widget(row)
    
class Panel(BoxLayout):
    def __init__(self, **kwargs):
        super(Panel, self).__init__(**kwargs)

    def add_new(self):
        if(self.ids.ti.text != ""):
            self.parent.add_row(self.ids.ti.text)
            self.parent.add_name(self.ids.ti.text)
            self.ids.ti.text = ""
        

    def refresh(self):
        self.parent.refresh()

    


if __name__ == '__main__':
    PestApp().run()
