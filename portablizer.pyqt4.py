import os
import sys
import pkg_resources # make PyInstaller import this
import psutil
import subprocess
import time
import threading

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from PyQt4.QtNetwork import *

class Portablizer(QMainWindow):
  def __init__(self):
    QMainWindow.__init__(self);
    self.resize(1024, 768)
    g = self.frameGeometry()
    g.moveCenter(QDesktopWidget().availableGeometry().center())
    self.move(g.topLeft())
    self.browser = QWebView()
    self.setCentralWidget(self.browser)

  def startBrowser(self):
    self.browser.setHtml('<strong>Loading...</strong>')
    self.browser.show()

  def goto(self, url):
    self.browser.load(QUrl(url))

if getattr(sys, 'frozen', False):
  basedir = sys._MEIPASS
else:
  basedir = os.path.dirname(os.path.abspath(__file__))

def nodedir(file):
  return os.path.join(basedir, "node", file)

nodeurl = 'http://127.0.0.1:3000/'

app = QApplication([])
app.setApplicationName('Portablizer')

portablizer = Portablizer()
portablizer.setWindowTitle('Portablizer')

# kill previous launched but not ended node process
for proc in psutil.process_iter():
  try:
    if proc.name == "node.exe" and proc.getcwd() == basedir:
      proc.kill()
  except:
    pass

# hide console window only in Windows exe
startupinfo = None
try:
  startupinfo = subprocess.STARTUPINFO()
  startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
except:
  pass

# can't use stdout in Windows because there is no console
nodeprocess = None
try:
  subp = [nodedir("node.exe"), nodedir("app.js")]
  if startupinfo is not None:
    nodeprocess = subprocess.Popen(subp, startupinfo=startupinfo)
  else:
    nodeprocess = subprocess.Popen(subp, stdout=subprocess.PIPE)
except:
  QMessageBox.warning(portablizer, "Error", "The application is missing required files. You need to re-install it.")
  if hasattr(nodeprocess, 'kill'):
    nodeprocess.kill()
  sys.exit(1)

portablizer.show()
portablizer.startBrowser()

if startupinfo is not None:
  # in Windows, delay one second
  threading.Timer(1, portablizer.goto(nodeurl))
else:
  # in unix, read node output, when server is ready, goto page
  for line in iter(nodeprocess.stdout.readline, ''):
    if "3000" in line:
      portablizer.goto(nodeurl)
      break

menubar = portablizer.menuBar()
helpMenu = menubar.addMenu('&Options')
openweb = QAction('Reload', app)
openweb.triggered.connect(lambda: portablizer.goto(nodeurl))
helpMenu.addAction(openweb)

appprocess = app.exec_()

if hasattr(nodeprocess, 'kill'):
  nodeprocess.kill()

sys.exit(appprocess)
