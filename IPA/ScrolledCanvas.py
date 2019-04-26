# This file implements the ScrolledCanvas class, which is a subclass of the Tkinter Canvas object; adding 
# the capability to automatically display working scrollbars if the canvas "virtual size" is larger
# than its' display size.
#
# author:   Adapted from example code in "Learning Python, 4th ed." by Mark Lutz
import tkinter as tk
from tkinter import ttk

class ScrolledCanvas(tk.Canvas):
    """
    Make a specialized tkinter canvas object that automatically makes scroll bars for itself.
    """
    def __init__(self, container):
        tk.Canvas.__init__(self, container)
        self.config(borderwidth=0)
        vScroll = tk.Scrollbar(container)
        hScroll = tk.Scrollbar(container, orient='horizontal')

        vScroll.pack(side=tk.RIGHT,  fill=tk.Y)                 
        hScroll.pack(side=tk.BOTTOM, fill=tk.X)                 
        self.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)

        # Hook the canvas and scrollbars together functionally... The tkinter
        # model has both the scrollbar and the canvas hooking into each other
        # for event handling to make the scrollbars work properly
        vScroll.config(command=self.yview)
        hScroll.config(command=self.xview)
        self.config(yscrollcommand=vScroll.set)
        self.config(xscrollcommand=hScroll.set)

