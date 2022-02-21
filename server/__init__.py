import datetime
import logging

from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship, declarative_base

__ALL__ = (
    'Base',
    'Customer',
    'Notification',
    'NotificationCounter',
    'process_notification',
)


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')

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


def find_customer_id(session, notification_text):
    logging.info(f"Ricerca del cliente per la notifica '{notification_text}'")
    notification_labels = [c.notification_label for c in session.query(Customer).all()]
    labels = [l for l in notification_labels if l.lower() in notification_text.lower()]
    logging.debug(f'Labels: {labels}')
    if len(labels) > 1:
        logging.debug(f"Notifica con tante label: {labels}")
        id_customer = None
    elif len(labels) == 1:
        customer = session.query(Customer).filter(Customer.notification_label.ilike(labels[0])).first()
        id_customer = customer.id
        logging.debug(f"Cliente '{customer.name}' trovato con label '{labels[0]}' per la notifica '{notification_text}'")
    else:
        logging.warning(f"Nessun cliente trovato per la notifica '{notification_text}'")
        id_customer = None
    return id_customer


def process_notification(notification_text, session):
    # Cerco l'ID cliente in base alla/alle label eventualmente presenti
    # nel messaggio
    id_customer = find_customer_id(session, notification_text)
    # Aggiungo la notifica
    session.add(Notification(body=notification_text, id_customer=id_customer))
    # Incremento il contatore del cliente
    if id_customer is not None:
        query = session.query(NotificationCounter).filter_by(
            id_customer=id_customer, day=datetime.date.today())
        if query.count() == 0:
            session.add(NotificationCounter(id_customer=id_customer, day=datetime.date.today(), num=1))
        else:
            query.update({'num': NotificationCounter.num + 1})
