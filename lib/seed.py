# lib/seed.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from lib.models import Base, Company, Dev, Freebie  # same folder, so direct import

def seed():
    engine = create_engine('sqlite:///freebies.db', echo=True)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    # Clear existing data (optional)
    session.query(Freebie).delete()
    session.query(Dev).delete()
    session.query(Company).delete()
    session.commit()

    # Create companies
    company1 = Company(name="TechCorp", founding_year=1990)
    company2 = Company(name="InnovateLLC", founding_year=1985)

    # Create devs
    dev1 = Dev(name="Alice")
    dev2 = Dev(name="Bob")
    dev3 = Dev(name="Charlie")

    session.add_all([company1, company2, dev1, dev2, dev3])
    session.commit()

    # Add freebies
    freebie1 = company1.give_freebie(dev1, "Sticker", 5)
    freebie2 = company1.give_freebie(dev2, "Mug", 10)
    freebie3 = company2.give_freebie(dev1, "T-Shirt", 20)
    freebie4 = company2.give_freebie(dev3, "Backpack", 50)

    session.add_all([freebie1, freebie2, freebie3, freebie4])
    session.commit()

    session.close()
    print("Seed data inserted successfully!")

if __name__ == '__main__':
    seed()
# This script seeds the database with initial data for testing purposes.
# It creates two companies, three developers, and several freebies.
# It also clears existing data before inserting new records.