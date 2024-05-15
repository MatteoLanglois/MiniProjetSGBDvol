from sqlalchemy import *
from sqlalchemy.orm import *


base = declarative_base()
engine = create_engine(
    "mysql+mysqlconnector://ben:aPykoGl70OtTNUsI@les"
    "-roseaux.dev/vol")
Session = sessionmaker(bind=engine)
session = Session()

base.metadata.create_all(engine)

from src.model.Vol import Vol
from src.model.User import User