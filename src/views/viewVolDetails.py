from src.model import Flight
from src.views.view import view
import tkinter as vtk
from src.views import viewInscription


"""
Classe viewVolDetails

Vue permettant d'afficher les détails d'un vol
"""


class viewVolDetails(view):
    def __init__(self, parent, controller):
        vtk.Frame.__init__(self, parent)
        self.controller = controller
        self.init_widget()
        self.title = "Détails du vol"

    def init_widget(self):
        pass

    def change_data(self, vol: 'Flight'):
        pass
