## Always start by initializing Qt (only once per application)
app = QtGui.QApplication([])

## Define a top-level widget to hold everything
win = QtGui.QWidget()
win.setWindowTitle('PY452 Data Logger')

## Create some widgets to be placed inside
btnStart = QtGui.QPushButton('Record!')
btnStop = QtGui.QPushButton('Stop!')
text = QtGui.QLineEdit(filename)
pw = pg.PlotWidget()

## initial text to display in the console
namespace = {'pg': pg, 'np': np}
ctext = """
This is an interactive python console. The numpy and pyqtgraph modules have already been imported 
as 'np' and 'pg'. 

Go, play.
"""
c = pyqtgraph.console.ConsoleWidget(namespace=namespace, text=ctext)
#c.show()
#c.setWindowTitle('pyqtgraph example: ConsoleWidget')

## Create a grid layout to manage the widgets size and position
layout = QtGui.QGridLayout()
win.setLayout(layout)

## Add widgets to the layout in their proper positions
layout.addWidget(text, 0, 0)   # text edit goes in top-left
layout.addWidget(btnStart, 1, 0)   # button goes in middle-left
layout.addWidget(btnStop, 2, 0)   # button goes in bottom-left
layout.addWidget(pw, 0, 1, 4, 1)  # plot goes on right side, spanning 4 rows
layout.addWidget(c, 5, 0, 1, 0)

## Add events to the buttons
def handleButtonStart():
    startButton()
def handleButtonStop():
    stopButton()
def changeFilename(text):
    global filename
    filename = str(text)

btnStart.clicked.connect(handleButtonStart)
btnStop.clicked.connect(handleButtonStop)
text.textChanged.connect(changeFilename)

## Display the widget as a new window
win.show()

## Start the Qt event loop
##app.exec_()
