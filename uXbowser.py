import os
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui, QtWebChannel
from PyQt5.QtNetwork import *
from threading import Thread
import requests
import json
import time

path = os.getcwd()
home = "file:///"+path+"/home.html"
home = home.replace("\\","/")
home = str(home)

class Browser(QWebEnginePage):
    def __init__(self):
        super(QtWebKit.QWebPage, self).__init__()

    def userAgentForUrl(self, url):
        return "uXbowser"



class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        with open("config.json") as f:
            a = json.load(f)
            f.close()
        
        packages = requests.get("""https://raw.githubusercontent.com/uXmuu/uXbowser-packages/main/a.txt""").text
        default_config = requests.get("https://raw.githubusercontent.com/uXmuu/uXbowser-packages/main/config/config.json").json()
        

        
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl(home))
        self.setCentralWidget(self.browser)
        self.showMaximized()
        self.show()
        self.setWindowIcon(QtGui.QIcon("loko.ico"))
        self.browser.settings().setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)
        
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
        reload_btn.triggered.connect(lambda: self.reload())
        self.navbar.addAction(reload_btn)

        home_btn = QAction('koti', self)
        home_btn.triggered.connect(self.navigate_home)
        self.navbar.addAction(home_btn)

        #update_button = QAction("ehkä",self)
        #update_button.triggered.connect(lambda aa = json.load(open("config.json")): self.update(aa))
        #self.navbar.addAction(update_button)

        self.shitscript_btn = QAction("shitscript: on", self)
        self.shitscript_btn.triggered.connect(lambda: self.disableJS(False))
        self.navbar.addAction(self.shitscript_btn)


        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.navbar.addWidget(self.url_bar)

        self.browser.page().fullScreenRequested.connect(self.handleFullscreenRequest)
        QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)




        
        

        
        uXbar = self.menuBar()

        kyllä = uXbar.addMenu("kyllä")
        

        for i in packages.split("\n")[:-1]:
            self.btn = kyllä.addAction(i)            
            text = self.btn.text()
            self.btn.triggered.connect(lambda ch, text=text : self.install(text))

        uXbar2 = self.menuBar()
        self.ei = uXbar2.addMenu("ei")
        self.p_list = []
        try:
	        for i in os.listdir("packages"):
	                i = i.replace("__pycache__", "").replace(".py","")
	                self.btn2 = self.ei.addAction(i)
	                text = self.btn2.text(); self.p_list.append(text)
	                self.btn2.triggered.connect(lambda ch, text=text : Thread(target=lambda: self.use(text)).start())

        except:
        	pass
        with open("config.json") as aa:
            self.update(aa)
        
        #self.setStyleSheet(f["app_style"])

    def use(self,a):
        sys.path.insert(1,"packages")
        #a = __import__(a)
        os.system("python packages/"+a+".py")

            
        #self.browser.page().runJavaScript(f'document.body.style.color = "white"; document.body.style.color = "yellow"; document.body.style.backgroundColor = "red";')
                    
        
    

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
            f.write(o)
            f.close()
            self.no_voi_vittu()
            
        
        except:
            
            p = os.system("mkdir packages")
            if p == 0:
                self.install(a)
        
        #Thread(target=lambda: self.use(a)).start()
    def userAgentForUrl(self, url):

        return "uXbowser"

        


        

    def update(self,a):
       
        with open("config.json") as f:
            f = json.load(f)
                
                
                        
        self.setStyleSheet(f["app_style"])
        self.navbar.setStyleSheet(f["navbar_style"])

    def reload(self):
        #self.browser.reload()
        aaa = json.load(open("config.json"))
        self.update(aaa)
        
        self.browser.page().runJavaScript(f'document.body.style.color = "{aaa["body_color"]}";')
        self.browser.page().runJavaScript(f'document.body.style.backgroundColor = "{aaa["body_background-color"]}";')
        self.browser.page().runJavaScript('''var divs = document.getElementsByTagName("div");
                                             for(var i = 0; i < divs.length; i++){
                                                divs[i].style.color = "%s"
                                                divs[i].style.backgroundColor = "%s";}''' % (aaa["body_color"],aaa["body_background-color"] ))

    def disableJS(self, a):             
        settings = QWebEngineSettings.globalSettings()
        o = self.shitscript_btn.text()
        if not a:
            print(o)
            if o == "shitscript: off":
                self.disableJS(True)
               
            else:
                self.shitscript_btn.setText("shitscript: off")
                settings.setAttribute(QWebEngineSettings.JavascriptEnabled, False)

            
        else:
            self.shitscript_btn.setText("shitscript: on")
            settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
    def no_voi_vittu(self):
        try:
            for i in os.listdir("packages"):
                    i = i.replace("__pycache__", "").replace(".py","")
                    if not i in self.p_list:
                        self.btn2 = self.ei.addAction(i)
                        text = self.btn2.text()
                        self.btn2.triggered.connect(lambda ch, text=text : Thread(target=lambda: self.use(text)).start())

        except:
            pass
    def handleFullscreenRequest(self, request):
        request.accept()

        if request.toggleOn():
            self.browser.setParent(None)
            self.browser.showFullScreen()
            
        else:
            self.setCentralWidget(self.browser)
            self.browser.showNormal()
            



           
      

if "__main__" == __name__:
    with open("config.json") as f:
        a = json.load(f)
    try:
        app = QApplication(sys.argv)
        app.setStyleSheet(a["app_style"])

        
        QApplication.setApplicationName('uXbowser')
        window = MainWindow()
    except Exception as e:
        print(e)
        app.exec_()
        
        try:
            app = QApplication(sys.argv)
            app.setStyleSheet(a["app_style"])

                
            QApplication.setApplicationName('uXbowser')
            window = MainWindow()
        except:
            pass
    app.exec_()



