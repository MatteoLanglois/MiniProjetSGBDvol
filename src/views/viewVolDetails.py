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
        self.label_vol = None
        self.vol = None

    def init_widget(self):
        self.init_header()

        label_title = vtk.Label(self, self.font_style("label"),
                                text="Détails du vol")
        label_title.grid(column=0, row=1, pady=10, padx=10)

        self.label_vol = vtk.Label(self, self.font_style("label"), text="")
        self.label_vol.grid(column=0, row=2, pady=10, padx=10)

        button_reserver = vtk.Button(self, self.button_style(), text="Réserver",
                                     command=lambda: self.controller.reserver(self.vol))
        button_reserver.grid(column=0, row=3, pady=10, padx=10)

        button_retour = vtk.Button(self, self.button_style(), text="Retour",
                                   command=lambda:
                                   self.controller.show_frame(
                                       viewInscription.viewInscription))
        button_retour.grid(column=0, row=4, pady=10, padx=10)

    def change_data(self, vol: 'Flight'):
        self.label_vol.config(text=vol)
        self.vol = vol
