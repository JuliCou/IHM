from PyQt5.QtWidgets import QApplication
import tkinter as tk
from qt_classes.fenetres import Fenetre


app = QApplication.instance() 
if not app: # sinon on crée une instance de QApplication
    app = QApplication(["Moodle"])

# création d'une fenêtre avec QWidget dont on place la référence dans fen
fen = Fenetre()
fen.show()

# exécution de l'application, l'exécution permet de gérer les événements
app.exec_()