from distutils.core import setup
import time, sys, os, py2exe
sys.argv.append('py2exe')
setup(
name='pykoGUI',
version='1.0',
windows=['code.py'],
zipfile = None,
options={
	"py2exe":{
	'bundle_files': 3,
	'compressed': True,
	"includes": ["Tkinter", "tkFileDialog", "ttk", "bs4", "BeautifulSoup", "threading", "tkMessageBox", "requests", "pafy", "os"]
	}
}
)
time.sleep(2)