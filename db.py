from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Create connection
# engine = create_engine('postgresql://mixartemev:mixfixX98@95.163.209.94/Postgres-mc', echo=False)
engine = create_engine('mysql+mysqlconnector://mixartemev:mixfixX98@old.mcity.ru/cian', echo=False)
# Base.metadata.schema = 'cian'
# Create all not created defined tables
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)  # , autoflush=False)
session = Session()
