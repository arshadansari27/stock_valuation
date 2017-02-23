"""
Unit test for services
"""


import unittest
from datetime import datetime
from application.models import Transaction, \
        Instrument
from application.services import AverageValuationProcessor, \
        FIFOValuationProcessor
from application.repositories.interfaces import InstrumentRepository
# from application.repositories import TransactionRepository


class ValuationProcessorTest(unittest.TestCase):
    """
    Valuation Processor Test for AverageValuationProcessor and 
    FIFOValuationProcessor
    """

    def setUp(self):
        context = {}
        context['TransactionRepository'] = None  # FakeTransactionRepository
        context['InstrumentRepository'] = FakeInstrumentRepository()
        self.context = context

        self.transactions = [
            Transaction(1, 1, 1, 'BUY', 50, 116, datetime(2017, 1, 1)),
            Transaction(2, 1, 1, 'BUY', 50, 120, datetime(2017, 1, 15)),
            Transaction(3, 1, 1, 'SELL', 80, 128, datetime(2017, 2, 1)),
            Transaction(4, 2, 1, 'BUY', 50, 800, datetime(2017, 2, 1)),
            Transaction(5, 2, 1, 'BUY', 10, 810, datetime(2017, 2, 7))
        ]

    def test_average_valuation(self):
        value = AverageValuationProcessor()(self.context, 
                                            self.transactions)
        print value
        assert "%.2f" % value == "620.75"
    
    def test_fifo_valuation(self):
        value = FIFOValuationProcessor()(self.context, 
                                         self.transactions)
        print 'FIFO', value



class FakeInstrumentRepository(InstrumentRepository):

    def get_by_id(self, instrument_id):
        if instrument_id is 1:
            return (1, 'APPL', 'Apple Pvt. Ltd.', 136),
        else:
            return (2, 'GOOG', 'Google Pvt. Ltd.', 849)

    def get_by_ids(self, instrument_ids):
        return [
            (1, 'APPL', 'Apple Pvt. Ltd.', 136),
            (2, 'GOOG', 'Google Pvt. Ltd.', 849)
        ]


'''
class FakeTransactionRepository(TransactionRepository):

    def get_by_id(self, transaction_id):
        return (transaction_id, 1,
                           1, 'BUY', 10, 10, datetime.now())

    def get_by_ids(self, transaction_ids):
        return [(u, 1, 1,
                            'BUY' if u % 2 is 0 else 'SELL',
                            10, 10, datetime.now()) 
                for u in transaction_ids]

    def get_by_user_id(self, user_id):
        return [(u, 1, user_id,
                            'BUY' if u % 2 is 0 else 'SELL',
                            10, 10, datetime.now()) 
                for u in range(1, 11)]
'''
