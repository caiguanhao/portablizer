import os
import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from PyQt4.QtNetwork import *

class Portablizer(QMainWindow):
  def __init__(self):
    QMainWindow.__init__(self);
    self.resize(1024, 768)
    self.browser = QWebView()
    self.setCentralWidget(self.browser)
    self.browser.setHtml('<strong>Hello World!</strong>')
    self.browser.show()

  def goto(self, url):
    self.browser.load(QUrl(url))

if getattr(sys, 'frozen', False):
  basedir = sys._MEIPASS
else:
  basedir = os.path.dirname(__file__)

app = QApplication([])
app.setApplicationName('Portablizer')

portablizer = Portablizer()
portablizer.setWindowTitle('Portablizer')
portablizer.show()

menubar = portablizer.menuBar()
helpMenu = menubar.addMenu('&Help')
openweb = QAction('Open website', app)
openweb.triggered.connect(lambda: portablizer.goto('http://en.m.wikipedia.org/wiki/Main_Page'))
helpMenu.addAction(openweb)

sys.exit(app.exec_())
