from sqlalchemy import *
from sqlalchemy.orm import *
from src.model import base, session, Aeroport, Reservation

from typing import List
from datetime import datetime


class Flight(base):
    __tablename__ = "Flight"
    idFlight = Column(Integer, primary_key=True)
    Price = Column(Float)
    DepartureDate = Column(DateTime)
    ArrivalDate = Column(DateTime)
    PlaneName = Column(String(50))
    FightCapacity = Column(Integer)
    idFlightCompany = Column(Integer, ForeignKey('FlightCompany.idFlightCompany'))
    idDepartureAeroport = Column(Integer, ForeignKey('Airport.idAeroport'))
    idArrivalAeroport = Column(Integer, ForeignKey('Airport.idAeroport'))

    flight_flightcompany = relationship('FlightCompany', backref='flight_flightcompany')
    departure_aeroport = relationship('Aeroport', backref='departure_aeroport', foreign_keys='Flight.idDepartureAeroport')
    arrival_aeroport = relationship('Aeroport', backref='arrival_aeroport', foreign_keys='Flight.idArrivalAeroport')

    def __init__(self, Price, DepartureDate, ArrivalDate, PlaneName,
                 FlightCapacity, idFlightCompany, idDepartureAeroport,
                 idArrivalAeroport, **kw: Any):
        super().__init__(**kw)
        if DepartureDate >= ArrivalDate:
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

    def __repr__(self):
        return (f"<Flight {self.idFlight} {self.idDepartureAeroport} "
                f"{self.idArrivalAeroport} {self.DepartureDate} "
                f"{self.ArrivalDate}>")

    def __str__(self):
        return (f"Vol {self.idFlight} de {self.idDepartureAeroport} à "
                f"{self.idArrivalAeroport} le {self.DepartureDate}")

    def print(self):
        return (f"{self.idDepartureAeroport} : {self.DepartureDate} - "
                f"{self.idArrivalAeroport} ")

    @staticmethod
    def get_by_id(idFlight: int) -> 'Flight':
        return session.query(Flight).filter(Flight.idFlight == idFlight).first()

    @staticmethod
    def get_all() -> List['Flight']:
        return session.query(Flight).all()

    @staticmethod
    def get_departure_airport(idFlight: int) -> 'Aeroport':
        return session.query(Aeroport).join(Flight).filter(Flight.idDepartureAeroport == Aeroport.idAeroport).filter(Flight.idFlight == idFlight).first()

    @staticmethod
    def get_arrival_airport(idFlight: int) -> 'Aeroport':
        return session.query(Aeroport).join(Flight).filter(Flight.idArrivalAeroport == Aeroport.idAeroport).filter(Flight.idFlight == idFlight).first()

    @staticmethod
    def get_flights_by_departure_airport(idDepartureAeroport: int) -> List['Flight']:
        return session.query(Flight).filter(Flight.idDepartureAeroport == idDepartureAeroport).all()

    @staticmethod
    def get_flights_by_arrival_airport(idArrivalAeroport: int) -> List['Flight']:
        return session.query(Flight).filter(Flight.idArrivalAeroport == idArrivalAeroport).all()

    @staticmethod
    def get_flights_by_date(date: datetime) -> List['Flight']:
        return session.query(Flight).filter(Flight.DepartureDate == date).all()

    @staticmethod
    def get_flights_by_company(idFlightCompany: int) -> List['Flight']:
        return session.query(Flight).filter(Flight.idFlightCompany == idFlightCompany).all()

    @staticmethod
    def get_future_flights() -> List['Flight']:
        return session.query(Flight).filter(Flight.DepartureDate >= datetime.now()).all()

    @staticmethod
    def get_flight_under_price(price: float) -> List['Flight']:
        return session.query(Flight).filter(Flight.Price <= price).all()

    @staticmethod
    def get_flight_departure_arrival_airport(idDepartureAeroport: int, idArrivalAeroport: int) -> List['Flight']:
        return session.query(Flight).filter(Flight.idDepartureAeroport == idDepartureAeroport).filter(Flight.idArrivalAeroport == idArrivalAeroport).all()

    def get_reservations(self) -> List['Reservation']:
        return session.query(Reservation).filter(Reservation.idFlight == self.idFlight).all()

    def get_free_seats(self) -> int:
        return self.FightCapacity - len(self.get_reservations())

