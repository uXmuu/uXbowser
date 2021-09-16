import os
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui
from threading import Thread
import requests
from qtwidgets import Toggle
from qtwidgets import AnimatedToggle

path = os.getcwd()
home = "file:///"+path+"/home.html"
home = home.replace("\\","/")
home = str(home)
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        
        packages = requests.get("""https://raw.githubusercontent.com/uXmuu/uXbowser-packages/main/a.txt""").text
        print(packages)

        
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl(home))
        self.setCentralWidget(self.browser)
        self.showMaximized()
        self.show()
        self.setWindowIcon(QtGui.QIcon("loko.ico"))
        
        self.shortcut1 = QShortcut(QKeySequence("Ctrl+R"), self)
        self.shortcut1.activated.connect(self.browser.reload)

        self.shortcut2 = QShortcut(QKeySequence("Ctrl+S"), self)
        self.shortcut2.activated.connect(self.browser.back)

        self.shortcut3 = QShortcut(QKeySequence("Ctrl+F"), self)
        self.shortcut3.activated.connect(self.browser.forward)

        self.shortcut4 = QShortcut(QKeySequence("Ctrl+H"), self)
        self.shortcut4.activated.connect(self.navigate_home)



        
        
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
        toggle_1 = Toggle()
        toggle_2 = AnimatedToggle(
            checked_color="#FFB000",
            pulse_checked_color="#44FFB000"
        )

        uXbar = self.menuBar()

        kyllä = uXbar.addMenu("kyllä")
        

        for i in packages.split("\n"):
        	self.btn = kyllä.addAction(i)            
        	text = self.btn.text()
        	self.btn.triggered.connect(lambda ch, text=text : self.install(text))
        	#self.btn.addAction(toggle_2)

    def navigate_home(self):
        self.browser.setUrl(QUrl(home))

    def navigate_to_url(self):
        url = self.url_bar.text()
        self.browser.setUrl(QUrl(url))

    def update_url(self, q):
        self.url_bar.setText(q.toString())
    def install(self,a):
    	file = "https://raw.githubusercontent.com/uXmuu/uXbowser-packages/main/"+a+".py"
    	o = requests.get(file).text
    	try:
    		f = open("packages/"+a+".py","w")
    	except:
    		os.system("mkdir packages")
    		self.install(a)
    	f.write(o)
    	print(file)


    
    
    




if "__main__" == __name__:
   
    app = QApplication(sys.argv)
    app.setStyleSheet("background-color: #333333; color: #333333")
    
    QApplication.setApplicationName('uXbowser')
    window = MainWindow()
    app.exec_()
