import tkinter as tk
from tkinter import ttk


class ScrolledCanvas(tk.Canvas):
    """
    a canvas in a container that automatically makes
    vertical and horizontal scroll bars for itself

    This class is adapted from example code in “Programming Python , Fourth Edition", by Mark Lutz
	(O’Reilly). Copyright 2011 Mark Lutz, 978-0-596-15810-1.
    """
    def __init__(self, container):
        tk.Canvas.__init__(self, container)
        self.config(borderwidth=0)
        vbar = tk.Scrollbar(container)
        hbar = tk.Scrollbar(container, orient='horizontal')

        vbar.pack(side=tk.RIGHT,  fill=tk.Y)                 # pack canvas after bars
        hbar.pack(side=tk.BOTTOM, fill=tk.X)                 # so clipped first
        self.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)

        vbar.config(command=self.yview)                # call on scroll move
        hbar.config(command=self.xview)
        self.config(yscrollcommand=vbar.set)           # call on canvas move
        self.config(xscrollcommand=hbar.set)

