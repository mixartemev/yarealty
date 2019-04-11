from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Create connection
engine = create_engine('postgresql://mix:321@localhost/cian', echo=False)

# Create all not created defined tables
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
