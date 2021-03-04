import tkinter as tk
from tkinter import ttk


class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self)
        yScrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        xScrollbar = ttk.Scrollbar(self, orient="horizontal", command=canvas.xview)
        self.body = ttk.Frame(canvas)

        self.body.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.body, anchor=tk.NW)

        canvas.configure(yscrollcommand=yScrollbar.set)
        canvas.configure(xscrollcommand=xScrollbar.set)

        yScrollbar.pack(side="right", fill="y")
        xScrollbar.pack(side="bottom", fill="x")
        canvas.pack(side="top", fill="both", expand=True)