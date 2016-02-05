## Always start by initializing Qt (only once per application)
app = QtGui.QApplication([])

## Define a top-level widget to hold everything
win = QtGui.QWidget()
win.setWindowTitle('PY452 Data Logger')

## Create some widgets to be placed inside
btnStart = QtGui.QPushButton('Record!')
btnStop = QtGui.QPushButton('Stop!')
text = QtGui.QLineEdit('Datafile Name')
pw = pg.PlotWidget()

## Create a grid layout to manage the widgets size and position
layout = QtGui.QGridLayout()
win.setLayout(layout)

## Add widgets to the layout in their proper positions
layout.addWidget(text, 0, 0)   # text edit goes in top-left
layout.addWidget(btnStart, 1, 0)   # button goes in middle-left
layout.addWidget(btnStop, 2, 0)   # button goes in bottom-left
layout.addWidget(pw, 0, 1, 4, 1)  # plot goes on right side, spanning 3 rows

## Add events to the buttons
def handleButtonStart():
    global writeData
    writeData=True
    #print ('Hello World')
def handleButtonStop():
    global writeData
    writeData=False
    #print ('Goodbye World')
btnStart.clicked.connect(handleButtonStart)
btnStop.clicked.connect(handleButtonStop)

## Display the widget as a new window
win.show()

## Start the Qt event loop
##app.exec_()
