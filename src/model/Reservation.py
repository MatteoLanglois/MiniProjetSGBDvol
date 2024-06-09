from sqlalchemy import *
from sqlalchemy.orm import *
from src.model import base, session, User

from typing import List
from datetime import datetime


class Reservation(base):
    __tablename__ = 'Reservation'
    idUser = Column(Integer, ForeignKey('User.idUser'), primary_key=True)
    idFlight = Column(Integer, ForeignKey('Flight.idFlight'), primary_key=True)
    ReservationDate = Column(DateTime)

    user = relationship('User', backref='user')
    flight = relationship('Flight', backref='flight')

    def __init__(self, idUser, idFlight, **kw: Any):
        import src.model as db
        if not db.Flight.get_by_id(idFlight):
            raise ValueError("Flight does not exist")
        if session.query(Reservation).filter(
                Reservation.idUser == idUser).filter(
                Reservation.idFlight == idFlight).first():
            raise ValueError("Reservation already exists")
        if db.Flight.get_by_id(idFlight).DepartureDate < datetime.now():
            raise ValueError("Flight has already left")

        super().__init__(**kw)
        self.idUser = idUser
        self.idFlight = idFlight
        self.ReservationDate = datetime.now()

    def __repr__(self):
        return f"<Reservation {self.idUser} {self.idFlight}>"

    def __str__(self):
        return f"Réservation {self.idUser} {self.idFlight}"

    def print(self):
        import src.model as db
        flight = db.Flight.get_by_id(self.idFlight)
        return (f"{flight.DepartureDate} : "
                f"{db.Aeroport.get_by_id(flight.idArrivalAeroport)} - "
                f"{db.Aeroport.get_by_id(flight.idArrivalAeroport)}")

    @staticmethod
    def get_by_user(idUser: int) -> List['Reservation']:
        return session.query(Reservation).filter(
            Reservation.idUser == idUser).all()

    @staticmethod
    def get_all() -> List['Reservation']:
        return session.query(Reservation).all()

    @staticmethod
    def get_by_flight(idFlight: int) -> List['Reservation']:
        return session.query(Reservation).filter(
            Reservation.idFlight == idFlight).all()
