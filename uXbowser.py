import os
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui
from threading import Thread
import requests
import json
import time

path = os.getcwd()
home = "file:///"+path+"/home.html"
home = home.replace("\\","/")
home = str(home)
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        with open("config.json") as f:
            a = json.load(f)
        
        packages = requests.get("""https://raw.githubusercontent.com/uXmuu/uXbowser-packages/main/a.txt""").text
        default_config = requests.get("https://raw.githubusercontent.com/uXmuu/uXbowser-packages/main/config/config.json").json()
        print(default_config)

        
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

        self.shortcut5 = QShortcut(QKeySequence("Ctrl+X"), self)
        self.shortcut5.activated.connect(sys.exit)



        self.navbar = QToolBar()
        self.addToolBar(self.navbar)
        self.navbar.setStyleSheet(a["navbar_style"])
        back_btn = QAction('selkä', self)
        back_btn.triggered.connect(self.browser.back)
        self.navbar.addAction(back_btn)

        forward_btn = QAction('vittu eteen päin', self)
        forward_btn.triggered.connect(self.browser.forward)
        self.navbar.addAction(forward_btn)

        reload_btn = QAction('ei vittu toimi', self)
        reload_btn.triggered.connect(self.browser.reload)
        self.navbar.addAction(reload_btn)

        home_btn = QAction('koti', self)
        home_btn.triggered.connect(self.navigate_home)
        self.navbar.addAction(home_btn)

        update_button = QAction("ehkä",self)
        update_button.triggered.connect(lambda aa = json.load(open("config.json")): self.update(aa))
        self.navbar.addAction(update_button)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.navbar.addWidget(self.url_bar)

        Thread(target=lambda aa = json.load(open("config.json")): self.update(aa)).start()
        

        
        uXbar = self.menuBar()

        kyllä = uXbar.addMenu("kyllä")
        

        for i in packages.split("\n")[:-1]:
            self.btn = kyllä.addAction(i)            
            text = self.btn.text()
            self.btn.triggered.connect(lambda ch, text=text : self.install(text))

        uXbar2 = self.menuBar()
        self.ei = uXbar2.addMenu("ei")
        try:
	        for i in os.listdir("packages")[:-2]:
	                i = i.replace("__pycache__", "").replace(".py","")
	                self.btn2 = self.ei.addAction(i)
	                text = self.btn2.text()
	                self.btn2.triggered.connect(lambda ch, text=text : Thread(target=lambda: self.use(text)).start())
        except:
        	pass
        
        default = self.ei.addAction("default")
        
        default.triggered.connect(lambda: self.default(default_config))
        
    def default(self,a):
    	with open("config.json","w") as u:
    		json.dump(a,u)

    def navigate_home(self):
        self.browser.setUrl(QUrl(home))

    def navigate_to_url(self):
        url = self.url_bar.text()
        self.browser.setUrl(QUrl("https://duckduckgo.com/"+url))

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
        Thread(target=lambda: self.use(a)).start()

        


    def use(b,a):
        sys.path.insert(1,"packages")
        a = __import__(a)

    def update(self,a):
        try:
            while 1:
                with open("config.json") as f:
                    f = json.load(f)
            
                if a != f:
                    self.setStyleSheet(f["app_style"])
                    self.navbar.setStyleSheet(f["navbar_style"])
                    time.sleep(5)
        except:
            self.update(a)
           
      

if "__main__" == __name__:
    with open("config.json") as f:
        a = json.load(f)
   
    app = QApplication(sys.argv)
    #app.setStyleSheet(a["app_style"])

    
    QApplication.setApplicationName('uXbowser')
    window = MainWindow()
    app.exec_()



