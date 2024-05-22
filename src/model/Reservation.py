from sqlalchemy import *
from sqlalchemy.orm import *
from src.model import base, session

from typing import List
from datetime import datetime


class Reservation(base):
    __tablename__ = 'reservations'
    idUser = Column(Integer, ForeignKey('users.idUser'), primary_key=True)
    idFlight = Column(Integer, ForeignKey('flights.idFlight'), primary_key=True)
    ReservationDate = Column(DateTime)

    user = relationship('User', backref='user')
    flight = relationship('Flight', backref='flight')

    def __init__(self, idUser, idFlight, **kw: Any):
        super().__init__(**kw)
        self.idUser = idUser
        self.idFlight = idFlight

    def __repr__(self):
        return f"<Reservation {self.idUser} {self.idFlight}>"

    def __str(self):
        return f"Réservation {self.idUser} {self.idFlight}"

    @staticmethod
    def get_by_user(idUser: int) -> List['Reservation']:
        return session.query(Reservation).filter(Reservation.idUser == idUser).all()

    @staticmethod
    def get_all() -> List['Reservation']:
        return session.query(Reservation).all()

    @staticmethod
    def get_by_flight(idFlight: int) -> List['Reservation']:
        return session.query(Reservation).filter(Reservation.idFlight == idFlight).all()

