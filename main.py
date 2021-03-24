# A library for making UIs in python (a tcl wrapper)
from tkinter import *
from tkinter import filedialog as fd, messagebox as mb

# A library used for managing data as if they were in tables
import pandas as pd
# An image library to allow tkinter to use images easier
from PIL import ImageTk, Image
# A series of imports used for machine learning
from sklearn.ensemble import RandomForestClassifier

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# A variable defined at the top of the program to allow all classes and functions access to some shared data and variables
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
        APPDATA["CURRENT_FRAME"] = frame.__name__


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

        # Create an image object and assign it to the background of a Label, which will be used as a container to hold a
        # graphic to the right of the Welcome page
        self.bgImg = ImageTk.PhotoImage(Image.open("images/code_brain.png"))
        Label(self, image=self.bgImg).grid(
            row=0, column=1, rowspan=5, sticky=NSEW)

        # Create a range of Labels (and a Frame as a separating block) as body content
        Label(self, text="Welcome", font=("Segoe UI", 48, "bold"),
              anchor=CENTER).grid(row=0, column=0, sticky=NSEW)
        Frame(self, bg="white", height=3).grid(
            row=1, column=0, sticky=EW, padx=40)
        Label(self, text="Titanic Survival Predictions", font=("Segoe UI", 22, "bold")).grid(row=2, column=0,
                                                                                             sticky=NSEW)
        Label(self, text="This tool uses Machine Learning techniques to predict who would survive a disaster " +
              "such as that of the Titanic.\n\nTo start, click the button below to train the predictive " +
              "model", anchor=CENTER, wraplength=340).grid(row=3, column=0, sticky=N + EW, pady=(30, 0))

        # Create a button that when pressed will start the model training and then load a PredictionsLoadFrame
        Button(self, text="Train the Model",
               command=lambda: APPDATA["WINDOW"].loadFrame(PredictionsLoadFrame)).grid(row=4, column=0,
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

        # Create an image object and assign it to the background of a Label, which will be used as a container to hold a
        # graphic to the right of the Welcome page
        self.bgImg = ImageTk.PhotoImage(Image.open("images/code_brain.png"))
        Label(self, image=self.bgImg).grid(
            row=0, column=1, rowspan=5, sticky=NSEW)

        # Create a range of Labels (and a Frame as a separating block) as body content
        Label(self, text="Trained", font=("Segoe UI", 48, "bold"),
              anchor=CENTER).grid(row=0, column=0, sticky=NSEW)
        Frame(self, bg="white", height=3).grid(
            row=1, column=0, sticky=EW, padx=40)
        Label(self, text="Time to make Predictions", font=(
            "Segoe UI", 22, "bold")).grid(row=2, column=0, sticky=NSEW)
        Label(self, text="Now that the model has been trained, it is time to make some predictions.\n\nClick the" +
              "button below to select the file containing the passenger data (making sure that it is in a " +
              "valid CSV Format)", anchor=CENTER, wraplength=340).grid(row=3, column=0, sticky=N + EW,
                                                                       pady=(30, 0))
        # Create a button that when pressed will make predictions and then load a PredictionViewFrame
        Button(self, text="Make Predictions",
               command=lambda: makePredictions(APPDATA["WINDOW"].loadFrame, PredictionViewFrame)).grid(row=4,
                                                                                                       column=0,
                                                                                                       sticky=NSEW,
                                                                                                       padx=10, pady=10)

    def tkraise(self, aboveThis=None):
        """An overridden method to add window title change functionality to the standard method"""
        # Raise this frame within it's container, then change the title of the MainWindow
        Frame.tkraise(self, aboveThis)
        APPDATA["WINDOW"].title(
            "Titanic Survivors Predictor - Make Predictions")


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
        #self.grid_columnconfigure(1, weight=1)

        # Create a range of Labels (and a Frame as a separating block) as body content
        Label(self, text="Trained", font=("Segoe UI", 48, "bold"),
              anchor=CENTER).grid(row=0, column=0, sticky=NSEW)
        Frame(self, bg="white", height=3).grid(
            row=1, column=0, sticky=EW, padx=40)
        Label(self, text="Here is your survival predictions:", font=(
            "Segoe UI", 22, "bold")).grid(row=2, column=0, sticky=NSEW)

        self.pieChartFrame = Frame(self)
        self.pieChartFrame.grid(row=3, column=0, sticky=NSEW)

        # This will hold the buttons that will be used to export and make new predictions
        self.buttonsFrame = Frame(self)
        self.buttonsFrame.grid_columnconfigure(0, weight=1)
        self.buttonsFrame.grid_columnconfigure(1, weight=1)
        self.buttonsFrame.grid(row=4, column=0, sticky=NSEW, padx=10, pady=10)

        # A button to allow the user to export the predictions in the format that Kaggle requires to a path that the user specifies
        Button(self.buttonsFrame, text="Export Data", command=exportData).grid(row=0, column=0,
                                                                               sticky=NSEW, padx=10,
                                                                               pady=10)

        # A button to allow the user to make a new prediction from a different file
        Button(self.buttonsFrame, text="Make new Predictions",
               command=lambda: APPDATA["WINDOW"].loadFrame(PredictionsLoadFrame)).grid(row=0, column=1,
                                                                                       sticky=NSEW,
                                                                                       padx=10,
                                                                                       pady=10)

        # Populate self.detailsFrame with the data provided from the selected data file and the predictions
        # self.populateDetails()

    def updatePieChart(self):
        self.pieChartFrame.grid_forget()
        self.pieChartFrame = Frame(self)
        self.pieChartFrame.grid(row=3, column=0, sticky=NSEW)
        pieLegends = ['Perished', 'Survived']
        pieVals = [len([_ for _ in APPDATA["predictions"] if _ == 0]), len(
            [_ for _ in APPDATA["predictions"] if _ == 1])]
        fig = Figure()  # create a figure object
        fig.clear()
        fig.patch.set_facecolor("black")
        ax = fig.add_subplot(111)  # add an Axes to the figure

        ax.pie(pieVals, radius=1, labels=pieLegends,
               autopct='%0.2f%%', shadow=False,colors=['red', 'green'])
        fig.legend(title="Survivor predictions")

        chart1 = FigureCanvasTkAgg(fig, self.pieChartFrame)
        chart1.get_tk_widget().children.clear()
        chart1.get_tk_widget().pack()

    def tkraise(self, aboveThis=None):
        """An overridden method to add window title change functionality to the standard method"""
        # Raise this frame within it's container, then change the title of the MainWindow
        Frame.tkraise(self, aboveThis)
        APPDATA["WINDOW"].title(
            "Titanic Survivors Predictor - Preview Predictions")


def makePredictions(callback=None, *args, **kwargs):
    """A function to run the data through the model and perform some passed in function"""
    # Clear the current predictionsFile value fom the APPDATA variable
    APPDATA["predictionsFile"] = None
    try:
        # Hide the main application window from view, and select a file to be read from to make predictions on, saving
        # the filepath in the APPDATA
        APPDATA["WINDOW"].withdraw()
        APPDATA["predictionsFile"] = fd.askopenfilename(title="Select data file", defaultextension=".csv",
                                                        filetypes=[("CSV", "*.csv")])

        # If the user selected a file, then clean the data in the file up ready for the predictions
        if APPDATA["predictionsFile"]:
            try:
                APPDATA["predictionData"] = cleanData(
                    pd.read_csv(APPDATA["predictionsFile"]))
            except:
                print(
                    "There was an error in cleaning prediction data. This may cause issues later on")

            try:
                y_train = APPDATA["trainData"]['Survived']
                x_train = APPDATA["trainData"].drop('Survived', axis=1)
                x_pred = APPDATA["predictionData"]

                rf = RandomForestClassifier()

            except:
                print("There was an error when applying Random")

            rf.fit(x_train, y_train)
            APPDATA["predictions"] = rf.predict(x_pred)

            callback(*args, **kwargs)
            APPDATA["WINDOW"].frames["PredictionViewFrame"].updatePieChart()
        else:
            if mb.askyesno("No file selected",
                           "No file was selected to make predictions from. Would you like to try again?"):
                return makePredictions(callback, *args, **kwargs)
            else:
                mb.showinfo("No file selected",
                            "No file was selected, so no predictions were made.")
    except TypeError as e:
        print(e)
    APPDATA["WINDOW"].update()
    APPDATA["WINDOW"].deiconify()


def exportData(callback=None, *args, **kwargs):
    """A function to export the currently stored prediction data"""
    try:
        # Use tkinter dialog to get an export file path
        export_file_name = fd.asksaveasfilename(title="Export Predictions", defaultextension=".csv",
                                                filetypes=[("CSV", "*.csv")])
        # If the user didn't cancel the dialog, then use pandas to put together the dataframe to export to CSV, and export it;
        if export_file_name:
            submission = pd.DataFrame(
                {'PassengerId': APPDATA["predictionData"]['PassengerId'], 'Survived': APPDATA["predictions"]})
            submission.to_csv(export_file_name, index=False)
        else:
            # If the user cancelled the export dialog, then check to see if they want to try again.
            # If they say Yes, then repeat the export function with the given traceback and args and kwargs
            if mb.askyesno("No file selected",
                           "No file was selected to export data to. Would you like to try again?"):
                return exportData(callback, *args, **kwargs)
            else:
                # If the user did want to cancel the export process, then notify them that the data wasn't exported
                mb.showinfo(
                    "No file selected", "No file was selected, so the predictions were not exported.")

        # Try to run the callback function that is passed in
        callback(*args, **kwargs)

    # If the user provided no valid callback, then this stops errors being found
    except TypeError:
        pass

    # If there were any other errors, then notify the user that there may have been an issue with exporting the data.
    except Exception as e:
        # Log the error on the console, then show an error message.
        print(f"An error was found: {e}")
        mb.showerror("An error occurred",
                     "There was an error while exporting the data. You may need to try again")


def cleanData(data):
    """A function to take some data, clean it up (removing certain fields and filling gaps, then return it"""

    # TODO: Do the data cleaning necessary (as written by ML team)
    # Remove the Cabin field from the data (as we found that there was too much data missing to be fillable
    data.drop('Cabin', axis=1, inplace=True)

    # Impute the age of the passengers in the data set
    data.loc[(data['Age'].isna()) & (data['Pclass'] == 1), 'Age'] = \
        data.groupby('Pclass')['Age'].mean()[1]
    data.loc[(data['Age'].isna()) & (data['Pclass'] == 2), 'Age'] = \
        data.groupby('Pclass')['Age'].mean()[2]
    data.loc[(data['Age'].isna()) & (data['Pclass'] == 3), 'Age'] = \
        data.groupby('Pclass')['Age'].mean()[3]

    # Filling the missing fare values with the price that occurs most frequently
    data['Fare'].fillna(data['Fare'].mode()[0], inplace=True)

    # Filling the missing values for Embarked with the most common port
    data['Embarked'].fillna(data['Embarked'].mode()[0], inplace=True)

    # Feature Engineering
    pd.get_dummies(data['Embarked'], drop_first=True).head()
    sex = pd.get_dummies(data['Sex'], drop_first=True)
    embark = pd.get_dummies(data['Embarked'], drop_first=True)
    data.drop(['Name', 'Sex', 'Ticket', 'Embarked'], axis=1, inplace=True)
    data = pd.concat([data, sex, embark], axis=1)
    return data


# If this file is being ran as a program and not imported
if __name__ == '__main__':
    from os import getcwd as cwd
    # Set the trainData APPDATA variable to be the cleaned result of the training data
    APPDATA["trainData"] = cleanData(pd.read_csv(f"{cwd()}\\train.csv"))
    # Create a TitanicTk object, store it inside of the APPDATA dictionary and locally as app
    app = APPDATA["WINDOW"] = TitanicTk()
    # Load the welcome frame and then start the UI loop (so it doesn't terminate when all other foreground functions
    # are completed
    app.loadFrame(WelcomeFrame)
    app.mainloop()
