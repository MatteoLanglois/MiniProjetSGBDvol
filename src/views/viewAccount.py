from src.views.view import view
import tkinter as vtk
import src.model as db

"""
Classe viewAccount

Vue permettant à l'utilisateur de changer son mot de passe et de voir ses 
réservations. Elle hérite de la classe view.
"""


class viewAccount(view):
    """
    Méthode __init__

    Constructeur de la classe viewAccount
    """
    def __init__(self, parent, controller):
        vtk.Frame.__init__(self, parent)
        self.controller = controller
        self.init_widget()
        self.label_error = None
        self.listbox_offres = None
        self.listbox_annonces = None
        self.title = "Mon compte"

    def init_widget(self):
        self.init_header()