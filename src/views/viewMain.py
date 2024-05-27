import datetime
from tkinter import ttk

from tkcalendar import DateEntry

from src.model import Aeroport
from src.views.view import view
from src.views import viewVolDetails
from src.views import viewFormVol
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
        self.dict_vol = {}

    def init_widget(self):
        self.init_header()

        dict_vol = {}
        vols = db.Flight.get_all()
        self.label_nb_annonces = vtk.Label(self, self.font_style("label"),
                                           text=f"{len(vols)} vols disponibles")
        self.label_nb_annonces.grid(column=0, row=2, pady=10, padx=10)

        self.listbox = vtk.Listbox(self, selectmode=vtk.SINGLE, width=100,
                                   height=10, font=self.font_style("subtitle"))
        self.listbox.bind('<ButtonRelease-1>',
                          lambda event: self.details(self.listbox, event,
                                                     dict_vol))
        self.listbox.grid(column=0, row=3, columnspan=5, pady=10, padx=10)
        vols = [vols for vols in vols if vols.DepartureDate.date()
                >= datetime.date.today()]
        for index, vol in enumerate(vols):
            dict_vol[index] = vol
            self.listbox.insert(vtk.END, vol)

        if (self.controller.is_connected and
                self.controller.userConnected.flightCompanyId is not None):
            button_add_vol = vtk.Button(self, self.button_style(),
                                        text="Ajouter un vol",
                                        command=self.add_vol)
            button_add_vol.grid(column=1, row=4, pady=10, padx=10)

        frame_filter = vtk.Frame(self, relief=vtk.GROOVE, borderwidth=2)
        frame_filter.grid(column=4, row=3, pady=10, padx=10, rowspan=5,
                          columnspan=5)
        label_filter = vtk.Label(frame_filter, self.font_style("subtitle"),
                                 text="Filtrer les vols")
        label_filter.grid(column=1, row=1, pady=10, padx=10)

        label_depart = vtk.Label(frame_filter, self.font_style("label"),
                                 text="Départ")
        label_depart.grid(column=0, row=2, pady=10, padx=10)

        combo_depart = ttk.Combobox(frame_filter, values=Aeroport.get_all())
        combo_depart.grid(column=1, row=2, pady=10, padx=10)

        label_arrivee = vtk.Label(frame_filter, self.font_style("label"),
                                  text="Arrivée")
        label_arrivee.grid(column=0, row=3, pady=10, padx=10)

        combo_arrivee = ttk.Combobox(frame_filter, values=Aeroport.get_all())
        combo_arrivee.grid(column=1, row=3, pady=10, padx=10)

        calendar = DateEntry(frame_filter, font=self.font_style("label"))
        calendar.grid(column=1, row=4, pady=10, padx=10)
        calendar.set_date(None)

        button_filter = vtk.Button(frame_filter, self.button_style(),
                                   text="Filtrer", command=lambda: self.filter(
                combo_depart.get(), combo_arrivee.get(), calendar.get_date()
            ))
        button_filter.grid(column=1, row=5, pady=10, padx=10)

    def filter(self, depart: str, arrivee: str, date: datetime.date):
        flights = db.Flight.get_all()
        if depart != "":
            flights = [flight for flight in flights if
                       db.Aeroport.get_by_id(flight.idDepartureAeroport)
                       .nomAeroport in depart]
        if arrivee != "":
            flights = [flight for flight in flights if
                       db.Aeroport.get_by_id(flight.idArrivalAeroport)
                       .nomAeroport in depart]
        if date != "":
            flights = [flight for flight in flights if
                       date == flight.DepartureDate.date()]
        self.listbox.delete(0, vtk.END)
        self.dict_vol = {}
        for index, vol in enumerate(flights):
            self.dict_vol[index] = vol

            self.listbox.insert(vtk.END, vol)
        self.listbox.update()
        self.update()
        self.update_idletasks()

    def details(self, listbox, event, dict_vol: dict):
        selected_index = listbox.nearest(event.y)
        if selected_index != -1:
            self.controller.show_frame(
                viewVolDetails.viewVolDetails)
            (self.controller.frames[viewVolDetails.viewVolDetails]
             .change_data(dict_vol[selected_index]))

    def add_vol(self):
        self.controller.show_frame(viewFormVol.viewFormVol)
        (self.controller.frames[viewFormVol.viewFormVol]
         .change_data(None))
