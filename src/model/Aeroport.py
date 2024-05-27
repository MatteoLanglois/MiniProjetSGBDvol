from typing import List

from sqlalchemy import *
from sqlalchemy.orm import *
from src.model import base, session


class Aeroport(base):
    __tablename__ = 'Airport'
    idAeroport = Column(Integer, primary_key=True)
    nomAeroport = Column(String(255))
    villeAeroport = Column(String(255))

    def __init__(self, nomAeroport, villeAeroport, **kw: Any):
        super().__init__(**kw)
        if not session.query(Aeroport).filter(Aeroport.nomAeroport == nomAeroport).filter(Aeroport.villeAeroport == villeAeroport).first() is None:
            raise ValueError("Aeroport already exists")

        self.nomAeroport = nomAeroport
        self.villeAeroport = villeAeroport

    def __repr__(self):
        return f"<Aeroport {self.nomAeroport} {self.villeAeroport}>"

    def __str__(self):
        return f"Aéroport {self.nomAeroport} de {self.villeAeroport}"

    @staticmethod
    def get_by_id(idAeroport: int) -> 'Aeroport':
        return session.query(Aeroport).filter(Aeroport.idAeroport == idAeroport).first()

    @staticmethod
    def get_all() -> List['Aeroport']:
        return session.query(Aeroport).all()

    @staticmethod
    def get_by_name(nomAeroport: str) -> 'Aeroport':
        return session.query(Aeroport).filter(Aeroport.nomAeroport == nomAeroport).first()