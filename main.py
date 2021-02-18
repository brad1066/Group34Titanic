from tkinter import *

from PIL import ImageTk, Image

APPDATA = {}


class TitanicTk(Tk):
	"""A class to hold the window data and the UI frames"""
	
	def __init__(self, *args, **kwargs):
		"""The constructor for the TitanicTk Class"""
		# Initialise the object as a Tk, add style options from a file
		Tk.__init__(self, *args, **kwargs)
		self.option_readfile("style.db")
		
		# Create the container for the content frames and configure it's layout. Fill the window with the container
		self.container = Frame(self)
		self.container.grid_rowconfigure(0, weight=1)
		self.container.grid_columnconfigure(0, weight=1)
		self.container.pack(side=TOP, fill=BOTH, expand=True)
		
		# Create a dictionary to store generated content frames, to make them easily swappable
		self.frames = {}
		
		# Set the size of the window, and make it not resizable
		self.geometry("930x640")
		self.resizable(0, 0)
	
	def loadFrame(self, frame):
		"""A method to allow the creation and/or loading of stored frames based on the name of the frame"""
		
		# If the frame has not been loaded in before...
		if frame.__name__ not in self.frames.keys():
			# Create the frame, store it using the name of it's class, and place it into the layout
			self.frames[frame.__name__] = frame(self.container)
			self.frames[frame.__name__].grid(row=0, column=0, sticky=NSEW)
		
		# Bring the frame to the forefront of the window
		self.frames[frame.__name__].tkraise()


class WelcomeFrame(Frame):
	"""A content container class for the Welcome page"""
	
	def __init__(self, parent):
		"""The constructor for the WelcomeFrame class"""
		# Initialise the object as a Frame and configure the layout manager
		Frame.__init__(self, parent)
		self.grid_rowconfigure(0, weight=4)
		self.grid_rowconfigure(1, weight=0)
		self.grid_rowconfigure(2, weight=2)
		self.grid_rowconfigure(3, weight=5)
		self.grid_rowconfigure(4, weight=2)
		self.grid_columnconfigure(0, weight=1)
		self.grid_columnconfigure(1, weight=1)
		
		self.bgImg = ImageTk.PhotoImage(Image.open("images/code_brain.png"))
		Label(self, image=self.bgImg).grid(row=0, column=1, rowspan=5, sticky=NSEW)
		
		# Create a range of Labels (and a Frame as a separating block) as body content
		Label(self, text="Welcome", font=("Segoe UI", 48, "bold"), anchor=CENTER).grid(row=0, column=0, sticky=NSEW)
		Frame(self, bg="white", height=3).grid(row=1, column=0, sticky=EW, padx=40)
		Label(self, text="Titanic Survival Predictions", font=("Segoe UI", 22, "bold")).grid(row=2, column=0,
																							 sticky=NSEW)
		Label(self, text="This tool uses Machine Learning techniques to predict who would survive a disaster " +
						 "such as that of the Titanic.\n\nTo start, click the button below to train the predictive " +
						 "model", anchor=CENTER, wraplength=340).grid(row=3, column=0, sticky=N + EW, pady=(30, 0))
		
		# Create a button that when pressed will start the model training and then load a PredictionsLoadFrame
		Button(self, text="Train the Model",
			   command=lambda: trainModel(APPDATA["WINDOW"].loadFrame(PredictionsLoadFrame))).grid(row=4, column=0,
																								   sticky=NSEW,
																								   padx=10, pady=10)
	
	def tkraise(self, aboveThis=None):
		"""An overridden method to add window title change functionality to the standard method"""
		# Raise this frame within it's container, then change the title of the MainWindow
		Frame.tkraise(self, aboveThis)
		APPDATA["WINDOW"].title("Titanic Survivors Predictor - Welcome")


