import datetime
from tkinter import END

from src.model import FlightCompany
import tkinter as vtk
import src.model as db
from src.views.view import view
from tkcalendar import DateEntry
from tkinter import ttk
from tkinter.messagebox import showerror, showinfo
from datetime import datetime
from datetime import date
from src.model import Aeroport
from src.views import viewMain

"""
Classe viewFormVol

Vue permettant à une companie aérienne de soumettre un vol. Elle hérite de la classe view.
"""


class viewFormVol(view):
    """
    Méthode __init__

    Constructeur de la classe viewFormVol
    """
    def __init__(self, parent, controller):
        vtk.Frame.__init__(self, parent)
        self.title = "Ajouter un vol"
        self.combo_arrival_aeroport = None
        self.button_arrival_date = None
        self.combo_departure_aeroport = None
        self.entry_prix_annonce = None
        self.label_title = None
        self.entry_flight_capacity = None
        self.entry_plane_name = None
        self.button_departure_date = None

        self.price = None
        self.DepartureDate = None
        self.ArrivalDate = None
        self.PlaneName = None
        self.FlightCapacity = None
        self.idFlightCompany = None
        self.idDepartureAeroport = None
        self.idArrivalAeroport = None
        self.cal = None

        self.label_departure_date = None
        self.label_arrival_date = None

        self.controller = controller
        self.init_widget()

    def init_widget(self):
        self.init_header()

        self.label_title = vtk.Label(self, self.font_style("title"),
                                     text="Soumettre un vol")
        self.label_title.grid()

        price = vtk.DoubleVar()
        label_price = vtk.Label(self, self.font_style("label"),
                                text="Prix du billet")
        label_price.grid()
        price.set(0.0)
        self.entry_prix_annonce = vtk.Spinbox(self, from_=0.0, to=10000.0,
                                              textvariable=price)
        self.entry_prix_annonce.grid()

        label_departure_date = vtk.Label(self, self.font_style("label"),
                                         text="Date de départ")
        label_departure_date.grid()
        self.button_departure_date = vtk.Button(self, self.button_style(),
                                                text="Choisir une date de départ",
                                                command=lambda: self.entry_date(
                                                    self.label_departure_date))
        self.button_departure_date.grid()
        self.label_departure_date = vtk.Label(self, self.font_style("label"),
                                              text="")
        self.label_departure_date.grid()

        label_departure_aeroport = vtk.Label(self, self.font_style("label"),
                                             text="Aéroport de départ")
        label_departure_aeroport.grid()

        self.combo_departure_aeroport = ttk.Combobox(self, width=50)
        self.combo_departure_aeroport.grid()
        liste_aeroport = db.Aeroport.get_all()
        self.combo_departure_aeroport['values'] = liste_aeroport

        label_arrival_date = vtk.Label(self, self.font_style("label"),
                                       text="Date d'arrivée")
        label_arrival_date.grid()
        self.button_arrival_date = vtk.Button(self, self.button_style(),
                                              text="Choisir une date d'arrivée",
                                              command=lambda: self.entry_date(
                                                  self.label_arrival_date))
        self.button_arrival_date.grid()
        self.label_arrival_date = vtk.Label(self, self.font_style("label"),
                                            text="")
        self.label_arrival_date.grid()

        label_arrival_aeroport = vtk.Label(self, self.font_style("label"),
                                           text="Aéroport d'arrivée")
        label_arrival_aeroport.grid()
        self.combo_arrival_aeroport = ttk.Combobox(self, width=50)
        self.combo_arrival_aeroport.grid()
        self.combo_arrival_aeroport['values'] = liste_aeroport

        label_plane_name = vtk.Label(self, self.font_style("label"),
                                     text="Nom de l'avion")
        label_plane_name.grid()
        self.entry_plane_name = vtk.Entry(self, self.entry_style())
        self.entry_plane_name.grid()

        label_flight_capacity = vtk.Label(self, self.font_style("label"),
                                          text="Capacité de l'avion")
        label_flight_capacity.grid()
        self.entry_flight_capacity = vtk.Spinbox(self, from_=0, to=10000)
        self.entry_flight_capacity.grid()

        button_submit = vtk.Button(self, self.button_style(),
                                   text="Soumettre",
                                   command=lambda: self.submit_flight(price))
        button_submit.grid(padx=10, pady=10)

    def change_data(self, idFlightCompany):
        self.idFlightCompany = idFlightCompany

    def entry_date(self, label, time=None):
        top = vtk.Tk()
        top.title("Choisir une date")

        ttk.Label(top, text='Choisissez une date:').pack(padx=10, pady=10)
        if time is None:
            time = datetime.now()
        self.cal = DateEntry(top, width=12, background='darkblue',
                             foreground='white', borderwidth=2, day=time.day,
                             month=time.month, year=time.year)
        self.cal.pack(padx=10, pady=10)
        button = ttk.Button(top, text="Valider",
                            command=lambda: self.date_entry_launch(label, top))
        button.pack(padx=10, pady=10)

    def date_entry_launch(self, label, top):
        if self.cal.get_date() < date.today():
            showerror("Erreur",
                      "La date ne peut pas être antérieure à la date "
                      "actuelle")
            self.entry_date(label, time=self.cal.get_date())
        elif self.label_arrival_date.cget(
                "text") == "" and self.label_departure_date.cget("text") == "":
            label.config(text=self.cal.get_date())
            top.destroy()
        elif self.label_departure_date.cget(
                "text") == "" and self.cal.get_date() > datetime.strptime(
                self.label_arrival_date.cget("text"), "%Y-%m-%d").date():
            showerror("Erreur",
                      "La date de départ ne peut pas être postérieure "
                      "à la date d'arrivée")
            self.entry_date(label, time=self.cal.get_date())
        elif self.label_arrival_date.cget(
                "text") == "" and self.cal.get_date() < datetime.strptime(
                self.label_departure_date.cget("text"), "%Y-%m-%d").date():
            showerror("Erreur",
                      "La date d'arrivée ne peut pas être antérieure à "
                      "la date de départ")
        else:
            label.config(text=self.cal.get_date())
            top.destroy()

    def submit_flight(self, price_entry):
        if price_entry.get() == "":
            showerror("Erreur", "Le prix ne peut pas être vide")
            return
        price = float(round(price_entry.get(), 2))
        if self.label_departure_date.cget("text") == "":
            showerror("Erreur", "La date de départ ne peut pas "
                                "être vide")
            return
        departure_date = datetime.strptime(
            self.label_departure_date.cget("text"), "%Y-%m-%d").date()
        if self.label_arrival_date.cget("text") == "":
            showerror("Erreur", "La date d'arrivée ne peut pas "
                                "être vide")
            return
        arrival_date = datetime.strptime(self.label_arrival_date.cget("text"),
                                         "%Y-%m-%d").date()
        if self.combo_departure_aeroport.get() == "":
            showerror("Erreur", "L'aéroport de départ ne peut pas "
                                "être vide")
            return
        departure_aeroport = Aeroport.get_by_name(
            self.combo_departure_aeroport.get()).idAeroport
        if self.combo_arrival_aeroport.get() == "":
            showerror("Erreur", "L'aéroport d'arrivée ne peut pas"
                                " être vide")
            return
        arrival_aeroport = Aeroport.get_by_name(
            self.combo_arrival_aeroport.get()).idAeroport
        if self.entry_plane_name.get() == "":
            showerror("Erreur", "Le nom de l'avion ne peut pas "
                                "être vide")
            return
        plane_name = self.entry_plane_name.get()
        if self.entry_flight_capacity.get() == "":
            showerror("Erreur", "La capacité de l'avion ne peut pas "
                                "être vide")
            return
        if self.entry_flight_capacity.get() == "0":
            showerror("Erreur", "La capacité de l'avion ne peut "
                                "pas être nulle")
            return
        if int(self.entry_flight_capacity.get()) < 0:
            showerror("Erreur",
                      "La capacité de l'avion ne peut pas être "
                      "négative")
            return
        if float(self.entry_flight_capacity.get()) % 1 != 0:
            showerror("Erreur", "La capacité de l'avion doit "
                                "être un entier")
            return
        flight_capacity = int(self.entry_flight_capacity.get())

        print(price, departure_date, arrival_date, plane_name, flight_capacity,
              departure_aeroport, arrival_aeroport)

        flight = db.Flight(Price=price, DepartureDate=departure_date,
                           ArrivalDate=arrival_date, PlaneName=plane_name,
                           FlightCapacity=flight_capacity,
                           idFlightCompany=self.idFlightCompany,
                           idDepartureAeroport=departure_aeroport,
                           idArrivalAeroport=arrival_aeroport)
        db.session.add(flight)
        db.session.commit()
        showinfo("Succès", "Vol soumis avec succès")
        self.controller.show_frame(viewMain.ViewMain)
        self.controller.update()
