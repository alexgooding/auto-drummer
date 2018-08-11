# Automatic Drum Composition Using Answer Set Programming
A drum pattern composition tool, named Auto Drummer, created using answer set programming. Auto Drummer was ideally built to aid drum pattern programming 
in electronic music production. The style of drumming outputted is focused around traditional Drum & Bass 'breakbeats' however,
the pattern generated can be used in any genre of music, particularly less constrained outputs. 

The patterns themselves are primarily modeled using answer set programming in AnsProlog. Data handling and the GUI are handled in Python.
The patterns are outputted in MIDI format for easy implementation in any DAW.

## Getting Started

To start generating drum patterns, open the executable file. Click 'generate' to create your first one bar pattern.
The GUI makes it clear what parameters can be controlled.

## Prerequisites

To use the single file distribution, it must be opened on Windows OS. The distribution may run on Linux OS and Mac OS through Wine, 
although this is untested. Download Wine from https://www.winehq.org/. To run Auto Drummer enter

```
wine Auto Drummer.exe
```

## Installing

If you are not using Windows OS, to deploy from the command line, several packages are required as well as a Python 2.X or 3.X build. 
Download Python from https://www.python.org/downloads. All other necessary packages can all be installed via pip once Python is installed.

```
pip install pyqt4
pip install numpy
pip install matplotlib
pip install MIDIUtil
```
Depending on your version of Python, PyQt4 may have to be installed with a wheel. If a pip installation does not work, try 
downloading the relevant wheel from https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyqt4. Then enter on the command line

```
C:\path\where\wheel\is\> pip install wheel_file.whl
```
Non-Windows users may need to replace the Clingo solver. Please consult https://github.com/potassco/clingo/releases for more information.

Everything necessary to generate the patterns themselves is listed above. 
However, to play preview audio of the patterns, FluidSynth must be installed. This can be done by consulting the FluidSynth website, http://www.fluidsynth.org.

Once everything is installed correctly, the program can be run with

```
python auto_drummer.py
```

## Authors

* **Alex Gooding** - *Creator/Developer*

## License

This project is licensed under the GNU General Public License - see the [LICENSE](LICENSE) file for details.
