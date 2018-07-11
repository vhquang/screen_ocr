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
        self._stopper = threading.Event()

    def run(self):
        if self.delay != 0:
            time.sleep(self.delay)
        if not self._stopper.is_set():
            self.callback()

    def mark_stop(self):
        self._stopper.set()


class Capture_Windows ():
    def __init__(self, width=600, height=400):
        self._exit = False
        self.high_alpha = 0.6
        self.low_alpha = 0.07 * 10
        self.root = Tk()
        self.root.wm_attributes("-topmost", 1)
        self.root.geometry('{w}x{h}'.format(w=width, h=height))

        # put window's info at bottom of the window
        self.position_str = StringVar()
        message = Message(self.root, textvariable=self.position_str, width=150)
        message.pack(side=tkinter.BOTTOM)

        self.root.attributes('-alpha', 0.1)
        self.root.bind("<Enter>", self.mouseEnter)
        self.root.bind("<Leave>", self.mouseLeave)
        self.root.protocol("WM_DELETE_WINDOW", self.on_quit)

    def increaseAlpha(self):
        self.root.attributes('-alpha', self.high_alpha)

    def decreaseAlpha(self):
        if not self._exit:
            self.root.attributes('-alpha', self.low_alpha)

    def mouseEnter(self, event):
        """
        Increase window' opacity when mouse hover.
        """
        for thread in threading.enumerate():
            if isinstance(thread, Stoppable_Thread):
                thread.mark_stop()
        self.increaseAlpha()

    def mouseLeave(self, event):
        """
        Decrease window's opacity 2 seconds after mouse leave.
        """
        thread = Stoppable_Thread(1, self.decreaseAlpha)
        thread.start()

    def on_quit(self):
        self._exit = True
        self.root.destroy()

    def output(self):
        # print (root.winfo_width())
        # print (root.winfo_height())
        # print (root.winfo_reqwidth())
        info_str = self.root.geometry()
        # width,height,posX,posY = [int(x) for x in re.split(r'[x+]', info_str)]
        posX = self.root.winfo_rootx()
        posY = self.root.winfo_rooty()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        display_message = "X: %d, Y: %d \n W: %d H: %d"%(posX, posY, width, height)
        self.position_str.set( display_message )

        caputure_box = posX, posY, posX+width, posY+height-20
        # img = ImageGrab.grab(caputure_box)
        # img.show()

        start = time.clock()
        # print(pytesser.image_to_string(img))
        # print(time.clock() - start)

        if not self._exit:
            self.root.after(200, self.output)

    def run(self):
        self.root.after(200, self.output)
        self.root.mainloop()


if __name__ == '__main__':
    capture = Capture_Windows()
    capture.run()
