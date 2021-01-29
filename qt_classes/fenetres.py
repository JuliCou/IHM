import tkinter as tk
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QAction, qApp
from PyQt5.QtCore import Qt


class FenetrePrincipale(QMainWindow):
	def __init__(self):
		super().__init__()
        self.setParametersUI()
		self.setUI()

    def setParametersUI():
        root = tk.Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
		self.setGeometry(int(0.07*screen_width), int(0.07*screen_height), int(0.7*screen_width), int(0.7*screen_height))
		self.setWindowTitle('Fenêtre principale')

	def setUI(self):
		menu = self.menuBar()
		fichierMenu = menu.addMenu("&Menu Principal")
		fichierMenu.addAction(QAction('&Exit', self))
		self.barreOutils = self.addToolBar('Quitter')
		self.barreOutils.addAction(exitAction)       
		self.statusBar().showMessage('Barre de statut')



class Fenetre(QWidget):
    def __init__(self):
        super().__init__()
        self.parameters()
        # Elements
        self.bouton1 = QPushButton("test 1")
        self.bouton1.clicked.connect(self.click_1)
        self.bouton2 = QPushButton("test 2")
        self.bouton2.clicked.connect(self.click_2)
        # Laytout
        self.layout()

    def parameters(self):
        self.setWindowTitle("Outil de suivi des élèves")
        # Screen size with Tkinter
        root = tk.Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        # Set Size and position
        self.resize(int(0.7*screen_width), int(0.7*screen_height))
        self.move(int(0.05*screen_width), int(0.05*screen_height))
        # Options
        self.setMouseTracking(False)
    
    def layout(self):
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.bouton1)
        self.layout.addWidget(self.bouton2)
        self.setLayout(self.layout)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print("Click gauche")
        if event.button() == Qt.RightButton:
            print("Click droit")
        print("position = " + str(event.x()) + " " + str(event.y()))

    def mouseReleaseEvent(self, event):
        print("release")

    def mouseDoubleClickEvent(self, event):
        print("double click")
    
    def mouseMoveEvent(self, event):
        print("mouvement")
    
    def click_1(self):
        print("appui 1")

    def click_2(self):
        print("appui 2")



        