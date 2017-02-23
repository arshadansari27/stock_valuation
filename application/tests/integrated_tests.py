"""
Integration test for services
"""


import MySQLdb
import unittest
from datetime import datetime
from application.models import Transaction, \
        Instrument
from application.services import AverageValuationProcessor, \
        FIFOValuationProcessor
from application.repositories.interfaces import InstrumentRepository
from application.services import UserTransactionsListing
from application.repositories import RepositoryFactory


class UserTransactionsListingTest(unittest.TestCase):
    """
    """

    def setUp(self):
        self.conn = MySQLdb.connect(host='localhost', port=3306, user='root',
                                    passwd='password', db='stock_tests')

        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO Instrument (ID,  Ticker, Name, Current_Price) "
            "VALUES ({}, '{}', '{}', '{}')".format(30010, 'GOOGL',
                                                   'Google', 849.0))

        cur.execute("INSERT INTO Instrument (ID, Ticker, Name, Current_Price) "
                    "VALUES ({}, '{}', '{}', '{}')".format(30012,
                                                           'APPL',
                                                           'Apple',
                                                           136.0))
        sql = "INSERT INTO Transaction " + \
            "(ID, Position_Id, User_ID, Buy_or_Sell, " + \
            "Quantity, Price, Date) VALUES " + \
            "({}, {}, {}, '{}', {}, {}, '{}')"

        transactions = [
            (1, 30012, 1, 'BUY', 50, 116, datetime(2017, 1, 1)),
            (2, 30012, 1, 'BUY', 50, 120, datetime(2017, 1, 15)),
            (3, 30012, 1, 'SELL', 80, 128, datetime(2017, 2, 1)),
            (4, 30010, 1, 'BUY', 50, 800, datetime(2017, 2, 1)),
            (5, 30010, 1, 'BUY', 10, 810, datetime(2017, 2, 7))
        ]
        for transaction in transactions:
            print sql.format(*transaction)
            cur.execute(sql.format(*transaction))
        cur.close()
        self.conn.commit()

    def test_service_user_listing(self):
        context = RepositoryFactory.factory({
            'host': 'localhost',
            'port': 3306,
            'user': 'root',
            'password': 'password',
            'db': 'stock_tests'
        }, 'mysql')
        UserTransactionsListing().handle(context, 1)

    def tearDown(self):
        cur = self.conn.cursor()
        print("Running TearDown")
        cur.execute("DELETE FROM Transaction")
        cur.execute("DELETE FROM Instrument")
        cur.close()
        self.conn.commit()
        self.conn.close()
