import tkinter as tk
from tkinter import ttk

class ScrolledCanvas(tk.Canvas):
    """
    Make a specialized tkinter canvas object that automatically makes scroll bars for itself.  Concept
    adapted from "Learning Python, 4th ed." by Mark Lutz
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

