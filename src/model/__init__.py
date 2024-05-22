from sqlalchemy import *
from sqlalchemy.orm import *
from typing import List

base = declarative_base()


class User(base):
    __tablename__ = 'users'
    idUser = Column(Integer, primary_key=True)
    prenomUser = Column(String(50))
    nomUser = Column(String(50))
    mailUser = Column(String(50))
    mdpUser = Column(String(255))
    flightCompany = Column(Integer,
                           ForeignKey('flightcompanies.idFlightCompany'),
                           nullable=True)

    flightcompany = relationship('FlightCompany', backref='flightcompany')


engine = create_engine(
    "mysql+mysqlconnector://ben:aPykoGl70OtTNUsI@les"
    "-roseaux.dev/vol")
Session = sessionmaker(bind=engine)
session = Session()
base.metadata.create_all(engine)
"""
from src.model.Flight import Flight
from src.model.User import User
from src.model.Aeroport import Aeroport
from src.model.FlightCompany import FlightCompany
from src.model.Reservation import Reservation
"""
