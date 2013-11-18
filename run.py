from pytesser import *
from Tkinter import *
from PIL import ImageGrab
import time
import re
import threading

root = Tk()
root.attributes('-alpha', 0.1)
root.geometry("400x600")

# root.update()

# print (root.winfo_width())
# print (root.winfo_height())
# print (root.winfo_reqwidth())

position_str = StringVar()
Message(root, textvariable=position_str, width=150).pack(side=BOTTOM)
runOnce = False
count = 0

class StoppableThread (threading.Thread):
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

def increaseAlpha():
	global root
	root.attributes('-alpha', 0.5)

def decreaseAlpha():
	global root
	root.attributes('-alpha', 0.03)

def mouseEnter(event):
	for thread in threading.enumerate():
		if isinstance(thread, StoppableThread):
			thread.stop()
	increaseAlpha()

def mouseLeave(event):
	thread = StoppableThread(2, decreaseAlpha)
	thread.start()
	

root.bind("<Enter>", mouseEnter)
root.bind("<Leave>", mouseLeave)

def output():
	st = root.geometry()
	width,height,posX,posY = [int(x) for x in re.split(r'[x+]', st)]
	posX = root.winfo_rootx()
	posY = root.winfo_rooty()
	width = root.winfo_width()
	height = root.winfo_height()
	msg = "X: %d, Y: %d, W: %d H: %d"%(posX, posY, width, height)
	position_str.set( msg )

	global runOnce, count
	# count += 1
	if not runOnce:
		bbox = posX, posY, posX+width, posY+height-20
		img = ImageGrab.grab(bbox)
		# img.show()
		
		start = time.clock()
		# image = Image.open('phototest.tif')
		print( image_to_string(img) );
		print time.clock() - start

		if count > 20:
			# img.show()
			runOnce = True

	root.after(200,output)

root.after(200, output)
root.mainloop()