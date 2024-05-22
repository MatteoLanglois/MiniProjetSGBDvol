from sqlalchemy import *
from sqlalchemy.orm import *
from src.model import base, session, Aeroport

from typing import List
from datetime import datetime


class Flight(base):
    __tablename__ = "flights"
    idFlight = Column(Integer, primary_key=True)
    Price = Column(Float)
    DepartureDate = Column(DateTime)
    ArrivalDate = Column(DateTime)
    PlaneName = Column(String(50))
    FightCapacity = Column(Integer)
    idFlightCompany = Column(Integer, ForeignKey('flightcompanies.idFlightCompany'))
    idDepartureAeroport = Column(Integer, ForeignKey('aeroports.idAeroport'))
    idArrivalAeroport = Column(Integer, ForeignKey('aeroports.idAeroport'))

    flightcompany = relationship('FlightCompany', backref='flightcompany')
    departure_aeroport = relationship('Aeroport', backref='departure_aeroport', foreign_keys='Flight.idDepartureAeroport')
    arrival_aeroport = relationship('Aeroport', backref='arrival_aeroport', foreign_keys='Flight.idArrivalAeroport')

    def __init__(self, Price, DepartureDate, ArrivalDate, PlaneName, FlightCapacity, idFlightCompany, idDepartureAeroport, idArrivalAeroport, **kw: Any):
        super().__init__(**kw)
        self.Price = Price
        self.DepartureDate = DepartureDate
        self.ArrivalDate = ArrivalDate
        self.PlaneName = PlaneName
        self.FightCapacity = FlightCapacity
        self.idFlightCompany = idFlightCompany
        self.idDepartureAeroport = idDepartureAeroport
        self.idArrivalAeroport = idArrivalAeroport

    def __repr__(self):
        return f"<Flight {self.idFlight} {self.idDepartureAeroport} {self.idArrivalAeroport} {self.DepartureDate} {self.ArrivalDate}>"

    def __str__(self):
        return f"Vol {self.idFlight} de {self.idDepartureAeroport} à {self.idArrivalAeroport} le {self.DepartureDate}"

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

