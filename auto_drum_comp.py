import sys 
from PyQt4 import QtGui, QtCore
import composer as cp

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Window(QtGui.QMainWindow):

	kickPlacement = True
	snarePlacement = True
	hatPlacement = True
	percPlacement = True
	gSnarePlacement = True

	def __init__(self):
		#Create main window
		super(Window, self).__init__()
		self.setGeometry(50, 50, 800, 700)
		self.setWindowTitle("Automatic Drum Composer")
		self.setWindowIcon(QtGui.QIcon('UI/drumkit_icon_small.png'))
		#self.general()

		QtGui.QApplication.setStyle("Cleanlooks")

		#Create grid layout
		self.centralwidget = QtGui.QWidget(self)
		self.centralwidget.setObjectName(_fromUtf8("centralwidget"))

		self.gridLayoutWidget = QtGui.QWidget(self.centralwidget)
		self.gridLayoutWidget.setGeometry(QtCore.QRect(0, -1, 800, 600))
		self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
		self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
		self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
		self.gridLayout_2 = QtGui.QGridLayout()
		self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
		self.setCentralWidget(self.centralwidget)

		#self.horizontalLayout_1 = QtGui.QHBoxLayout()
		#self.horizontalLayout_1.setObjectName(_fromUtf8("horizontalLayout_1"))
		#self.gridLayout.addLayout(self.horizontalLayout_1, 6, 0, 1, 1) 

		#Check box layouts
		self.verticalLayout_1 = QtGui.QVBoxLayout()
		self.verticalLayout_1.setObjectName(_fromUtf8("verticalLayout_1"))   
		self.gridLayout_2.addLayout(self.verticalLayout_1, 1, 0, 1, 1)

		self.gridLayout.addLayout(self.gridLayout_2, 0, 0, 1, 1)

		self.verticalLayout_2 = QtGui.QVBoxLayout()
		self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
		self.gridLayout.addLayout(self.verticalLayout_2, 1, 0, 1, 1)

		self.verticalLayout_3 = QtGui.QVBoxLayout()
		self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
		self.gridLayout.addLayout(self.verticalLayout_3, 3, 0, 1, 1)       

		self.verticalLayout_4 = QtGui.QVBoxLayout()
		self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4")) 
		self.gridLayout.addLayout(self.verticalLayout_4, 4, 0, 1, 1) 

		self.verticalLayout_5 = QtGui.QVBoxLayout()
		self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))        
		self.gridLayout.addLayout(self.verticalLayout_5, 5, 0, 1, 1) 

		#Check boxes and sliders
		self.kickBox1 = QtGui.QCheckBox(self.gridLayoutWidget)
		self.kickBox1.setObjectName(_fromUtf8("kickBox1"))
		self.verticalLayout_1.addWidget(self.kickBox1)
		self.kickBox1.stateChanged.connect(self.kick_placement)
		self.kickBox1.toggle()

		self.kickMinSlider = QtGui.QSlider(self.gridLayoutWidget)
		self.kickMinSlider.setOrientation(QtCore.Qt.Horizontal)
		self.kickMinSlider.setObjectName(_fromUtf8("kickMinSlider"))
		self.verticalLayout_1.addWidget(self.kickMinSlider)

		self.kickMaxSlider = QtGui.QSlider(self.gridLayoutWidget)
		self.kickMaxSlider.setOrientation(QtCore.Qt.Horizontal)
		self.kickMaxSlider.setObjectName(_fromUtf8("kickMaxSlider"))
		self.verticalLayout_1.addWidget(self.kickMaxSlider)

		self.kickConvSlider = QtGui.QSlider(self.gridLayoutWidget)
		self.kickConvSlider.setOrientation(QtCore.Qt.Horizontal)
		self.kickConvSlider.setObjectName(_fromUtf8("kickConvSlider"))
		self.verticalLayout_1.addWidget(self.kickConvSlider)

		self.snareBox1 = QtGui.QCheckBox(self.gridLayoutWidget)
		self.snareBox1.setObjectName(_fromUtf8("snareBox1"))
		self.verticalLayout_2.addWidget(self.snareBox1)
		self.snareBox1.stateChanged.connect(self.snare_placement)
		self.snareBox1.toggle()

		self.snareMinSlider = QtGui.QSlider(self.gridLayoutWidget)
		self.snareMinSlider.setOrientation(QtCore.Qt.Horizontal)
		self.snareMinSlider.setObjectName(_fromUtf8("snareMinSlider"))
		self.verticalLayout_2.addWidget(self.snareMinSlider)

		self.snareMaxSlider = QtGui.QSlider(self.gridLayoutWidget)
		self.snareMaxSlider.setOrientation(QtCore.Qt.Horizontal)
		self.snareMaxSlider.setObjectName(_fromUtf8("snareMaxSlider"))
		self.verticalLayout_2.addWidget(self.snareMaxSlider)

		self.snareConvSlider = QtGui.QSlider(self.gridLayoutWidget)
		self.snareConvSlider.setOrientation(QtCore.Qt.Horizontal)
		self.snareConvSlider.setObjectName(_fromUtf8("snareConvSlider"))
		self.verticalLayout_2.addWidget(self.snareConvSlider) 

		self.hatBox1 = QtGui.QCheckBox(self.gridLayoutWidget)
		self.hatBox1.setObjectName(_fromUtf8("hatBox1"))
		self.verticalLayout_3.addWidget(self.hatBox1)
		self.hatBox1.stateChanged.connect(self.hat_placement)
		self.hatBox1.toggle()		

		self.hatMinSlider = QtGui.QSlider(self.gridLayoutWidget)
		self.hatMinSlider.setOrientation(QtCore.Qt.Horizontal)
		self.hatMinSlider.setObjectName(_fromUtf8("hatMinSlider"))
		self.verticalLayout_3.addWidget(self.hatMinSlider)

		self.hatMaxSlider = QtGui.QSlider(self.gridLayoutWidget)
		self.hatMaxSlider.setOrientation(QtCore.Qt.Horizontal)
		self.hatMaxSlider.setObjectName(_fromUtf8("hatMaxSlider"))
		self.verticalLayout_3.addWidget(self.hatMaxSlider)

		self.hatConvSlider = QtGui.QSlider(self.gridLayoutWidget)
		self.hatConvSlider.setOrientation(QtCore.Qt.Horizontal)
		self.hatConvSlider.setObjectName(_fromUtf8("hatConvSlider"))
		self.verticalLayout_3.addWidget(self.hatConvSlider)               

		self.percBox1 = QtGui.QCheckBox(self.gridLayoutWidget)
		self.percBox1.setObjectName(_fromUtf8("percBox1"))
		self.verticalLayout_4.addWidget(self.percBox1)
		self.percBox1.stateChanged.connect(self.perc_placement)
		self.percBox1.toggle()		

		self.percMinSlider = QtGui.QSlider(self.gridLayoutWidget)
		self.percMinSlider.setOrientation(QtCore.Qt.Horizontal)
		self.percMinSlider.setObjectName(_fromUtf8("percMinSlider"))
		self.verticalLayout_4.addWidget(self.percMinSlider)

		self.percMaxSlider = QtGui.QSlider(self.gridLayoutWidget)
		self.percMaxSlider.setOrientation(QtCore.Qt.Horizontal)
		self.percMaxSlider.setObjectName(_fromUtf8("percMaxSlider"))
		self.verticalLayout_4.addWidget(self.percMaxSlider)

		self.percConvSlider = QtGui.QSlider(self.gridLayoutWidget)
		self.percConvSlider.setOrientation(QtCore.Qt.Horizontal)
		self.percConvSlider.setObjectName(_fromUtf8("percConvSlider"))
		self.verticalLayout_4.addWidget(self.percConvSlider)

		self.gSnareBox1 = QtGui.QCheckBox(self.gridLayoutWidget)
		self.gSnareBox1.setObjectName(_fromUtf8("gSnareBox1"))
		self.verticalLayout_5.addWidget(self.gSnareBox1)
		self.gSnareBox1.stateChanged.connect(self.g_snare_placement)
		self.gSnareBox1.toggle()		

		self.gSnareMinSlider = QtGui.QSlider(self.gridLayoutWidget)
		self.gSnareMinSlider.setOrientation(QtCore.Qt.Horizontal)
		self.gSnareMinSlider.setObjectName(_fromUtf8("gSnareMinSlider"))
		self.verticalLayout_5.addWidget(self.gSnareMinSlider)

		self.gSnareMaxSlider = QtGui.QSlider(self.gridLayoutWidget)
		self.gSnareMaxSlider.setOrientation(QtCore.Qt.Horizontal)
		self.gSnareMaxSlider.setObjectName(_fromUtf8("gSnareMaxSlider"))
		self.verticalLayout_5.addWidget(self.gSnareMaxSlider)

		self.gSnareConvSlider = QtGui.QSlider(self.gridLayoutWidget)
		self.gSnareConvSlider.setOrientation(QtCore.Qt.Horizontal)
		self.gSnareConvSlider.setObjectName(_fromUtf8("gSnareConvSlider"))
		self.verticalLayout_5.addWidget(self.gSnareConvSlider)       

        #Generate button
		self.genBtn = QtGui.QPushButton(self.gridLayoutWidget)
		self.genBtn.setObjectName(_fromUtf8("pushButton"))
		self.gridLayout.addWidget(self.genBtn, 7, 0, 1, 1)
		self.genBtn.clicked.connect(self.generate)
		#self.genBtn.resize(self.genBtn.sizeHint())

		#Main menu options
		quitAction = QtGui.QAction("&Quit", self)
		quitAction.setShortcut("Ctrl+Q")
		quitAction.setStatusTip("Leave The App")
		quitAction.triggered.connect(self.exit)

		#Create main menu
		self.statusBar()

		mainMenu = self.menuBar()
		fileMenu = mainMenu.addMenu("&File")
		fileMenu.addAction(quitAction)

		self.retranslateUi(Window)
		#QtCore.QMetaObject.connectSlotsByName(Window)

	def retranslateUi(self, Window):
		self.gSnareBox1.setText(_translate("Window", "Ghost Snare", None))
		self.percBox1.setText(_translate("Window", "Percussion", None))
		self.kickBox1.setText(_translate("Window", "Kick", None))
		self.hatBox1.setText(_translate("Window", "Hi-Hat", None))
		self.snareBox1.setText(_translate("Window", "Snare", None))
		
	def kick_placement(self, state):
		if state == QtCore.Qt.Checked:
			self.kickPlacement = True
		else:
			self.kickPlacement = False

	def snare_placement(self, state):
		if state == QtCore.Qt.Checked:
			self.snarePlacement = True
		else:
			self.snarePlacement = False

	def hat_placement(self, state):
		if state == QtCore.Qt.Checked:
			self.hatPlacement = True
		else:
			self.hatPlacement = False

	def perc_placement(self, state):
		if state == QtCore.Qt.Checked:
			self.percPlacement = True
		else:
			self.percPlacement = False

	def g_snare_placement(self, state):
		if state == QtCore.Qt.Checked:
			self.gSnarePlacement = True
		else:
			self.gSnarePlacement = False


	def generate(self):
		constraints = [ [self.kickPlacement, True, True], \
		                [False, self.snarePlacement], \
		                [True], \
		                [False, self.hatPlacement, True, True], \
		                [self.percPlacement, True, True], \
		                [self.gSnarePlacement, True, True] ]

		#Patterns will be filled out around any user input given to the program.
		#user_input = ["chooseHit(k, 3).", "chooseHit(s, 5).", "chooseHit(s, 13)."]

		cp.generate_patterns(constraints, 1, 2, 0.01)
		#sys.exit()

	def exit(self):
		choice = QtGui.QMessageBox.question(self, "Exit",
											"Are you sure you want to exit the program?", 
											QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
		if choice == QtGui.QMessageBox.Yes:
			sys.exit()
		else:
			pass


def main():

	app = QtGui.QApplication(sys.argv)
	GUI = Window()
	GUI.show()
	sys.exit(app.exec_())

main()	
