from datetime import datetime
from typing import List

from sqlalchemy import *
from sqlalchemy.orm import *
from src.model import base, session, Flight


class FlightCompany(base):
    __tablename__ = 'FlightCompany'
    idFlightCompany = Column(Integer, primary_key=True)
    nameFlightCompany = Column(String(255))

    def __init__(self, nameFlightCompany, **kw: Any):
        super().__init__(**kw)
        self.nameFlightCompany = nameFlightCompany

    def __repr__(self):
        return f"<FlightCompany {self.nameFlightCompany}>"

    def __str__(self):
        return f"Compagnie {self.nameFlightCompany}"

    @staticmethod
    def get_by_id(idFlightCompany: int) -> 'FlightCompany':
        return session.query(FlightCompany).filter(FlightCompany.idFlightCompany == idFlightCompany).first()

    @staticmethod
    def get_all() -> List['FlightCompany']:
        return session.query(FlightCompany).all()

    def get_flights(self) -> List['Flight']:
        return session.query(Flight).filter(Flight.idFlightCompany == self.idFlightCompany).all()

    def get_future_flights(self) -> List['Flight']:
        return session.query(Flight).filter(Flight.idFlightCompany == self.idFlightCompany).filter(Flight.departureDate >= datetime.now()).all()
