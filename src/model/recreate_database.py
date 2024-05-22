from sqlalchemy import *
from sqlalchemy.orm import *
from typing import List

base = declarative_base()

class Aeroport(base):
    __tablename__ = 'Airport'
    idAeroport = Column(Integer, primary_key=True)
    nomAeroport = Column(String(255))
    villeAeroport = Column(String(255))

class User(base):
    __tablename__ = 'User'
    idUser = Column(Integer, primary_key=True)
    prenomUser = Column(String(50))
    nomUser = Column(String(50))
    mailUser = Column(String(50))
    mdpUser = Column(String(255))
    flightCompanyId = Column(Integer,
                           ForeignKey('FlightCompany.idFlightCompany'),
                           nullable=True)

    flightcompany = relationship('FlightCompany', backref='flightcompany')

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

    flightcompany = relationship('FlightCompany', backref='flightcompany')
    departure_aeroport = relationship('Aeroport', backref='departure_aeroport', foreign_keys='Flight.idDepartureAeroport')
    arrival_aeroport = relationship('Aeroport', backref='arrival_aeroport', foreign_keys='Flight.idArrivalAeroport')


class FlightCompany(base):
    __tablename__ = 'FlightCompany'
    idFlightCompany = Column(Integer, primary_key=True)
    nameFlightCompany = Column(String(255))

class Reservation(base):
    __tablename__ = 'Reservation'
    idUser = Column(Integer, ForeignKey('User.idUser'), primary_key=True)
    idFlight = Column(Integer, ForeignKey('Flight.idFlight'), primary_key=True)
    ReservationDate = Column(DateTime)

    user = relationship('User', backref='user')
    flight = relationship('Flight', backref='flight')

engine = create_engine(
    "mysql+mysqlconnector://ben:aPykoGl70OtTNUsI@les"
    "-roseaux.dev/vol")
Session = sessionmaker(bind=engine)
session = Session()
base.metadata.create_all(engine)
