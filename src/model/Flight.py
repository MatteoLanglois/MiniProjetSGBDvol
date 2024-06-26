from sqlalchemy import *
from sqlalchemy.orm import *
from src.model import base, session, Aeroport, Reservation
from typing import List
from datetime import datetime
from src.model.Aeroport import Aeroport

"""
Classe Flight

Cette classe permet de gérer les vols. Elle hérite de la classe base.
"""

class Flight(base):
    __tablename__ = "Flight"
    idFlight = Column(Integer, primary_key=True)
    Price = Column(Float)
    DepartureDate = Column(DateTime)
    ArrivalDate = Column(DateTime)
    PlaneName = Column(String(50))
    FightCapacity = Column(Integer)
    idFlightCompany = Column(Integer,
                             ForeignKey('FlightCompany.idFlightCompany'))
    idDepartureAeroport = Column(Integer, ForeignKey('Airport.idAeroport'))
    idArrivalAeroport = Column(Integer, ForeignKey('Airport.idAeroport'))

    flight_flightcompany = relationship('FlightCompany',
                                        backref='flight_flightcompany')
    departure_aeroport = relationship('Aeroport', backref='departure_aeroport',
                                      foreign_keys='Flight.idDepartureAeroport')
    arrival_aeroport = relationship('Aeroport', backref='arrival_aeroport',
                                    foreign_keys='Flight.idArrivalAeroport')

    allVols = []

    """
    Constructeur de la classe Flight
    
    :param Price: Prix du vol
    :param DepartureDate: Date de départ
    :param ArrivalDate: Date d'arrivée
    :param PlaneName: Nom de l'avion
    :param FlightCapacity: Capacité du vol
    :param idFlightCompany: Identifiant de la compagnie de vol
    :param idDepartureAeroport: Identifiant de l'aéroport de départ
    :param idArrivalAeroport: Identifiant de l'aéroport d'arrivée
    """
    def __init__(self, Price, DepartureDate, ArrivalDate, PlaneName,
                 FlightCapacity, idFlightCompany, idDepartureAeroport,
                 idArrivalAeroport, **kw: Any):
        super().__init__(**kw)
        if DepartureDate > ArrivalDate:
            raise ValueError("Departure date must be before arrival date")
        if Price < 0:
            raise ValueError("Price must be positive")
        if FlightCapacity <= 0:
            raise ValueError("Flight capacity must be positive")

        self.Price = Price
        self.DepartureDate = DepartureDate
        self.ArrivalDate = ArrivalDate
        self.PlaneName = PlaneName
        self.FightCapacity = FlightCapacity
        self.idFlightCompany = idFlightCompany
        self.idDepartureAeroport = idDepartureAeroport
        self.idArrivalAeroport = idArrivalAeroport

    """
    Méthode __repr__
    
    Cette méthode permet de retourner une représentation de l'objet
    """
    def __repr__(self):
        return (f"<Flight {self.idFlight} {self.idDepartureAeroport} "
                f"{self.idArrivalAeroport} {self.DepartureDate} "
                f"{self.ArrivalDate}>")

    """
    Méthode __str__
    
    Cette méthode permet de retourner une chaîne de caractères représentant
    l'objet
    """
    def __str__(self):
        return (f"{Aeroport.get_by_id(self.idDepartureAeroport).villeAeroport}"
                f" - {Aeroport.get_by_id(self.idArrivalAeroport).villeAeroport}"
                f" : {self.DepartureDate} - {self.Price}€")

    def print(self):
        depart = Aeroport.get_by_id(self.idDepartureAeroport)
        arrival = Aeroport.get_by_id(self.idArrivalAeroport)
        return (f"{depart} : {self.DepartureDate} - "
                f"{arrival} ")

    @staticmethod
    def get_by_id(idFlight: int) -> 'Flight':
        return session.query(Flight).filter(Flight.idFlight == idFlight).first()

    @staticmethod
    def get_all() -> List['Flight']:
        if len(Flight.allVols) == 0:
            Flight.allVols = session.query(Flight).all()
        return Flight.allVols

    @staticmethod
    def get_departure_airport(idFlight: int) -> 'Aeroport':
        return session.query(Aeroport).join(Flight).filter(
            Flight.idDepartureAeroport == Aeroport.idAeroport).filter(
            Flight.idFlight == idFlight).first()

    @staticmethod
    def get_arrival_airport(idFlight: int) -> 'Aeroport':
        return session.query(Aeroport).join(Flight).filter(
            Flight.idArrivalAeroport == Aeroport.idAeroport).filter(
            Flight.idFlight == idFlight).first()

    @staticmethod
    def get_flights_by_departure_airport(idDepartureAeroport: int) -> List[
        'Flight']:
        return session.query(Flight).filter(
            Flight.idDepartureAeroport == idDepartureAeroport).all()

    @staticmethod
    def get_flights_by_arrival_airport(idArrivalAeroport: int) -> List[
        'Flight']:
        return session.query(Flight).filter(
            Flight.idArrivalAeroport == idArrivalAeroport).all()

    @staticmethod
    def get_flights_by_date(date: datetime) -> List['Flight']:
        return session.query(Flight).filter(Flight.DepartureDate == date).all()

    @staticmethod
    def get_flights_by_company(idFlightCompany: int) -> List['Flight']:
        return session.query(Flight).filter(
            Flight.idFlightCompany == idFlightCompany).all()

    @staticmethod
    def get_future_flights() -> List['Flight']:
        return session.query(Flight).filter(
            Flight.DepartureDate >= datetime.now()).all()

    @staticmethod
    def get_flight_under_price(price: float) -> List['Flight']:
        return session.query(Flight).filter(Flight.Price <= price).all()

    @staticmethod
    def get_flight_departure_arrival_airport(idDepartureAeroport: int,
                                             idArrivalAeroport: int) \
            -> List['Flight']:
        return session.query(Flight).filter(
            Flight.idDepartureAeroport == idDepartureAeroport).filter(
            Flight.idArrivalAeroport == idArrivalAeroport).all()

    def get_reservations(self) -> List['Reservation']:
        return session.query(Reservation).filter(
            Reservation.idFlight == self.idFlight).all()

    def get_free_seats(self) -> int:
        return self.FightCapacity - len(self.get_reservations())
