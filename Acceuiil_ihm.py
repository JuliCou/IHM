#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 11:56:55 2021

@author: laurent
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys

class fen(QWidget):
    def __init__(self):
        super().__init__()
        self.InitGUI()
    
    def InitGUI(self):

        self.Titre=QLabel("Outils de gestion moodle")
        self.GR_eleve=QGroupBox("Eleve")
        self.GR_prof=QGroupBox("Prof")
        
        self.Lab_prof=QLabel("Professeur")
        self.slider_prof=QSlider(Qt.Horizontal)
        self.module_prof=QSpinBox()
        self.pres_prof=QSpinBox()
        self.Bt_prof=QPushButton("Valider")
        
        
        self.layout_prof=QVBoxLayout()
        self.layout_prof.addWidget(self.Lab_prof)
        self.layout_prof.addWidget(self.module_prof)
        self.layout_prof.addWidget(self.pres_prof)
        self.layout_prof.addWidget(self.slider_prof)
        self.layout_prof.addWidget(self.Bt_prof)
        self.GR_prof.setLayout(self.layout_prof)
        
        
        self.Lab_eleve=QLabel("Eleve")
        self.slider_eleve=QSpinBox()
        self.slider_eleve=QSlider(Qt.Horizontal)
        self.module_eleve=QSpinBox()
        self.pres_eleve=QSpinBox()
        self.Bt_eleve=QPushButton("Valider")
        
        self.layout_eleve=QVBoxLayout()
        self.layout_eleve.addWidget(self.Lab_eleve)
        self.layout_eleve.addWidget(self.module_eleve)
        self.layout_eleve.addWidget(self.pres_eleve)
        self.layout_eleve.addWidget(self.slider_eleve)
        self.layout_eleve.addWidget(self.Bt_eleve)
        self.GR_eleve.setLayout(self.layout_eleve)
        
        self.layout=QGridLayout()
        self.layout.addWidget(self.Titre,0,0,1,2,Qt.AlignCenter)
        self.layout.addWidget(self.GR_prof,1,0)
        self.layout.addWidget(self.GR_eleve,1,1)
        
        self.setLayout(self.layout)
        
        
        
app=QApplication(sys.argv)
base=fen()
base.show()

app.exec_()        
