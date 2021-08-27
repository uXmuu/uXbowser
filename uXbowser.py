import os
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui

path = os.getcwd()
home = "file:///"+path+"/home.html"
home = home.replace("\\","/")
home = str(home)
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl(home))
        self.setCentralWidget(self.browser)
        self.showMaximized()
        self.show()
        self.setWindowIcon(QtGui.QIcon("loko.ico"))
        
       
        
        
        # navbar
        navbar = QToolBar()
        self.addToolBar(navbar)
        navbar.setStyleSheet("background-color: #35363a; color: white")
        back_btn = QAction('selkä', self)
        back_btn.triggered.connect(self.browser.back)
        navbar.addAction(back_btn)

        forward_btn = QAction('vittu eteen päin', self)
        forward_btn.triggered.connect(self.browser.forward)
        navbar.addAction(forward_btn)

        reload_btn = QAction('ei vittu toimi', self)
        reload_btn.triggered.connect(self.browser.reload)
        navbar.addAction(reload_btn)

        home_btn = QAction('ko ti', self)
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        self.browser.urlChanged.connect(self.update_url)

    def navigate_home(self):
        self.browser.setUrl(QUrl(home))

    def navigate_to_url(self):
        url = self.url_bar.text()
        self.browser.setUrl(QUrl(url))

    def update_url(self, q):
        self.url_bar.setText(q.toString())




if "__main__" == __name__:
   
    app = QApplication(sys.argv)
    app.setStyleSheet("background-color: #333333; color: #333333")
    QApplication.setApplicationName('uXbowser')
    window = MainWindow()
    app.exec_()
