#!/usr/bin/env python3

# based from example tkinter code in "Programming Python, 4ed" by Mark Lutz

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

imgdir = "/Users/tim/Pictures/"
filename1 = 'Evelyn Smashed.jpg'
filename2 = 'Evelyn Smashed.gif'


class IPA(ttk.Frame):
	"""This is the main program class of IPA: Image Processing Application"""
	def __init__(self, parent=None, **options):
		ttk.Frame.__init__(self, parent=None, **options)
		self.pack()
		self.master.title("IPA: Image Processing Application")

		self.img1 = Image.open(imgdir + filename1)
		self.photoimg1 = ImageTk.PhotoImage(self.img1)

		self.img2 = Image.open(imgdir + filename2)
		self.photoimg2 = ImageTk.PhotoImage(self.img2)
		
		self.nb = ttk.Notebook(self, padding=0)
		self.frame1 = ttk.Frame(self.nb)
		self.frame2 = ttk.Frame(self.nb)
		self.nb.add(self.frame1, text='Image 1')
		self.nb.add(self.frame2, text='Image 2')
		self.nb.pack()

		self.can = tk.Canvas(self.frame1)
		self.can.config(width=self.photoimg1.width(), height=self.photoimg1.height())
		self.can.create_image(2, 2, image=self.photoimg1, anchor=tk.NW)
		self.can.pack(fill=tk.BOTH)

		self.can = tk.Canvas(self.frame2)
		self.can.config(width=self.photoimg2.width(), height=self.photoimg2.height())
		self.can.create_image(2, 2, image=self.photoimg2, anchor=tk.NW)
		self.can.pack(fill=tk.BOTH)


		ttk.Button(self, text="Close").pack(side=tk.RIGHT)
		ttk.Button(self, text="Save...").pack(side=tk.RIGHT)
		ttk.Button(self, text='Open...').pack(side=tk.RIGHT)


if __name__ == '__main__':
	IPA().mainloop()