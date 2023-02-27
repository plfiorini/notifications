#!/usr/bin/env python3

import unittest
import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from server import (
    Base,
    Customer,
    Notification,
    NotificationCounter,
    process_notification,
)


class TestNotifications(unittest.TestCase):
    def setUp(self):
        # Creo database engine e sessione
        engine = create_engine("sqlite:///:memory:", echo=True)

        # Creo le tabelle
        Base.metadata.create_all(engine)

        # Creo la sessione
        Session = sessionmaker(bind=engine)
        self.session = Session()

        # Dati di test
        self.customers = [
            Customer(name="Yvonne Nash", notification_label="Los Angeles"),
            Customer(name="Justin Wright", notification_label="Jeddah"),
            Customer(name="Thomas Hamilton", notification_label="Bangkok"),
            Customer(name="Lily Lee", notification_label="Casablanca"),
            Customer(name="Angela Davies", notification_label="Addis Ababa"),
            Customer(name="Dan Skinner", notification_label="Lahore"),
            Customer(name="Dylan Butler", notification_label="Kinshasa"),
            Customer(name="Carl Reid", notification_label="Dhaka"),
            Customer(name="Jasmine Rampling", notification_label="Karachi"),
            Customer(name="Amelia Ross", notification_label="Abidjan"),
        ]
        self.session.add_all(self.customers)
        self.session.commit()

    def tearDown(self):
        self.session.rollback()
        self.session.close()

    # Test di una notifica valida
    def test_valid_notification(self):
        notification_text = "Sono una notifica da Dhaka"
        process_notification(notification_text, self.session)
        notifications = self.session.query(Notification)
        self.assertEqual(notifications.count(), 1)
        notification = notifications.one()
        self.assertEqual(notification.body, "Sono una notifica da Dhaka")
        self.assertEqual(notification.customer.notification_label, "Dhaka")
        notification_counter = (
            self.session.query(NotificationCounter)
            .filter_by(id_customer=notification.customer.id, day=datetime.date.today())
            .one()
        )
        self.assertEqual(notification_counter.num, 1)

    # Test di una notifica con una label che non corrisponde ad alcun cliente
    def test_no_customer(self):
        notification_text = "Sono una notifica da Tokyo"
        process_notification(notification_text, self.session)
        notifications = self.session.query(Notification).filter(
            Notification.body == notification_text
        )
        self.assertEqual(notifications.count(), 1)
        notification = notifications.one()
        self.assertIsNone(notification.customer)

    # Test di una notifica con label multiple
    def test_multiple_labels(self):
        notification_text = "Sono una notifica da Los Angeles e Casablanca"
        process_notification(notification_text, self.session)
        notifications = self.session.query(Notification).filter(
            Notification.body == notification_text
        )
        self.assertEqual(notifications.count(), 1)
        notification = notifications.one()
        self.assertIsNone(notification.customer)


if __name__ == "__main__":
    unittest.main()
