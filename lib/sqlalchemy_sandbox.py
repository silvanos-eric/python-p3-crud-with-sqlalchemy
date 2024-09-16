#!/usr/bin/env python3

from datetime import datetime

from sqlalchemy import (create_engine, desc, func, CheckConstraint,
                        PrimaryKeyConstraint, UniqueConstraint, Index, Column,
                        DateTime, Integer, String)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Student(Base):
    __tablename__ = 'students'
    __table_args__ = (PrimaryKeyConstraint('id', name='id_pk'),
                      UniqueConstraint('email', name='unique_email'),
                      CheckConstraint('grade BETWEEN 1 AND 12',
                                      name='grade_between_1_and_12'))

    Index('index_name', 'name')

    id = Column(Integer())
    name = Column(String())
    email = Column(String(55))
    grade = Column(Integer())
    birthday = Column(DateTime())
    enrolled_date = Column(DateTime(), default=datetime.now())

    id = Column(Integer(), primary_key=True)
    name = Column(String())

    def __repr__(self):
        return f"Student {self.id}: " \
            + f"{self.name}, " \
                + f"Grade {self.grade}"


if __name__ == '__main__':
    # Connect to database
    engine = create_engine('sqlite:///:memory:')
    # Create relation equivalent of class models
    Base.metadata.create_all(engine)

    # use our engine to configure a 'Session' class
    Session = sessionmaker(bind=engine)

    # use 'Session' class to create 'session' object
    session = Session()

    # Create a new model instance
    albert_einstein = Student(name="Albert Einstein",
                              email="alber.einstein@zurich.edu",
                              grade=6,
                              birthday=datetime(year=1979, month=3, day=14))

    # Create another model class instance
    alan_turing = Student(name="Alan Turing",
                          email="alan.turing@sherbone.edu",
                          grade=11,
                          birthday=datetime(year=1912, month=6, day=23))

    session.bulk_save_objects([albert_einstein, alan_turing])
    session.commit()

    print(f"New Student ID is {albert_einstein.id}")
    print(f"New Student ID is {alan_turing.id}")
