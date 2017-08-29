#!/bin/python2

import subprocess
import Tkinter as tk

# select lastlat, lastlon from network order by lasttime asc;
# select lastlat, lastlon from network order by lasttime asc;
raw = subprocess.check_output('sqlite3 wigle "select lat, lon from location"', shell=True)

loc = raw.split('\n')
loc = loc[:-1]
#print loc
for i in range(0, len(loc)):
    loc[i] = loc[i].split('|')
    loc[i][0] = int(round((float(loc[i][0]) - 38) * 500))
    loc[i][1] = int(round((float(loc[i][1]) - 58) * 300))

class View(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.prevX = loc[i][1]
        self.prevY = loc[i][0]
        self.createWidgets()

    def drawPoint(self, x, y):
        #self.canvas.create_line(self.prevX, self.prevY, x, y)
        self.canvas.create_rectangle(x-200, 100-y, (x+3)-200, 100-(y+5), fill='black')
        self.prevX = x
        self.prevY = y

    def createWidgets(self):
        self.canvas = tk.Canvas(self, width=800, height=100)
        self.canvas.grid()
        self.canvas.__getitem__
        for l in loc:
            self.drawPoint(l[1], l[0])


print "FLAG = FLAG{F0UND_M3_2BD3F768}"

v = View()
v.mainloop()
