from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship, declarative_base

__ALL__ = (
    'Base',
    'Customer',
    'Notification',
    'NotificationCounter',
    'process_notification',
)


# Base per l'ORM
Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    notification_label = Column(String, nullable=False, unique=True)

class Notification(Base):
    __tablename__ = 'notifications'

    id = Column(Integer, primary_key=True, autoincrement=True)
    body = Column(String, nullable=False)
    id_customer = Column(Integer, ForeignKey('customers.id'))
    customer = relationship('Customer')

class NotificationCounter(Base):
    __tablename__ = 'notification_counters'

    # SQLAlchemy vuole per forza una primary key: metto un campo ID autoincrementale
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_customer = Column(Integer, ForeignKey('customers.id'), nullable=False)
    num = Column(Integer, nullable=False, default=0)
    day = Column(Date, nullable=False)
    customer = relationship('Customer')


def process_notification(notification_text, session):
    pass
