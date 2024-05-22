from src.views.view import view
import tkinter as vtk
import src.model as db


"""
Classe viewMain

Vue principale de l'application. Elle hérite de la classe view.
"""


class ViewMain(view):
    """
    Méthode __init__

    Constructeur de la classe viewMain
    """
    def __init__(self, parent, controller):
        vtk.Frame.__init__(self, parent)
        self.listbox = None
        self.label_nb_annonces = None
        self.controller = controller
        self.init_widget()
        self.controller.update()
        self.controller.update_idletasks()
        self.title = "Le Bon Angle"

    def init_widget(self):
        self.init_header()
