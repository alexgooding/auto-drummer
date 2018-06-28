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

class MainWindow(object):

	kickPlacement = True
	snarePlacement = True
	snareExpPlacement = False
	snareConvPlacement= True
	hatPlacement = True
	hatExpPlacement = False
	hatConvPlacement = True
	percPlacement = True
	gSnarePlacement = True

	kickCon1 = True
	kickCon2 = True
	kickSnareCon1 = True
	hatCon1 = True
	hatCon2 = True
	percCon1 = True
	percCon2 = True
	gSnareCon1 = True
	gSnareCon2 = True

	snareConvValue = 0
	hatConvValue = 0

	kickMin = 0
	kickMax = 3
	snareMin = 2
	snareMax = 3
	hatExpMin = 0
	hatExpMax = 16
	percMin = 0
	percMax = 1
	gSnareMin = 0
	gSnareMax = 3

	humanisationAmount = 0

	patternLength = 1

	numberOfPatterns = 1

	def setupUi(self, Window):
		#Create main window
		Window.setObjectName(_fromUtf8("Window"))
		Window.resize(800, 700)
		Window.setWindowTitle("Automatic Drum Composer")
		Window.setWindowIcon(QtGui.QIcon('UI/drumkit_icon_small.png'))

		QtGui.QApplication.setStyle("Cleanlooks")

		#Create grid layout
		self.centralwidget = QtGui.QWidget(Window)
		self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
		Window.setCentralWidget(self.centralwidget)

		self.formLayoutWidget = QtGui.QWidget(self.centralwidget)
		self.formLayoutWidget.setGeometry(QtCore.QRect(200, -1, 400, 700))
		self.formLayoutWidget.setObjectName(_fromUtf8("formLayoutWidget"))
		self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
		self.formLayout.setObjectName(_fromUtf8("formLayout"))        

		#Check boxes, sliders and dials
		self.kickBox1 = QtGui.QCheckBox(self.formLayoutWidget)
		self.kickBox1.setObjectName(_fromUtf8("kickBox1"))
		self.kickBox1.sizeHint()
		self.kickBox1.stateChanged.connect(self.kick_placement)
		self.kickBox1.toggle()
		
		self.kickMinSlider = QtGui.QSlider(self.formLayoutWidget)
		self.kickMinSlider.setOrientation(QtCore.Qt.Horizontal)
		self.kickMinSlider.setObjectName(_fromUtf8("kickMinSlider"))
		self.kickMinSlider.setRange(0, 3)
		self.kickMinSlider.sizeHint()
		
		self.kickMaxSlider = QtGui.QSlider(self.formLayoutWidget)
		self.kickMaxSlider.setOrientation(QtCore.Qt.Horizontal)
		self.kickMaxSlider.setObjectName(_fromUtf8("kickMaxSlider"))
		self.kickMaxSlider.setRange(0, 3)	
		self.kickMaxSlider.sizeHint()
		self.kickMaxSlider.setValue(3)	

		self.kickConvSlider = QtGui.QSlider(self.formLayoutWidget)
		self.kickConvSlider.setOrientation(QtCore.Qt.Horizontal)
		self.kickConvSlider.setObjectName(_fromUtf8("kickConvSlider"))
		self.kickConvSlider.setRange(0, 2)
		self.kickConvSlider.sizeHint()
		self.kickConvSlider.setValue(0)
		
		self.kickMinSlider.valueChanged.connect(self.kick_min)
		self.kickMaxSlider.valueChanged.connect(self.kick_max)
		self.kickConvSlider.valueChanged.connect(self.kick_conv)

		self.snareBox1 = QtGui.QCheckBox(self.formLayoutWidget)
		self.snareBox1.setObjectName(_fromUtf8("snareBox1"))
		self.snareBox1.sizeHint()
		self.snareBox1.stateChanged.connect(self.snare_placement)
		self.snareBox1.toggle()

		self.snareMinSlider = QtGui.QSlider(self.formLayoutWidget)
		self.snareMinSlider.setOrientation(QtCore.Qt.Horizontal)
		self.snareMinSlider.setObjectName(_fromUtf8("snareMinSlider"))
		self.snareMinSlider.setRange(0, 3)
		self.snareMinSlider.sizeHint()
		self.snareMinSlider.setValue(2)

		self.snareMaxSlider = QtGui.QSlider(self.formLayoutWidget)
		self.snareMaxSlider.setOrientation(QtCore.Qt.Horizontal)
		self.snareMaxSlider.setObjectName(_fromUtf8("snareMaxSlider"))
		self.snareMaxSlider.setRange(0, 3)
		self.snareMaxSlider.sizeHint()
		self.snareMaxSlider.setValue(3)

		self.snareConvSlider = QtGui.QSlider(self.formLayoutWidget)
		self.snareConvSlider.setOrientation(QtCore.Qt.Horizontal)
		self.snareConvSlider.setObjectName(_fromUtf8("snareConvSlider"))
		self.snareConvSlider.setRange(0, 2)
		self.snareConvSlider.sizeHint()
		self.snareConvSlider.setValue(0)

		self.snareMinSlider.valueChanged.connect(self.snare_min)
		self.snareMaxSlider.valueChanged.connect(self.snare_max)
		self.snareConvSlider.valueChanged.connect(self.snare_conv)		

		self.hatBox1 = QtGui.QCheckBox(self.formLayoutWidget)
		self.hatBox1.setObjectName(_fromUtf8("hatBox1"))
		self.hatBox1.sizeHint()
		self.hatBox1.stateChanged.connect(self.hat_placement)
		self.hatBox1.toggle()		

		self.hatMinSlider = QtGui.QSlider(self.formLayoutWidget)
		self.hatMinSlider.setOrientation(QtCore.Qt.Horizontal)
		self.hatMinSlider.setObjectName(_fromUtf8("hatMinSlider"))
		self.hatMinSlider.setRange(0, 16)
		self.hatMinSlider.sizeHint()
		self.hatMinSlider.setValue(0)

		self.hatMaxSlider = QtGui.QSlider(self.formLayoutWidget)
		self.hatMaxSlider.setOrientation(QtCore.Qt.Horizontal)
		self.hatMaxSlider.setObjectName(_fromUtf8("hatMaxSlider"))
		self.hatMaxSlider.setRange(0, 16)
		self.hatMaxSlider.sizeHint()
		self.hatMaxSlider.setValue(16)

		self.hatConvSlider = QtGui.QSlider(self.formLayoutWidget)
		self.hatConvSlider.setOrientation(QtCore.Qt.Horizontal)
		self.hatConvSlider.setObjectName(_fromUtf8("hatConvSlider"))
		self.hatConvSlider.setRange(0, 3)
		self.hatConvSlider.sizeHint()
		self.hatConvSlider.setValue(0)               

		self.hatMinSlider.valueChanged.connect(self.hat_min)
		self.hatMaxSlider.valueChanged.connect(self.hat_max)
		self.hatConvSlider.valueChanged.connect(self.hat_conv)

		self.percBox1 = QtGui.QCheckBox(self.formLayoutWidget)
		self.percBox1.setObjectName(_fromUtf8("percBox1"))
		self.percBox1.sizeHint()
		self.percBox1.stateChanged.connect(self.perc_placement)
		self.percBox1.toggle()		

		self.percMinSlider = QtGui.QSlider(self.formLayoutWidget)
		self.percMinSlider.setOrientation(QtCore.Qt.Horizontal)
		self.percMinSlider.setObjectName(_fromUtf8("percMinSlider"))
		self.percMinSlider.setRange(0, 1)
		self.percMinSlider.sizeHint()

		self.percMaxSlider = QtGui.QSlider(self.formLayoutWidget)
		self.percMaxSlider.setOrientation(QtCore.Qt.Horizontal)
		self.percMaxSlider.setObjectName(_fromUtf8("percMaxSlider"))
		self.percMaxSlider.setRange(0, 1)
		self.percMaxSlider.sizeHint()
		self.percMaxSlider.setValue(1)

		self.percConvSlider = QtGui.QSlider(self.formLayoutWidget)
		self.percConvSlider.setOrientation(QtCore.Qt.Horizontal)
		self.percConvSlider.setObjectName(_fromUtf8("percConvSlider"))
		self.percConvSlider.setRange(0, 2)
		self.percConvSlider.sizeHint()
		self.percConvSlider.setValue(0)

		self.percMinSlider.valueChanged.connect(self.perc_min)
		self.percMaxSlider.valueChanged.connect(self.perc_max)
		self.percConvSlider.valueChanged.connect(self.perc_conv)

		self.gSnareBox1 = QtGui.QCheckBox(self.formLayoutWidget)
		self.gSnareBox1.setObjectName(_fromUtf8("gSnareBox1"))
		self.gSnareBox1.sizeHint()
		self.gSnareBox1.stateChanged.connect(self.g_snare_placement)
		self.gSnareBox1.toggle()		

		self.gSnareMinSlider = QtGui.QSlider(self.formLayoutWidget)
		self.gSnareMinSlider.setOrientation(QtCore.Qt.Horizontal)
		self.gSnareMinSlider.setObjectName(_fromUtf8("gSnareMinSlider"))
		self.gSnareMinSlider.setRange(0, 3)
		self.gSnareMinSlider.sizeHint()

		self.gSnareMaxSlider = QtGui.QSlider(self.formLayoutWidget)
		self.gSnareMaxSlider.setOrientation(QtCore.Qt.Horizontal)
		self.gSnareMaxSlider.setObjectName(_fromUtf8("gSnareMaxSlider"))
		self.gSnareMaxSlider.setRange(0, 3)
		self.gSnareMaxSlider.sizeHint()
		self.gSnareMaxSlider.setValue(3)

		self.gSnareConvSlider = QtGui.QSlider(self.formLayoutWidget)
		self.gSnareConvSlider.setOrientation(QtCore.Qt.Horizontal)
		self.gSnareConvSlider.setObjectName(_fromUtf8("gSnareConvSlider"))
		self.gSnareConvSlider.setRange(0, 2)
		self.gSnareConvSlider.sizeHint()
		self.gSnareConvSlider.setValue(0)

		self.gSnareMinSlider.valueChanged.connect(self.g_snare_min)
		self.gSnareMaxSlider.valueChanged.connect(self.g_snare_max)
		self.gSnareConvSlider.valueChanged.connect(self.g_snare_conv)	

		self.humanisationDial = QtGui.QDial(self.formLayoutWidget)
		self.humanisationDial.setObjectName(_fromUtf8("humanisationDial"))
		self.humanisationDial.setRange(0, 50)
		self.humanisationDial.setValue(0)

		self.humanisationDial.valueChanged.connect(self.humanisation_amount)

		self.patternLengthBox = QtGui.QComboBox(self.formLayoutWidget)
		self.patternLengthBox.setObjectName(_fromUtf8("patternLengthBox"))
		self.patternLengthBox.addItem("1")
		self.patternLengthBox.addItem("2")

		self.patternLengthBox.activated[str].connect(self.pattern_length)

		self.numberOfPatternsBox = QtGui.QSpinBox(self.formLayoutWidget)
		self.numberOfPatternsBox.setObjectName(_fromUtf8("numberOfPatternsBox"))
		self.numberOfPatternsBox.setMinimum(1)

		self.numberOfPatternsBox.valueChanged.connect(self.number_of_patterns)

		self.inputBox = QtGui.QLineEdit(self.formLayoutWidget)
		self.inputBox.setObjectName(_fromUtf8("inputBox"))				


		#Create labels
		
		self.kickLabel1 = QtGui.QLabel(self.formLayoutWidget)
		self.kickLabel1.setObjectName(_fromUtf8("kickLabel1"))
		self.kickLabel2 = QtGui.QLabel(self.formLayoutWidget)
		self.kickLabel2.setObjectName(_fromUtf8("kickLabel2"))      
		self.kickLabel3 = QtGui.QLabel(self.formLayoutWidget)
		self.kickLabel3.setObjectName(_fromUtf8("kickLabel3"))
		self.kickLabel4 = QtGui.QLabel(self.formLayoutWidget)
		self.kickLabel4.setObjectName(_fromUtf8("kickLabel4"))

		self.snareLabel1 = QtGui.QLabel(self.formLayoutWidget)
		self.snareLabel1.setObjectName(_fromUtf8("snareLabel1"))
		self.snareLabel2 = QtGui.QLabel(self.formLayoutWidget)
		self.snareLabel2.setObjectName(_fromUtf8("snareLabel2"))     
		self.snareLabel3 = QtGui.QLabel(self.formLayoutWidget)
		self.snareLabel3.setObjectName(_fromUtf8("snareLabel3"))
		self.snareLabel4 = QtGui.QLabel(self.formLayoutWidget)
		self.snareLabel4.setObjectName(_fromUtf8("snareLabel4"))

		self.hatLabel1 = QtGui.QLabel(self.formLayoutWidget)
		self.hatLabel1.setObjectName(_fromUtf8("hatLabel1"))
		self.hatLabel2 = QtGui.QLabel(self.formLayoutWidget)
		self.hatLabel2.setObjectName(_fromUtf8("hatLabel2"))     
		self.hatLabel3 = QtGui.QLabel(self.formLayoutWidget)
		self.hatLabel3.setObjectName(_fromUtf8("hatLabel3"))
		self.hatLabel4 = QtGui.QLabel(self.formLayoutWidget)
		self.hatLabel4.setObjectName(_fromUtf8("hatLabel4"))

		self.percLabel1 = QtGui.QLabel(self.formLayoutWidget)
		self.percLabel1.setObjectName(_fromUtf8("percLabel1"))
		self.percLabel2 = QtGui.QLabel(self.formLayoutWidget)
		self.percLabel2.setObjectName(_fromUtf8("percLabel2"))      
		self.percLabel3 = QtGui.QLabel(self.formLayoutWidget)
		self.percLabel3.setObjectName(_fromUtf8("percLabel3"))
		self.percLabel4 = QtGui.QLabel(self.formLayoutWidget)
		self.percLabel4.setObjectName(_fromUtf8("percLabel4"))

		self.gSnareLabel1 = QtGui.QLabel(self.formLayoutWidget)
		self.gSnareLabel1.setObjectName(_fromUtf8("gSnareLabel1"))
		self.gSnareLabel2 = QtGui.QLabel(self.formLayoutWidget)
		self.gSnareLabel2.setObjectName(_fromUtf8("gSnareLabel2"))      
		self.gSnareLabel3 = QtGui.QLabel(self.formLayoutWidget)
		self.gSnareLabel3.setObjectName(_fromUtf8("gSnareLabel3"))
		self.gSnareLabel4 = QtGui.QLabel(self.formLayoutWidget)
		self.gSnareLabel4.setObjectName(_fromUtf8("gSnareLabel4"))

		self.humanisationLabel = QtGui.QLabel(self.formLayoutWidget)
		self.humanisationLabel.setObjectName(_fromUtf8("humanisationLabel"))	

		self.patternLengthLabel = QtGui.QLabel(self.formLayoutWidget)
		self.patternLengthLabel.setObjectName(_fromUtf8("patternLengthLabel"))	

		self.numberOfPatternsLabel = QtGui.QLabel(self.formLayoutWidget)
		self.numberOfPatternsLabel.setObjectName(_fromUtf8("numberOfPatternsLabel"))

		self.inputBoxLabel = QtGui.QLabel(self.formLayoutWidget)
		self.inputBoxLabel.setObjectName(_fromUtf8("inputBoxLabel"))							
		
    	#Generate button
		self.genBtn = QtGui.QPushButton(self.formLayoutWidget)
		self.genBtn.setObjectName(_fromUtf8("pushButton"))
		self.genBtn.sizeHint()
		self.genBtn.clicked.connect(self.generate)
		self.genBtn.resize(self.genBtn.sizeHint())

		#Add objects to formLayout	
		self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.kickLabel1)
		self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.kickBox1)
		self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.kickLabel2)
		self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.kickMinSlider)
		self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.kickLabel3)
		self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.kickMaxSlider)
		self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.kickLabel4)
		self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.kickConvSlider)

		self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.snareLabel1)
		self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.snareBox1)
		self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.snareLabel2)
		self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.snareMinSlider)
		self.formLayout.setWidget(6, QtGui.QFormLayout.LabelRole, self.snareLabel3)
		self.formLayout.setWidget(6, QtGui.QFormLayout.FieldRole, self.snareMaxSlider)
		self.formLayout.setWidget(7, QtGui.QFormLayout.LabelRole, self.snareLabel4)
		self.formLayout.setWidget(7, QtGui.QFormLayout.FieldRole, self.snareConvSlider)	

		self.formLayout.setWidget(8, QtGui.QFormLayout.LabelRole, self.hatLabel1)
		self.formLayout.setWidget(8, QtGui.QFormLayout.FieldRole, self.hatBox1)
		self.formLayout.setWidget(9, QtGui.QFormLayout.LabelRole, self.hatLabel2)
		self.formLayout.setWidget(9, QtGui.QFormLayout.FieldRole, self.hatMinSlider)
		self.formLayout.setWidget(10, QtGui.QFormLayout.LabelRole, self.hatLabel3)
		self.formLayout.setWidget(10, QtGui.QFormLayout.FieldRole, self.hatMaxSlider)
		self.formLayout.setWidget(11, QtGui.QFormLayout.LabelRole, self.hatLabel4)
		self.formLayout.setWidget(11, QtGui.QFormLayout.FieldRole, self.hatConvSlider)

		self.formLayout.setWidget(12, QtGui.QFormLayout.LabelRole, self.percLabel1)
		self.formLayout.setWidget(12, QtGui.QFormLayout.FieldRole, self.percBox1)
		self.formLayout.setWidget(13, QtGui.QFormLayout.LabelRole, self.percLabel2)
		self.formLayout.setWidget(13, QtGui.QFormLayout.FieldRole, self.percMinSlider)
		self.formLayout.setWidget(14, QtGui.QFormLayout.LabelRole, self.percLabel3)
		self.formLayout.setWidget(14, QtGui.QFormLayout.FieldRole, self.percMaxSlider)
		self.formLayout.setWidget(15, QtGui.QFormLayout.LabelRole, self.percLabel4)
		self.formLayout.setWidget(15, QtGui.QFormLayout.FieldRole, self.percConvSlider)

		self.formLayout.setWidget(16, QtGui.QFormLayout.LabelRole, self.gSnareLabel1)
		self.formLayout.setWidget(16, QtGui.QFormLayout.FieldRole, self.gSnareBox1)
		self.formLayout.setWidget(17, QtGui.QFormLayout.LabelRole, self.gSnareLabel2)
		self.formLayout.setWidget(17, QtGui.QFormLayout.FieldRole, self.gSnareMinSlider)
		self.formLayout.setWidget(18, QtGui.QFormLayout.LabelRole, self.gSnareLabel3)
		self.formLayout.setWidget(18, QtGui.QFormLayout.FieldRole, self.gSnareMaxSlider)
		self.formLayout.setWidget(19, QtGui.QFormLayout.LabelRole, self.gSnareLabel4)
		self.formLayout.setWidget(19, QtGui.QFormLayout.FieldRole, self.gSnareConvSlider)

		self.formLayout.setWidget(20, QtGui.QFormLayout.LabelRole, self.humanisationLabel)
		self.formLayout.setWidget(20, QtGui.QFormLayout.FieldRole, self.humanisationDial)

		self.formLayout.setWidget(21, QtGui.QFormLayout.LabelRole, self.patternLengthLabel)
		self.formLayout.setWidget(21, QtGui.QFormLayout.FieldRole, self.patternLengthBox)

		self.formLayout.setWidget(22, QtGui.QFormLayout.LabelRole, self.numberOfPatternsLabel)
		self.formLayout.setWidget(22, QtGui.QFormLayout.FieldRole, self.numberOfPatternsBox)

		self.formLayout.setWidget(23, QtGui.QFormLayout.LabelRole, self.inputBoxLabel)
		self.formLayout.setWidget(23, QtGui.QFormLayout.FieldRole, self.inputBox)		

		self.formLayout.setWidget(24, QtGui.QFormLayout.FieldRole, self.genBtn)											
		
		#Main menu options
		"""
		quitAction = QtGui.QAction("&Quit", Window)
		quitAction.setShortcut("Ctrl+Q")
		quitAction.setStatusTip("Leave The App")
		quitAction.triggered.connect(self.exit)
		
		#Create main menu
		self.menubar = QtGui.QMenuBar(Window)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
		self.menubar.setObjectName(_fromUtf8("menubar"))
		self.menuFile = QtGui.QMenu(self.menubar)
		self.menuFile.setObjectName(_fromUtf8("menuFile"))
		Window.setMenuBar(self.menubar)
		self.statusbar = QtGui.QStatusBar(Window)
		self.statusbar.setObjectName(_fromUtf8("statusbar"))
		Window.setStatusBar(self.statusbar)
		self.actionExit = QtGui.QAction(Window)
		self.actionExit.setObjectName(_fromUtf8("actionExit"))
		self.actionExit.triggered.connect(self.quit)
		self.menuFile.addAction(self.actionExit)
		self.menubar.addAction(self.menuFile.menuAction())
		"""
		self.retranslateUi(Window)


	#Name objects
	def retranslateUi(self, Window):
		self.kickBox1.setText(_translate("Window", "Kick", None))
		self.snareBox1.setText(_translate("Window", "Snare", None))
		self.hatBox1.setText(_translate("Window", "Hi-Hat", None))
		self.percBox1.setText(_translate("Window", "Percussion", None))
		self.gSnareBox1.setText(_translate("Window", "Ghost Snare", None))
		self.genBtn.setText(_translate("Window", "Generate", None))
		self.kickLabel1.setText(_translate("Window", "Kick Toggle", None))
		self.kickLabel2.setText(_translate("Window", "Kick Density Minimum", None))
		self.kickLabel3.setText(_translate("Window", "Kick Density Maximum", None))
		self.kickLabel4.setText(_translate("Window", "Kick Experimentalness", None))
		self.snareLabel1.setText(_translate("Window", "Snare Toggle", None))
		self.snareLabel2.setText(_translate("Window", "Snare Density Minimum", None))
		self.snareLabel3.setText(_translate("Window", "Snare Density Maximum", None))
		self.snareLabel4.setText(_translate("Window", "Snare Experimentalness", None))
		self.hatLabel1.setText(_translate("Window", "Hi-Hat Toggle", None))
		self.hatLabel2.setText(_translate("Window", "Hi-Hat Density Minimum", None))
		self.hatLabel3.setText(_translate("Window", "Hi-Hat Density Maximum", None))
		self.hatLabel4.setText(_translate("Window", "Hi-Hat Experimentalness", None))
		self.percLabel1.setText(_translate("Window", "Percussion Toggle", None))
		self.percLabel2.setText(_translate("Window", "Percussion Density Minimum", None))
		self.percLabel3.setText(_translate("Window", "Percussion Density Maximum", None))
		self.percLabel4.setText(_translate("Window", "Percussion Experimentalness", None))
		self.gSnareLabel1.setText(_translate("Window", "Ghost Snare Toggle", None))
		self.gSnareLabel2.setText(_translate("Window", "Ghost Snare Density Minimum", None))
		self.gSnareLabel3.setText(_translate("Window", "Ghost Snare Density Maximum", None))
		self.gSnareLabel4.setText(_translate("Window", "Ghost Snare Experimentalness", None))
		self.humanisationLabel.setText(_translate("Window", "Humanisation Amount", None))
		self.patternLengthLabel.setText(_translate("Window", "Pattern Length", None))
		self.numberOfPatternsLabel.setText(_translate("Window", "Number of Patterns", None))
		self.inputBoxLabel.setText(_translate("Window", "User Input", None))
		#self.menuFile.setTitle(_translate("MainWindow", "File", None))
		#self.actionExit.setText(_translate("MainWindow", "Exit", None))
		#self.actionExit.setShortcut(_translate("MainWindow", "Ctrl+Q", None))		

	#Constraint variable assignment methods	
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

	def kick_min(self):
		self.kickMin = self.kickMinSlider.value()

	def kick_max(self):
		self.kickMax = self.kickMaxSlider.value()

	def kick_conv(self):
		value = self.kickConvSlider.value()
		if value == 0:
			self.kickCon1 = True 
			self.kickCon2 = True
		if value == 1:
			self.kickCon1 = True
			self.kickCon2 = False
		if value == 2:
			self.kickCon1 = False 
			self.kickCon2 = False

	def snare_min(self):
		self.snareMin = self.snareMinSlider.value()

	def snare_max(self):
		self.snareMax = self.snareMaxSlider.value()

	def snare_conv(self):
		self.snareConvValue = self.snareConvSlider.value()

	def hat_min(self):
		self.hatExpMin = self.hatMinSlider.value()

	def hat_max(self):
		self.hatExpMax = self.hatMaxSlider.value()

	def hat_conv(self):
		self.hatConvValue = self.hatConvSlider.value()

	def perc_min(self):
		self.percMin = self.percMinSlider.value()

	def perc_max(self):
		self.percMax = self.percMaxSlider.value()

	def perc_conv(self):
		value = self.percConvSlider.value()
		if value == 0:
			self.percCon1 = True 
			self.percCon2 = True
		if value == 1:
			self.percCon1 = True
			self.percCon2 = False
		if value == 2:
			self.percCon1 = False 
			self.percCon2 = False

	def g_snare_min(self):
		self.gSnareMin = self.gSnareMinSlider.value()

	def g_snare_max(self):
		self.gSnareMax = self.gSnareMaxSlider.value()

	def g_snare_conv(self):
		value = self.gSnareConvSlider.value()
		if value == 0:
			self.gSnareCon1 = True 
			self.gSnareCon2 = True
		if value == 1:
			self.gSnareCon1 = True
			self.gSnareCon2 = False
		if value == 2:
			self.gSnareCon1 = False 
			self.gSnareCon2 = False

	def humanisation_amount(self):
		self.humanisationAmount = float(self.humanisationDial.value())/1000

	def pattern_length(self, text):
		self.patternLength = int(text)

	def number_of_patterns(self):
		self.numberOfPatterns = self.numberOfPatternsBox.value()

	def constraint_assignment(self):
		if self.snarePlacement == False:
			self.snareExpPlacement = False
			self.snareConvPlacement = False
			self.kickSnareCon1 = False
		elif self.snareConvValue == 0:
			self.snareExpPlacement = False 
			self.snareConvPlacement = True
			self.kickSnareCon1 = True
		elif self.snareConvValue == 1:
			self.snareExpPlacement = True 
			self.snareConvPlacement = False
			self.kickSnareCon1 = True
		else:
			self.snareExpPlacement = True 
			self.snareConvPlacement = False
			self.kickSnareCon1 = False

		if self.hatPlacement == False:
			self.hatExpPlacement = False
			self.hatConvPlacement = False
			self.hatCon1 = False
			self.hatCon2 = False
		elif self.hatConvValue == 0:
			self.hatExpPlacement = False 
			self.hatConvPlacement = True
			self.hatCon1 = True
			self.hatCon2 = True
		elif self.hatConvValue == 1:
			self.hatExpPlacement = False 
			self.hatConvPlacement = True
			self.hatCon1 = True
			self.hatCon2 = False
		elif self.hatConvValue == 2:
			self.hatExpPlacement = True 
			self.hatConvPlacement = False
			self.hatCon1 = True
			self.hatCon2 = False
		else:
			self.hatExpPlacement = True 
			self.hatConvPlacement = False
			self.hatCon1 = False
			self.hatCon2 = False

	def generate(self):

		self.constraint_assignment()

		constraints = [ [self.kickPlacement, self.kickCon1, self.kickCon2], \
		                [self.snareExpPlacement, self.snareConvPlacement], \
		                [self.kickSnareCon1], \
		                [self.hatExpPlacement, self.hatConvPlacement, self.hatCon1, self.hatCon2], \
		                [self.percPlacement, self.percCon1, self.percCon2], \
		                [self.gSnarePlacement, self.gSnareCon1, self.gSnareCon2] ]

		#Patterns will be filled out around any user input given to the program.
		#userInput = []
		inputParameters = ["kickMin(" + str(self.kickMin) + ").", "kickMax(" + str(self.kickMax) + ").", \
							"snareMin(" + str(self.snareMin) + ").", "snareMax(" + str(self.snareMax) + ").", \
							"hatExpMin(" + str(self.hatExpMin) + ").", "hatExpMax(" + str(self.hatExpMax) + ").", \
							"percMin(" + str(self.percMin) + ").", "percMax(" + str(self.percMax) + ").", \
							"gSnareMin(" + str(self.gSnareMin) + ").", "gSnareMax(" + str(self.gSnareMax) + ")."]

		userInput = self.inputBox.text()

		input = inputParameters + [userInput]

		"""
		print(input)
		print("\n")
		print(constraints)
		print("\n")
		"""
		cp.generate_patterns(constraints, self.numberOfPatterns, self.patternLength, self.humanisationAmount, input)
		#sys.exit()

	def quit(self):
		choice = QtGui.QMessageBox.question(self, "Exit",
											"Are you sure you want to exit the program?", 
											QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
		if choice == QtGui.QMessageBox.Yes:
			sys.exit()
		else:
			pass


def main():

	app = QtGui.QApplication(sys.argv)
	Window = QtGui.QMainWindow()
	GUI = MainWindow()
	GUI.setupUi(Window)
	Window.show()
	sys.exit(app.exec_())

main()	
