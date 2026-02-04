from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

URL_DATABASE = 'postgresql://postgres:localdb%402026@localhost:5432/QuizApp'

engine = create_engine(URL_DATABASE)

sessionlocal = sessionmaker(autocommit= False, autoflush= False, bind= engine)

Base = declarative_base()