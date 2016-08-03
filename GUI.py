## Always start by initializing Qt (only once per application)
app = QtGui.QApplication([])

## Define a top-level widget to hold everything
win = QtGui.QWidget()
win.setWindowTitle('PY452 Data Logger')

## Create some widgets to be placed inside
btnStart = QtGui.QPushButton('Record Continuous')
btnSingleMeasurement = QtGui.QPushButton('Record Single Measurement')
btnStop = QtGui.QPushButton('Stop')
btnPause = QtGui.QPushButton('Pause!')
text = QtGui.QLineEdit(filename)
textSetV = QtGui.QLineEdit(str(outputV))
btnSecret = QtGui.QPushButton('Secret Signal!')
pw1 = pg.PlotWidget()
pw2 = pg.PlotWidget()
space = QtGui.QSpacerItem(1,1)

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

layout.setRowStretch(3,1)
layout.setRowStretch(2,1)
layout.setRowStretch(1,1)
layout.setRowStretch(0,1)

## Add widgets to the layout in their proper positions
layout.addWidget(pw1, 0, 0, 1, 3)  # plot goes on right side, spanning 4 rows
layout.addWidget(pw2, 0, 3, 1, 3)  # plot goes on right side, spanning 4 rows

layout.addWidget(text, 1, 0, 1, 3)   # text edit goes in top-left
layout.addWidget(btnStart, 2, 0, 1, 1)   # button goes in middle-left
layout.addWidget(btnStop, 2, 1, 1, 1)   # button goes in bottom-left
layout.addWidget(btnPause, 2, 2, 1, 1)  
layout.addWidget(btnSingleMeasurement, 3, 0, 1, 3)  
layout.addWidget(textSetV, 4, 0, 1, 1) 
layout.addWidget(btnSecret, 4, 1, 1, 1) 
layout.addWidget(c, 1, 3, 4, 3)

## Add events to the buttons
def handleButtonStart():
    startButton()
    btnStart.setStyleSheet("background-color: green")
def handleButtonStop():
    stopButton()
    btnStart.setStyleSheet("background-color: none")
def changeFilename(text):
    global filename
    filename = str(text)
def setVoltage():
    global outputV
    outputV = int(textSetV.text())
    cr.request('!ao ' + str(outputV))
def handleButtonPause():
    pauseButton()
    if paused:
        btnPause.setStyleSheet("background-color: red")
    else:
        btnPause.setStyleSheet("background-color: none")
def handleButtonSingleMeasurement():
    btnSingleMeasurement.setStyleSheet("background-color: green")
    singlemeausurementButton()
    btnSingleMeasurement.setStyleSheet("background-color: none")
def handleButtonSecret():
    secretButton()
    if paused:
        btnSecret.setStyleSheet("background-color: green")
    else:
        btnSecret.setStyleSheet("background-color: none")

    
btnStart.clicked.connect(handleButtonStart)
btnStop.clicked.connect(handleButtonStop)
btnPause.clicked.connect(handleButtonPause)
text.textChanged.connect(changeFilename)
textSetV.editingFinished.connect(setVoltage)
btnSingleMeasurement.clicked.connect(handleButtonSingleMeasurement)
btnSecret.clicked.connect(handleButtonSecret)

## Display the widget as a new window
win.show()

## Start the Qt event loop
##app.exec_()
