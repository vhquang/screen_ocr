from tkinter import Tk, StringVar, Message
import re
import tkinter
import time
import threading

# from PIL import ImageGrab
from Pytesser import pytesser


class Stoppable_Thread (threading.Thread):
    def __init__(self, delay, callback):
        threading.Thread.__init__(self)
        self.delay = delay
        self.callback = callback
        self._stop = threading.Event()

    def run(self):
        if self.delay != 0:
            time.sleep(self.delay)
        if not self._stop.isSet():
            self.callback()

    def stop(self):
        self._stop.set()


class Capture_Windows ():
    def __init__(self):
        self.exitFlag = False
        self.root = Tk()
        # put window's info at bottom of the window
        self.position_str = StringVar()
        Message(self.root, textvariable=self.position_str, width=150).pack(side=tkinter.BOTTOM)

        self.root.wm_attributes("-topmost", 1)
        self.root.geometry("600x400")
        self.root.attributes('-alpha', 0.1)
        # increase window' opacity when mouse hover
        self.root.bind("<Enter>", self.mouseEnter)
        # decrease window's opacity 2 seconds after mouse leave
        self.root.bind("<Leave>", self.mouseLeave)
        self.root.after(200, self.output)
        self.root.protocol("WM_DELETE_WINDOW", self.on_quit)
        self.root.mainloop()

        # root.update()
        # print (root.winfo_width())
        # print (root.winfo_height())
        # print (root.winfo_reqwidth())

    def increaseAlpha(self):
        self.root.attributes('-alpha', 0.6)

    def decreaseAlpha(self):
        # don't set attribute after the root been destroyed
        if not self.exitFlag:
            self.root.attributes('-alpha', 0.07)

    def mouseEnter(self, event):
        for thread in threading.enumerate():
            if isinstance(thread, Stoppable_Thread):
                thread.stop()
        self.increaseAlpha()

    def mouseLeave(self, event):
        thread = Stoppable_Thread(2, self.decreaseAlpha)
        thread.start()

    def on_quit(self):
        self.exitFlag = True
        self.root.destroy()

    def output(self):
        info_str = self.root.geometry()
        # width,height,posX,posY = [int(x) for x in re.split(r'[x+]', info_str)]
        posX = self.root.winfo_rootx()
        posY = self.root.winfo_rooty()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        display_message = "X: %d, Y: %d, W: %d H: %d"%(posX, posY, width, height)
        self.position_str.set( display_message )

        caputure_box = posX, posY, posX+width, posY+height-20
        # img = ImageGrab.grab(caputure_box)
        # img.show()

        start = time.clock()
        # print(pytesser.image_to_string(img))
        print(time.clock() - start)

        self.root.after(200, self.output)



if __name__ == '__main__':
    capture = Capture_Windows()