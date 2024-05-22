from sqlalchemy import *
from sqlalchemy.orm import *
import bcrypt
from src.model import base, session

"""
Classe User

Cette classe permet de créer des utilisateurs
Elle contient les attributs suivants :
- idUser : int
- prenomUser : str
- nomUser : str
- mailUser : str
- mdpUser : str
"""


class User(base):
    __tablename__ = 'User'
    idUser = Column(Integer, primary_key=True)
    prenomUser = Column(String(50))
    nomUser = Column(String(50))
    mailUser = Column(String(50))
    mdpUser = Column(String(255))
    flightCompany = Column(Integer,
                           ForeignKey('FlightCompany.idFlightCompany'),
                           nullable=True)

    flightcompany = relationship('FlightCompany', backref='flightcompany')

    """
    Méthode __init__
    
    Constructeur de la classe User
    """

    def __init__(self, prenomUser, nomUser, mailUser, mdpUser, **kw: Any):
        super().__init__(**kw)
        if not session.query(User).filter(User.mailUser == mailUser).first() is None:
            raise ValueError("User already exists")

        self.prenomUser = prenomUser
        self.nomUser = nomUser
        self.mailUser = mailUser
        self.mdpUser = User.hashPassword(mdpUser)

    """
    Méthode __str__
    
    Méthode permettant d'afficher un utilisateur
    """

    def __str__(self):
        return f"{self.prenomUser} {self.nomUser}"

    """
    Méthode try_connect(mail: str, password: str)
    
    Méthode permettant de se connecter. Elle vérifie si l'utilisateur existe
    et si le mot de passe est correct.
    """

    @staticmethod
    def try_connect(mail: str, password: str) -> 'User' or None:
        user = session.query(User).filter(User.mailUser.like(mail)).first()
        if user is None:
            return None
        if bcrypt.checkpw(password.encode('utf-8'),
                          user.mdpUser.encode('utf-8')):
            return user

    """
    Méthode getByEmail(email: str)
    
    Méthode permettant de récupérer un utilisateur par son email
    """

    @staticmethod
    def getByEmail(email: str) -> 'User' or None:
        return session.query(User).filter(User.mailUser.like(email)).first()

    """
    Méthode hashPassword(password: str)
    
    Méthode permettant de hasher un mot de passe
    """

    @staticmethod
    def hashPassword(password: str) -> bytes:
        password = password.encode('utf-8')
        salt = bcrypt.gensalt()
        password = bcrypt.hashpw(password, salt)
        return password
