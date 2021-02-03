import tkinter as tk
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QGridLayout, QPushButton, QAction, qApp, QLabel
from PyQt5.QtCore import Qt


class FenetreAccueil(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setParametersUI()
		self.setUI()
		

	def setUI(self):
		menu = self.menuBar()
		fichierMenu = menu.addMenu("&Menu Principal")
		exitAction = QAction('&Exit', self)
		fichierMenu.addAction(exitAction)
		self.barreOutils = self.addToolBar('Quitter')
		self.barreOutils.addAction(exitAction)       
		self.statusBar().showMessage('Barre de statut')
	
	def activate(self):
		self.fenetre.show()



class Fenetre(QWidget):
	def __init__(self):
		super().__init__()
		# Paramètres
		self.parameters()
		# Fenêtre initiale accueil
		self.set_layout_fenetre_initiale()

		# Elements
		# self.bouton1 = QPushButton("test 1")
		# self.bouton1.clicked.connect(self.click_1)
		# self.bouton2 = QPushButton("test 2")
		# self.bouton2.clicked.connect(self.click_2)
		# self.bouton3 = QPushButton("test 3")
		# self.bouton3.clicked.connect(self.click_1)
		# self.bouton4 = QPushButton("test 4")
		# self.bouton4.clicked.connect(self.click_2)
		# self.bouton1.setFixedWidth(100)
		# self.bouton2.setFixedWidth(100)
		# self.bouton3.setFixedWidth(100)
		# self.bouton4.setFixedWidth(100)

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
	
	def set_layout_fenetre_initiale(self):
		# Main layout
		self.layout = QGridLayout()
		self.layout.fillWidth = False
		self.layout.fillHeight = False
		# Background color
		self.setAutoFillBackground(True)
		p = self.palette()
		p.setColor(self.backgroundRole(), Qt.gray)
		self.setPalette(p)
		# Séparation de la fenêtre en 3 zones
		# Zone titre
		self.layout_titre = QGridLayout()
		self.layout_titre.fillWidth = False
		self.layout_titre.fillHeight = False
		# self.layout_titre.setStyleSheet("background-color: gray;")
		# Zone prof
		self.layout_prof = QGridLayout()
		self.layout_prof.fillWidth = False
		self.layout_prof.fillHeight = False
		# self.layout_prof.setStyleSheet("background-color: green;")
		# Zone eleve
		self.layout_eleve = QGridLayout()
		self.layout_eleve.fillHeight = False
		self.layout_eleve.fillWidth = False
		# self.layout_eleve.setStyleSheet("background-color: green;")
		# Ajout des sous-layout au principal
		self.layout.addItem(self.layout_titre, 0, 0, 1, 2)
		self.layout.addItem(self.layout_prof, 1, 0)
		self.layout.addItem(self.layout_eleve, 1, 1)
		# Laytout titre
		self.layout_titre_fprincipale()
		self.layout_prof_fprincipale()
		self.layout_eleve_fprincipale()
		# Layout1
		# self.layout1.addWidget(self.bouton1, 0, 0)
		# self.layout1.addWidget(self.bouton2, 1, 0)
		# Layout1
		# self.layout2.addWidget(self.bouton3, 0, 0)
		# self.layout2.addWidget(self.bouton4, 0, 1)
		# self.setLayout(self.layout)

	def layout_titre_fprincipale(self):
		self.titre_main = QLabel(self)
		self.titre_main.setText("<font color=black>Outil de gestion Moodle</font>")
		self.layout_titre.addWidget(self.titre_main, 0, 0)

	def layout_prof_fprincipale(self):
		self.titre_prof = QLabel(self)
		self.titre_prof.setText("<font color=white>Professeur</font>")
		self.layout_prof.addWidget(self.titre_prof, 0, 0)
		self.bouton1 = QPushButton("test 1")
		self.bouton1.clicked.connect(self.click_1)
		self.bouton1.setFixedWidth(100)
		self.layout_prof.addWidget(self.bouton1, 1, 0)

	def layout_eleve_fprincipale(self):
		self.titre_eleve = QLabel(self)
		self.titre_eleve.setText("<font color=white>Elève</font>")
		self.layout_eleve.addWidget(self.titre_eleve, 0, 0)
		self.bouton2 = QPushButton("test 1")
		self.bouton2.clicked.connect(self.click_2)
		self.bouton2.setFixedWidth(100)
		self.layout_eleve.addWidget(self.bouton1, 1, 0)

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
		self.bouton2.hide()

	def click_2(self):
		print("appui 2")



		
