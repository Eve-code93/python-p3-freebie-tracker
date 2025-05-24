from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    founding_year = Column(Integer)

    # One-to-many: Company to Freebies
    freebies = relationship("Freebie", back_populates="company")

    # Many-to-many (via freebies): Company to Devs who collected freebies
    devs = relationship("Dev", secondary="freebies", viewonly=True)

    def give_freebie(self, dev, item_name, value):
        """
        Create a new Freebie for the dev associated with this company.
        Note: Caller is responsible for adding and committing the session.
        """
        freebie = Freebie(item_name=item_name, value=value, dev=dev, company=self)
        return freebie

    @classmethod
    def oldest_company(cls, session):
        """
        Returns the Company instance with the earliest founding year.
        """
        return session.query(cls).order_by(cls.founding_year).first()

    def __repr__(self):
        return f"<Company(id={self.id}, name={self.name}, founding_year={self.founding_year})>"


class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    # One-to-many: Dev to Freebies
    freebies = relationship("Freebie", back_populates="dev")

    # Many-to-many (via freebies): Dev to Companies who gave freebies
    companies = relationship("Company", secondary="freebies", viewonly=True)

    def received_one(self, item_name):
        """
        Returns True if the dev has received a freebie with the given item_name.
        """
        return any(freebie.item_name == item_name for freebie in self.freebies)

    def give_away(self, other_dev, freebie):
        """
        Transfer ownership of a freebie to another dev,
        only if this dev currently owns it.
        Returns True if successful, False otherwise.
        """
        if freebie.dev == self:
            freebie.dev = other_dev
            return True
        return False

    def __repr__(self):
        return f"<Dev(id={self.id}, name={self.name})>"


class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer, primary_key=True)
    item_name = Column(String)
    value = Column(Integer)

    dev_id = Column(Integer, ForeignKey('devs.id'))
    company_id = Column(Integer, ForeignKey('companies.id'))

    # Many-to-one: Freebie to Dev and Company
    dev = relationship("Dev", back_populates="freebies")
    company = relationship("Company", back_populates="freebies")

    def print_details(self):
        """
        Returns a formatted string describing the freebie ownership.
        """
        return f"{self.dev.name} owns a {self.item_name} from {self.company.name}"

    def __repr__(self):
        return (f"<Freebie(id={self.id}, item_name={self.item_name}, value={self.value}, "
                f"dev_id={self.dev_id}, company_id={self.company_id})>")
