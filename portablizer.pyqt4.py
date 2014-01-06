import os
import sys
import psutil
import subprocess

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
  basedir = os.path.dirname(__file__)

def nodedir(file):
  return os.path.join(basedir, "node", file)

nodeurl = 'http://127.0.0.1:3000/'

app = QApplication([])
app.setApplicationName('Portablizer')

portablizer = Portablizer()
portablizer.setWindowTitle('Portablizer')

try:
  startupinfo = subprocess.STARTUPINFO()
  startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
except:
  startupinfo = None

for proc in psutil.process_iter():
  try:
    if proc.name == "node.exe" and proc.getcwd() == basedir:
      proc.kill()
  except:
    pass

try:
  nodeprocess = subprocess.Popen([nodedir("node.exe"), nodedir("app.js")], startupinfo=startupinfo, stdout=subprocess.PIPE)
except:
  QMessageBox.warning(portablizer, "Error", "The application is missing required files. You need to re-install it.")
  sys.exit(1)

portablizer.show()
portablizer.startBrowser()

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

try:
  nodeprocess.kill()
except:
  pass

sys.exit(appprocess)
