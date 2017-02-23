"""
Unit test for mysql instrument repository
"""


import unittest
import MySQLdb
import random
from datetime import datetime
from application.repositories.mysql_repositories import \
        MySqlInstrumentRepository, MySqlTransactionRepository


class MySqlInstrumentRepositoryTest(unittest.TestCase):
    """
    Instrument Repository TestCase
    """

    def setUp(self):

        instrument_id = int(random.random() * 1000)
        self.instrument_id = instrument_id

        self.conn = MySQLdb.connect(host='localhost', port=3306, user='root',
                                    passwd='password', db='stock_tests')
        self.repository = MySqlInstrumentRepository(self.conn)

        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO Instrument (ID,  Ticker, Name, Current_Price) "
            "VALUES ({}, '{}', '{}', '{}')".format(instrument_id, 'GOOGL',
                                                   'Google Inc', 10.0))

        cur.execute("INSERT INTO Instrument (ID, Ticker, Name, Current_Price) "
                    "VALUES ({}, '{}', '{}', '{}')".format(instrument_id + 1,
                                                           'APPL',
                                                           'Apple Pvt. Ltd.',
                                                           10.0))
        cur.close()
        self.conn.commit()

    def test_get_by_id(self):
        instrument = self.repository.get_by_id(self.instrument_id)
        assert instrument[0] == self.instrument_id

    def test_get_by_ids(self):
        instruments = self.repository.get_by_ids([self.instrument_id,
                                                  self.instrument_id + 1])
        assert len(instruments) >= 2

    def tearDown(self):
        cur = self.conn.cursor()
        cur.execute("DELETE FROM Transaction")
        cur.execute("DELETE FROM Instrument")
        cur.close()
        self.conn.commit()
        self.conn.close()


class MySqlTransactionRespoistoryTest(unittest.TestCase):
    """
    Transaction Repository TestCase
    """

    def setUp(self):
        self.conn = MySQLdb.connect(host='localhost', port=3306, user='root',
                                    passwd='password', db='stock_tests')
        self.repository = MySqlTransactionRepository(self.conn)

        cur = self.conn.cursor()
        instrument_id = int(random.random() * 1000)
        instruments = [
            (instrument_id, 'GOOGL', 'Google Inc', 10.0),
            (instrument_id + 1, 'APPL', 'Apple Pvt. Ltd.', 10.0)
        ]
        for instrument in instruments:
            sql = "INSERT INTO Instrument " + \
                    "(ID,  Ticker, Name, Current_Price) " + \
                    "values ({}, '{}', '{}', {})"
            print sql.format(*instrument)
            cur.execute(sql.format(*instrument))

        sql = "INSERT INTO Transaction " + \
            "(ID, Position_Id, User_ID, Buy_or_Sell, " + \
            "Quantity, Price, Date) VALUES " + \
            "({}, {}, {}, '{}', {}, {}, '{}')"
        self.transaction_ids = []
        for i in range(1, 11):
            transaction_id = int(random.random() * 1000)
            self.transaction_id = transaction_id
            _instrument_id = (instrument_id + 1
                              if (i % 2) is 0 else instrument_id)
            buy_or_sell = 'BUY' if random.random() * 10 > 5 else 'SELL'
            quantity = int(random.random() * 100)
            price = float(10 * i % 10 + 10)
            date = str(datetime.now())
            transaction = (transaction_id, _instrument_id, 1, buy_or_sell,
                           quantity, price, date)
            sql.format(*transaction)
            cur.execute(sql.format(*transaction))
            self.transaction_ids.append(transaction_id)
        print("Collected Txns", self.transaction_ids)
        cur.close()
        self.conn.commit()

    def test_get_by_id(self):
        """ Test Transaction Get By ID """
        print(self.repository.get_by_id(self.transaction_id))

    def test_get_by_user_id(self):
        """ Test Transaction Get By User_ID """
        print(list(self.repository.get_by_user_id(1)))

    def test_get_by_ids(self):
        transactions = self.repository.get_by_ids(self.transaction_ids)
        print 'LEN', len(transactions), len(self.transaction_ids)

    def tearDown(self):
        cur = self.conn.cursor()
        print("Running TearDown")
        cur.execute("DELETE FROM Transaction")
        cur.execute("DELETE FROM Instrument")
        cur.close()
        self.conn.commit()
        self.conn.close()


if __name__ == '__main__':
    unittest.main()
