from src.views.view import view
import tkinter as vtk
from src.views import viewInscription
from datetime import timedelta
from src.model import Flight
import src.model as db

"""
Classe viewVolDetails

Vue permettant d'afficher les détails d'un vol
"""


class viewVolDetails(view):
    def __init__(self, parent, controller):
        vtk.Frame.__init__(self, parent)
        self.listbox_otherflights = None
        self.controller = controller
        self.init_widget()
        self.title = "Détails du vol"
        self.label_vol = None
        self.vol = None
        self.dict_vol = None

    def init_widget(self):
        self.init_header()
        self.dict_vol = {}
        label_title = vtk.Label(self, self.font_style("label"),
                                text="Détails du vol")
        label_title.grid(column=0, row=1, pady=10, padx=10)

        self.label_vol = vtk.Label(self, self.font_style("label"), text="")
        self.label_vol.grid(column=0, row=2, pady=10, padx=10)
        if self.controller.is_connected:
            button_reserver = vtk.Button(self, self.button_style(),
                                         text="Réserver",
                                         command=lambda: self.controller.reserver(
                                             self.vol))
            button_reserver.grid(column=0, row=3, pady=10, padx=10)

        label_otherflights = vtk.Label(self, self.font_style("label"),
                                       text="Autres vols disponibles")
        label_otherflights.grid(column=0, row=4, pady=10, padx=10)

        self.listbox_otherflights = vtk.Listbox(self, selectmode=vtk.SINGLE,
                                                width=100, height=10,
                                                font=self.font_style(
                                                    "subtitle"))
        self.listbox_otherflights.grid(column=0, row=5, pady=10, padx=10)
        self.listbox_otherflights.bind('<ButtonRelease-1>', lambda
            event: self.details(self.listbox_otherflights, event))

    def change_data(self, vol: Flight):
        self.vol = vol
        self.label_vol.config(text=vol)

        vols = db.Flight.get_all()
        index = 0
        for _, flight in enumerate(vols):
            if flight != self.vol:
                if ((flight.departure_aeroport == self.vol.departure_aeroport)
                        and (
                                flight.arrival_aeroport == self.vol.arrival_aeroport)):
                    if (self.vol.DepartureDate - timedelta(
                            days=3)) <= vol.DepartureDate <= (
                            self.vol.DepartureDate + timedelta(days=3)):
                        self.dict_vol[index] = flight
                        self.listbox_otherflights.insert(vtk.END, flight)
                        index += 1

    def details(self, listbox, event):
        selected_index = listbox.nearest(event.y)
        if selected_index != -1:
            listbox.delete(0, vtk.END)
            self.change_data(self.dict_vol[selected_index + 1])
