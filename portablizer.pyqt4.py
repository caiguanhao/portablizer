import os
import sys
import pkg_resources # make PyInstaller import this
import psutil
import subprocess
import socket

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
  basedir = sys._MEIPASS # PyInstaller path
else:
  basedir = os.path.dirname(os.path.abspath(__file__))

def nodedir(file):
  return os.path.join(basedir, "node", file)

# if you call this function,
# system would ask user for internet permission for the first time
def findAvailablePort():
  newSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  newSocket.bind(("", 0))
  newSocket.listen(1)
  newPort = newSocket.getsockname()[1]
  newSocket.close()
  return newPort

port = str(findAvailablePort())
nodeurl = 'http://127.0.0.1:' + port + '/'

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

# hide console window only in Windows exe, so don't use stdout in latter code
startupinfo = None
try:
  startupinfo = subprocess.STARTUPINFO()
  startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
except:
  pass

nodeprocess = None
try:
  env = os.environ.copy()
  env['PORTABLIZER_PORT'] = port
  nodeprocess = subprocess.Popen([nodedir("node.exe"), nodedir("app.js")],
    startupinfo=startupinfo, env=env)
except:
  QMessageBox.warning(portablizer, "Error",
    "The application is missing required files. You need to re-install it.")
  if hasattr(nodeprocess, 'kill'):
    nodeprocess.kill()
  sys.exit(1)

portablizer.show()
portablizer.startBrowser()
portablizer.browser.setHtml('''
  <script>setTimeout(function(){ window.location.href="%s"; }, 1000);</script>
  <strong>Loading...</strong>
  ''' % nodeurl)

menubar = portablizer.menuBar()
helpMenu = menubar.addMenu('&Options')
openweb = QAction('Reload', app)
openweb.triggered.connect(lambda: portablizer.goto(nodeurl))
helpMenu.addAction(openweb)

appprocess = app.exec_()

if hasattr(nodeprocess, 'kill'):
  nodeprocess.kill()

sys.exit(appprocess)
