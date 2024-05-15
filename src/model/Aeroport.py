from typing import List

from sqlalchemy import *
from sqlalchemy.orm import *
from src.model import base, session


class Aeroport(base):
    __tablename__ = 'aeroports'
    idAeroport = Column(Integer, primary_key=True)
    nomAeroport = Column(String(255))
    villeAeroport = Column(String(255))

    def __init__(self, nomAeroport, villeAeroport, **kw: Any):
        super().__init__(**kw)
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