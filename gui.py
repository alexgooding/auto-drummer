import sys 
import os
from PyQt4 import QtGui, QtCore
from midi2audio import FluidSynth #Also requires fluidsynth install
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

	#Generate counter
	c = 0

	#At least one pattern generated boolean
	success = True

	#No patterns generated
	fail = False

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

	fills = False

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

	buttonBools = {}
	for i in range(5):
		for j in range(16):
			buttonBools[(i, j)] = False

	savePath = os.getcwd()

	def setupUi(self, Window):
		#Create main window
		Window.setObjectName(_fromUtf8("Window"))
		Window.resize(800, 800)
		Window.setWindowTitle("Automatic Drum Composer")
		Window.setWindowIcon(QtGui.QIcon('UI/drumkit_icon_small.png'))

		QtGui.QApplication.setStyle("Cleanlooks")

		#Create layout
		self.tabLayout = QtGui.QTabWidget(Window)
		self.tabLayout.setObjectName(_fromUtf8("tabLayout"))
		self.tabLayout.setGeometry(QtCore.QRect(0, 30, 800, 670))
		self.tabLayout.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
		self.tabLayout.setTabPosition(QtGui.QTabWidget.North)
		self.tabLayout.setTabShape(QtGui.QTabWidget.Rounded)
		self.tabLayout.setObjectName(_fromUtf8("tabLayout"))
		self.basicTab = QtGui.QWidget()
		self.basicTab.setObjectName(_fromUtf8("basicTab"))
		self.tabLayout.addTab(self.basicTab, _fromUtf8(""))
		self.advancedTab = QtGui.QWidget()
		self.advancedTab.setObjectName(_fromUtf8("advancedTab"))
		self.tabLayout.addTab(self.advancedTab, _fromUtf8(""))
		self.inputTab = QtGui.QWidget()
		self.inputTab.setObjectName(_fromUtf8("inputTab"))
		self.tabLayout.addTab(self.inputTab, _fromUtf8(""))
		Window.setCentralWidget(self.tabLayout)

		self.gridLayoutWidget = QtGui.QWidget(self.inputTab)
		self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 200, 800, 180))
		self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)

		self.boxLayoutWidget = QtGui.QWidget(self.basicTab)
		self.boxLayoutWidget.setGeometry(QtCore.QRect(0, 200, 800, 350))
		self.boxLayout = QtGui.QVBoxLayout(self.boxLayoutWidget)

		self.formLayoutWidget = QtGui.QWidget(self.advancedTab)
		self.formLayoutWidget.setGeometry(QtCore.QRect(200, -1, 400, 700))
		self.formLayoutWidget.setObjectName(_fromUtf8("formLayoutWidget"))
		self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
		self.formLayout.setObjectName(_fromUtf8("formLayout"))   

		self.formLayoutWidget_2 = QtGui.QWidget(self.basicTab)
		self.formLayoutWidget_2.setGeometry(QtCore.QRect(200, -1, 400, 700))
		self.formLayoutWidget_2.setObjectName(_fromUtf8("formLayoutWidget_2"))
		self.formLayout_2 = QtGui.QFormLayout(self.formLayoutWidget_2)
		self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))  

		#Check boxes, sliders, dials, buttons and text boxes
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

		self.patternLengthBox = QtGui.QSpinBox(self.formLayoutWidget_2)
		self.patternLengthBox.setObjectName(_fromUtf8("patternLengthBox"))
		self.patternLengthBox.setMinimum(1)
		self.patternLengthBox.setMaximum(32)

		self.patternLengthBox.valueChanged.connect(self.pattern_length)

		self.fillsBox = QtGui.QCheckBox(self.formLayoutWidget_2)
		self.fillsBox.setObjectName(_fromUtf8("fillsBox"))
		self.fillsBox.stateChanged.connect(self.fills_enabled)

		self.saveNameBox = QtGui.QLineEdit(self.formLayoutWidget_2)
		self.saveNameBox.setObjectName(_fromUtf8("saveNameBox"))	
		self.saveNameBox.setText("drum_pattern")

		self.inputButtons = {}

		for i in range(5):
		    for j in range(16):
		        # keep a reference to the buttons
		        index = (i, j)
		        self.inputButtons[index] = QtGui.QPushButton()
		        self.inputButtons[index].clicked.connect(self.make_toggle_input(index))
		        # add to the layout
		        self.gridLayout.addWidget(self.inputButtons[index], i, j + 1)

		self.inputButtonLabels = {}
		for i in range(16):
			labelName = str(i + 1)
			label = QtGui.QLabel(labelName)
			label.setAlignment(QtCore.Qt.AlignCenter)
			self.inputButtonLabels[i] = label
			self.gridLayout.addWidget(self.inputButtonLabels[i], 5, i + 1)

		self.kickInputLabel = QtGui.QLabel("Kick")
		self.gridLayout.addWidget(self.kickInputLabel, 0, 0)
		self.snareInputLabel = QtGui.QLabel("Snare")
		self.gridLayout.addWidget(self.snareInputLabel, 1, 0)
		self.hatInputLabel = QtGui.QLabel("Hi-Hat")
		self.gridLayout.addWidget(self.hatInputLabel, 2, 0)
		self.percInputLabel = QtGui.QLabel("Percussion")
		self.gridLayout.addWidget(self.percInputLabel, 3, 0)
		self.gSnareInputLabel = QtGui.QLabel("Ghost Snare")
		self.gridLayout.addWidget(self.gSnareInputLabel, 4, 0)

		self.genBtn = QtGui.QPushButton(self.formLayoutWidget_2)
		self.genBtn.setObjectName(_fromUtf8("pushButton"))
		self.genBtn.sizeHint()
		self.genBtn.clicked.connect(self.generate)
		self.genBtn.resize(self.genBtn.sizeHint())

		self.playBtn = QtGui.QPushButton(self.formLayoutWidget_2)
		self.playBtn.setObjectName(_fromUtf8("pushButton_2"))
		self.playBtn.sizeHint()
		self.playBtn.clicked.connect(self.play_audio)
		self.playBtn.resize(self.genBtn.sizeHint())

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

		self.patternLengthLabel = QtGui.QLabel(self.formLayoutWidget_2)
		self.patternLengthLabel.setObjectName(_fromUtf8("patternLengthLabel"))	

		self.fillsLabel = QtGui.QLabel(self.formLayoutWidget_2)
		self.fillsLabel.setObjectName(_fromUtf8("fillsLabel"))		

		self.saveNameBoxLabel = QtGui.QLabel(self.formLayoutWidget_2)
		self.saveNameBoxLabel.setObjectName(_fromUtf8("saveNameBoxLabel"))							
		
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

		self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.patternLengthLabel)
		self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.patternLengthBox)

		self.formLayout_2.setWidget(2, QtGui.QFormLayout.LabelRole, self.fillsLabel)
		self.formLayout_2.setWidget(2, QtGui.QFormLayout.FieldRole, self.fillsBox)

		self.formLayout_2.setWidget(3, QtGui.QFormLayout.LabelRole, self.saveNameBoxLabel)
		self.formLayout_2.setWidget(3, QtGui.QFormLayout.FieldRole, self.saveNameBox)		

		self.formLayout_2.setWidget(4, QtGui.QFormLayout.LabelRole, self.genBtn)
		self.formLayout_2.setWidget(4, QtGui.QFormLayout.FieldRole, self.playBtn)
		self.playBtn.setVisible(False)

		self.playShortcut = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+P"), self.formLayoutWidget_2)
		self.playShortcut.activated.connect(self.play_audio)

		#Main menu options

		self.actionExit = QtGui.QAction(Window)
		self.actionExit.setObjectName(_fromUtf8("actionExit"))
		self.actionExit.triggered.connect(self.quit)

		self.actionPath = QtGui.QAction(Window)
		self.actionPath.setObjectName(_fromUtf8("actionPath"))
		self.actionPath.triggered.connect(self.pick_path)

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

		self.menuFile.addAction(self.actionPath)
		self.menuFile.addSeparator()
		self.menuFile.addAction(self.actionExit)
		self.menubar.addAction(self.menuFile.menuAction())		
		
		self.retranslateUi(Window)


	#Name objects
	def retranslateUi(self, Window):
		self.kickBox1.setText(_translate("Window", "Kick", None))
		self.snareBox1.setText(_translate("Window", "Snare", None))
		self.hatBox1.setText(_translate("Window", "Hi-Hat", None))
		self.percBox1.setText(_translate("Window", "Percussion", None))
		self.gSnareBox1.setText(_translate("Window", "Ghost Snare", None))
		self.genBtn.setText(_translate("Window", "Generate", None))
		self.playBtn.setText(_translate("Window", "Play", None))
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
		self.fillsLabel.setText(_translate("Window", "Enable Fills", None))
		self.saveNameBoxLabel.setText(_translate("Window", "File Save Name", None))
		self.menuFile.setTitle(_translate("Window", "File", None))
		self.actionExit.setText(_translate("Window", "Exit", None))
		self.actionExit.setShortcut(_translate("Window", "Ctrl+Q", None))
		self.actionPath.setText(_translate("Window", "Choose Save Location", None))		
		self.tabLayout.setTabText(self.tabLayout.indexOf(self.basicTab), _translate("Window", "Basic", None))
		self.tabLayout.setTabText(self.tabLayout.indexOf(self.advancedTab), _translate("Window", "Advanced", None))
		self.tabLayout.setTabText(self.tabLayout.indexOf(self.inputTab), _translate("Window", "Pattern Input", None))

	#Constraint variable assignment methods	
	def fills_enabled(self, state):
		if state == QtCore.Qt.Checked:
			self.fills = True
		else:
			self.fills = False

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
		self.patternLength = self.patternLengthBox.value()

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

	def pick_path(self):
		dialog = QtGui.QFileDialog()
		folder_path = dialog.getExistingDirectory(None, "Select Folder")
		self.savePath = folder_path

	def make_toggle_input(self, index):
		def toggle_input():
			if self.buttonBools[index] == True:
				self.inputButtons[index].setStyleSheet("")
				self.buttonBools[index] = False
			else:
				self.inputButtons[index].setStyleSheet("background-color: black")
				self.buttonBools[index] = True
		return toggle_input

	def determine_input(self):
		input = ""
		for i in range(16):
			label = i + 1
			if self.buttonBools[(0, i)] == True:
				input += "chooseHit(k, " + str(label) + "). "
		for i in range(16):
			label = i + 1
			if self.buttonBools[(1, i)] == True:
				input += "chooseHit(s, " + str(label) + "). "
		for i in range(16):
			label = i + 1
			if self.buttonBools[(2, i)] == True:
				input += "chooseHit(h, " + str(label) + "). "
		for i in range(16):
			label = i + 1
			if self.buttonBools[(3, i)] == True:
				input += "chooseHit(p, " + str(label) + "). "
		for i in range(16):
			label = i + 1
			if self.buttonBools[(4, i)] == True:
				input += "chooseHit(g, " + str(label) + "). "	

		return input

	def play_audio(self):
		midiPath = self.savePath + "\\" + self.saveName + ".mid"
		FluidSynth('Soundfont\\dnb_kit.sf2').play_midi(midiPath)

	def null_method(self):
		return

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

		userInput = self.determine_input()

		self.saveName = self.saveNameBox.text()

		input = inputParameters + [userInput]

		if self.success and self.fail == False and self.c != 0:
			self.boxLayout.removeWidget(self.patternPlot)
			self.patternPlot.deleteLater()
			self.patternPlot = None

			self.playBtn.setVisible(False)

		self.patternPlot = cp.generate_patterns(constraints, self.savePath, self.saveName, self.patternLength, self.fills, self.humanisationAmount, input)

		#Allow user to see the play button
		self.playBtn.setVisible(True)

		#Plotting the pattern generated if one exists
		if self.patternPlot == None:
			if self.fail == False:
				self.nullLabel = QtGui.QLabel("No patterns have been found.")
				self.nullLabel.setAlignment(QtCore.Qt.AlignCenter)
				self.nullLabel.setFont(QtGui.QFont("Verdana", 24))
				self.boxLayout.addWidget(self.nullLabel)
			self.playBtn.setVisible(False)
			self.fail = True
		else:
			if self.fail:
				self.boxLayout.removeWidget(self.nullLabel)
				self.nullLabel.deleteLater()
				self.nullLabel = None				
			self.boxLayout.addWidget(self.patternPlot)
			self.success = True
			self.fail = False 
			self.c += 1


	def quit(self):
		choice = QtGui.QMessageBox.question(None, "Exit",
											"Are you sure you want to exit the program?", 
											QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
		if choice == QtGui.QMessageBox.Yes:
			sys.exit()
		else:
			pass


def run_app():

	app = QtGui.QApplication(sys.argv)
	Window = QtGui.QMainWindow()
	GUI = MainWindow()
	GUI.setupUi(Window)
	Window.show()
	sys.exit(app.exec_())
	