class PredictionsLoadFrame(Frame):
	"""A content container class for the Predictions Loaded page"""
	
	def __init__(self, parent):
		"""The constructor for the PredictionsLoadFrame class"""
		# Initialise the object as a Frame and configure the layout manager
		Frame.__init__(self, parent)
		self.grid_rowconfigure(0, weight=4)
		self.grid_rowconfigure(1, weight=0)
		self.grid_rowconfigure(2, weight=2)
		self.grid_rowconfigure(3, weight=5)
		self.grid_rowconfigure(4, weight=2)
		self.grid_columnconfigure(0, weight=1)
		self.grid_columnconfigure(1, weight=1)
		
		self.bgImg = ImageTk.PhotoImage(Image.open("images/code_brain.png"))
		Label(self, image=self.bgImg).grid(row=0, column=1, rowspan=5, sticky=NSEW)
		
		# Create a range of Labels (and a Frame as a separating block) as body content
		Label(self, text="Trained", font=("Segoe UI", 48, "bold"), anchor=CENTER).grid(row=0, column=0, sticky=NSEW)
		Frame(self, bg="white", height=3).grid(row=1, column=0, sticky=EW, padx=40)
		Label(self, text="Time to make Predictions", font=("Segoe UI", 22, "bold")).grid(row=2, column=0, sticky=NSEW)
		Label(self, text="Now that the model has been trained, it is time to make some predictions.\n\nClick the" +
						 "button below to select the file containing the passenger data (making sure that it is in a " +
						 "valid CSV Format)", anchor=CENTER, wraplength=340).grid(row=3, column=0, sticky=N + EW,
																				  pady=(30, 0))
		# Create a button that when pressed will make predictions and then load a PredictionViewFrame
		Button(self, text="Make Predictions",
			   command=lambda: makePredictions(APPDATA["WINDOW"].loadFrame(PredictionViewFrame))).grid(row=4,
																									   column=0,
																									   sticky=NSEW,
																									   padx=10, pady=10)
	
	def tkraise(self, aboveThis=None):
		"""An overridden method to add window title change functionality to the standard method"""
		# Raise this frame within it's container, then change the title of the MainWindow
		Frame.tkraise(self, aboveThis)
		APPDATA["WINDOW"].title("Titanic Survivors Predictor - Make Predictions")


class PredictionViewFrame(Frame):
	"""A content container class for the Predictions View page"""
	
	def __init__(self, parent):
		"""The constructor for the PredictionViewFrame class"""
		# Initialise the object as a Frame and configure the layout manager
		Frame.__init__(self, parent)
		self.grid_rowconfigure(0, weight=4)
		self.grid_rowconfigure(1, weight=0)
		self.grid_rowconfigure(2, weight=2)
		self.grid_rowconfigure(3, weight=5)
		self.grid_rowconfigure(4, weight=2)
		self.grid_columnconfigure(0, weight=1)
		self.grid_columnconfigure(1, weight=1)
		
		# Create a range of Labels (and a Frame as a separating block) as body content
		Label(self, text="Trained", font=("Segoe UI", 48, "bold"), anchor=CENTER).grid(row=0, column=0, sticky=NSEW)
		Frame(self, bg="white", height=3).grid(row=1, column=0, sticky=EW, padx=40)
		Label(self, text="Here are your predictions:", font=("Segoe UI", 22, "bold")).grid(row=2, column=0, sticky=NSEW)
		
		self.detailsFrame = Frame(self, bg="red", width=330)
		self.detailsFrame.grid(row=0, column=1, rowspan=4, sticky=NSEW, ipadx=10, ipady=20)
		
		Button(self, text="Export Data").grid(row=4, column=0, sticky=NSEW, padx=10, pady=10)
		Button(self, text="Make new Predictions",
			   command=lambda: makePredictions(APPDATA["WINDOW"].loadFrame(PredictionsLoadFrame))).grid(row=4, column=1,
																										sticky=NSEW,
																										padx=10,
																										pady=10)
	
	def populateDetails(self):
		# TODO: Clear the table from self.detailsFrame and repopulate with header and content labels in a grid
		pass
	
	def tkraise(self, aboveThis=None):
		"""An overridden method to add window title change functionality to the standard method"""
		# Raise this frame within it's container, then change the title of the MainWindow
		Frame.tkraise(self, aboveThis)
		APPDATA["WINDOW"].title("Titanic Survivors Predictor - Preview Predictions")


def trainModel(callback=None, *args, **kwargs):
	"""A function to train the model and perform some passed in function"""
	# TODO: model training code
	# Try to run the callback function that is passed in
	try:
		callback(*args, **kwargs)
	except:
		pass


def makePredictions(callback=None, *args, **kwargs):
	"""A function to run the data through the model and perform some passed in function"""
	# TODO: Do model training code
	# Try to run the callback function that is passed in
	try:
		callback(*args, **kwargs)
	except:
		pass


def exportData(callback=None, *args, **kwargs):
	"""A function to export the currently stored prediction data"""
	# TODO: Do exporting code
	# Try to run the callback function that is passed in
	try:
		callback(*args, **kwargs)
	except:
		pass


# If this file is being ran as a program and not imported
if __name__ == '__main__':
	# Create a TitanicTk object, store it inside of the APPDATA dictionary and locally as app
	app = APPDATA["WINDOW"] = TitanicTk()
	# Load the welcome frame and then start the UI loop (so it doesn't terminate when all other foreground functions
	# are completed
	app.loadFrame(WelcomeFrame)
	app.mainloop()
