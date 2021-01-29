from PyQt5.QtWidgets import QApplication
import tkinter as tk
from qt_classes.fenetres import FenetrePrincipale



# Première étape : création d'une application Qt avec QApplication
#    afin d'avoir un fonctionnement correct avec IDLE ou Spyder
#    on vérifie s'il existe déjà une instance de QApplication
app = QApplication.instance() 
if not app: # sinon on crée une instance de QApplication
    app = QApplication(["Moodle"])

# création d'une fenêtre avec QWidget dont on place la référence dans fen
fen = FenetrePrincipale()
fen.show()

# exécution de l'application, l'exécution permet de gérer les événements
app.exec_()