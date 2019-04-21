import tkinter as tk
from tkinter import ttk

class ScrolledCanvas(tk.Canvas):
    """
    A tkinter canvas object that automatically makes scroll bars for itself
    """
    def __init__(self, container):
        tk.Canvas.__init__(self, container)
        self.config(borderwidth=0)
        vbar = tk.Scrollbar(container)
        hbar = tk.Scrollbar(container, orient='horizontal')

        vbar.pack(side=tk.RIGHT,  fill=tk.Y)                 
        hbar.pack(side=tk.BOTTOM, fill=tk.X)                 
        self.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)

        # The tkinter model has both the scrollbar and the canvas hooking into each other for event handling to make
        # the scrollbars work properly
        vbar.config(command=self.yview)
        hbar.config(command=self.xview)
        self.config(yscrollcommand=vbar.set)
        self.config(xscrollcommand=hbar.set)

