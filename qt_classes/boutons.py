from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import Qt

class Bouton(QPushButton):
    def __init__(self, text):
        QPushButton.__init__(self, text)