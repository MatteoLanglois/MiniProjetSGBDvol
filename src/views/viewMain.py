from src.model import Flight
from src.views.view import view
from src.views import viewVolDetails
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
        self.title = "Vol"

    def init_widget(self):
        self.init_header()

        dict_vol = {}
        vols = db.Flight.get_all()
        self.label_nb_annonces = vtk.Label(self, self.font_style("label"),
                                           text="Nombre de vols : "
                                                + str(len(dict_vol)))

        self.listbox = vtk.Listbox(self, selectmode=vtk.SINGLE)
        self.listbox.bind('<ButtonRelease-1>', lambda
            event: self.details(self.listbox, event, dict_vol))
        self.listbox.grid(column=0, row=2, columnspan=5, pady=10, padx=10)
        for index, vol in enumerate(vols):
            dict_vol[index] = vol
            self.listbox.insert(vtk.END, vol.print())

        button_reserver = vtk.Button(self, self.button_style(), text="Réserver",
                                     command=lambda: self.controller.reserver(
                                         dict_vol[self.listbox.get(vtk.ACTIVE)])
                                     )
        button_reserver.grid(column=0, row=3, pady=10, padx=10)

    def details(self, listbox, event, dict_vol: dict):
        selected_index = listbox.nearest(event.y)
        if selected_index != -1:
            vol = Flight.get_by_id(dict_vol[selected_index].idFlight)
            self.controller.show_frame(
                viewVolDetails.viewVolDetails)
            (self.controller.frames[viewVolDetails.viewVolDetails]
             .change_data(vol))
