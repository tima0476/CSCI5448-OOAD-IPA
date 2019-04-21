#!/usr/bin/env python3

# based from example tkinter code in "Programming Python, 4ed" by Mark Lutz

import tkinter as tk
from tkinter import ttk
from PIL import Image
from PIL.ImageTk import PhotoImage 
from ScrolledCanvas import ScrolledCanvas

imgdir = "/Users/tim/Google Drive/Spring 2019/csci5448/Project/github/CSCI5448-OOAD-IPA/test_images/"
filename1 = '2008 Colder Bolder-55.jpg'
filename2 = 'Evelyn Smash Burger.jpg'

class IPA:
	"""
	This is the main program class of IPA: Image Processing Application. 
	"""
	def __init__(self):
		self.mainFrame = ttk.Frame(parent=None)
		self.mainFrame.pack()
		self.mainFrame.master.title("IPA: Image Processing Application")

		self.tkImages = []		# for aggregation of tkInter image objects
		
		self.nb = ttk.Notebook(self.mainFrame, padding=0) # height and width are for size of initial blank Notebook
		self.nb.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.TRUE)

		ttk.Button(self.mainFrame, text="Close").pack(side=tk.RIGHT)
		ttk.Button(self.mainFrame, text="Save...").pack(side=tk.RIGHT)
		ttk.Button(self.mainFrame, text='Open...', command=self.openButton).pack(side=tk.RIGHT)

		# To Do if time:  Can I improve the packing of the widgets so the buttons don't collapse away on size-down?

	def go(self):
		"""
		Start the application running by firing off the tkInter event loop 
		"""
		self.mainFrame.mainloop()

	def openButton(self):
		print("Pressed Open...")
		self.openImage(imgdir, filename1)

	def openImage(self, path, filename):
		"""
		Given a path name, open the image file and add a tab to display it.
		"""
		print("openImage({},{})".format(path,filename))
		# Open the image file using PIL and save a reference to the image object (aggregation)
		pilImage = Image.open(path + filename)
		tkImage = PhotoImage(image=pilImage)

		self.tkImages.append(tkImage)	# must keep a reference so it doesn't get garbage collected.

		# Add a tab to the main frame's notebook object, and display the image on that tab pane
		frame = ttk.Frame(self.nb)
		self.nb.add(frame, text=filename)

		canvas = ScrolledCanvas(frame)

		# compute a maximum size based on the display size, leaving some buffer for other UI elements
		screenW = self.mainFrame.winfo_screenwidth()-40
		screenH = self.mainFrame.winfo_screenheight()-150

		# create the canvas object on which the image will be displayed
		canvas.config(width=min(screenW,tkImage.width()), height=min(screenH,tkImage.height()))	# size of the image region on screen
		canvas.config(scrollregion=(0, 0, tkImage.width(), tkImage.height()))					# virtual size of the image
		canvas.create_image(0, 0, image=tkImage, anchor=tk.NW)				 					# 0,0 is the relative coordinates of the image
		canvas.pack(fill=tk.BOTH)




if __name__ == '__main__':
	ipa = IPA()
	ipa.go()			# This call doesn't return until the application terminates