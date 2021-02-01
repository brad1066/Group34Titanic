from tkinter import *

APPDATA = {}


class TitanicTk(Tk):
	def __init__(self, *args, **kwargs):
		Tk.__init__(self, *args, **kwargs)
		self.option_readfile("style.db")
		self.container = Frame(self)
		self.container.grid_rowconfigure(0, weight=1)
		self.container.grid_columnconfigure(0, weight=1)
		self.container.pack(side=TOP, fill=BOTH, expand=True)
		
		self.frames = {}
		
		self.geometry("430x640")
	
	def loadFrame(self, frame):
		if frame.__name__ not in self.frames.keys():
			self.frames[frame.__name__] = frame(self.container)
			self.frames[frame.__name__].grid(row=0, column=0)
		self.frames[frame.__name__].tkraise()


class WelcomeFrame(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent)
	
	def tkraise(self, aboveThis=None):
		Frame.tkraise(self, aboveThis)
		APPDATA["WINDOW"].title(f"Titanic Survivors Predictor - Welcome")


class PredictionsLoadFrame(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent)
	
	def tkraise(self, aboveThis=None):
		Frame.tkraise(self, aboveThis)
		APPDATA["WINDOW"].title(f"Titanic Survivors Predictor - Make Predictions")


class PredictionPreviewFrame(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent)
	
	def tkraise(self, aboveThis=None):
		Frame.tkraise(self, aboveThis)
		APPDATA["WINDOW"].title(f"Titanic Survivors Predictor - Preview Predictions")


class PredictionDetailsFrame(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent)
	
	def tkraise(self, aboveThis=None):
		Frame.tkraise(self, aboveThis)
		APPDATA["WINDOW"].title(f"Titanic Survivors Predictor - Prediction Details")


if __name__ == '__main__':
	app = APPDATA["WINDOW"] = TitanicTk()
	app.loadFrame(WelcomeFrame)
	app.mainloop()
