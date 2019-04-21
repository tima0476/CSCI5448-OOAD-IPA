#!/usr/bin/env python3

# based from example tkinter code in "Programming Python, 4ed" by Mark Lutz

import tkinter as tk
from tkinter import ttk

from PIL import Image
from PIL.ImageTk import PhotoImage 

imgdir = "/Users/tim/Google Drive/Spring 2019/csci5448/Project/github/CSCI5448-OOAD-IPA/test_images/"
filename2 = 'Evelyn Smash Burger.jpg'
filename1 = '2008 Colder Bolder-55 smaller.jpg'


class IPA:
	"""
	This is the main program class of IPA: Image Processing Application. 
	"""
	def __init__(self):
		self.mainFrame = ttk.Frame(parent=None)
		self.mainFrame.pack()
		self.mainFrame.master.title("IPA: Image Processing Application")

		self.pilImages = []
		self.tkImages = []
		# self.imageTabs = []

		self.nb = ttk.Notebook(self.mainFrame, padding=0)
		self.nb.pack()

		ttk.Button(self.mainFrame, text="Close").pack(side=tk.RIGHT)
		ttk.Button(self.mainFrame, text="Save...").pack(side=tk.RIGHT)
		ttk.Button(self.mainFrame, text='Open...', command=self.openButton).pack(side=tk.RIGHT)

	def go(self):
		self.mainFrame.mainloop()

	def openButton(self):
		print("Pressed Open...")
		self.openImage(imgdir, filename1)

	def openImage(self, path, filename):
		print("openImage({},{})".format(path,filename))
		# Open the image file using PIL and save a reference to the image object (aggregation)
		pilImage = Image.open(path + filename)
		tkImage = PhotoImage(image=pilImage)

		# self.pilImages.append(pilImage)
		self.tkImages.append(tkImage)	# must keep a reference so it doesn't get garbage collected.

		# Add a tab to the main frame's notebook object, and display the image on that tab pane
		frame = ttk.Frame(self.nb)
		# self.imageTabs.append(frame)
		self.nb.add(frame, text=filename)
		# self.nb.pack()			# todo: necessary?

		canvas = tk.Canvas(frame)
		canvas.config(width=tkImage.width(), height=tkImage.height())	# To do - Add scrolling instead of forcing size
		print("width", tkImage.width(), "height", tkImage.height() )
		canvas.create_image(0, 0, image=tkImage, anchor=tk.NW)				 			# 0,0 is the relative coordinates of the image
		canvas.pack(fill=tk.BOTH)




if __name__ == '__main__':
	ipa = IPA()
	ipa.go()			# This call doesn't return until the application terminates