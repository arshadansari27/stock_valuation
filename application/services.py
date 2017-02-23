"""
Service module to handle cross model functions
"""


import abc
from collections import defaultdict
from models import Instrument, Transaction
from repositories import RepositoryFactory
from datetime import datetime


class UserTransactionsListing:
    """
    Service Class to Display and return user transaction details
    """

    def handle(self, context, user_id):
        average_valuation_processor = AverageValuationProcessor()
        fifo_valuation_processor = FIFOValuationProcessor()
        transactions = list(Transaction.fetch_by_user_id(context, user_id))
        if len(transactions) is 0:
            raise Exception("No transactions found")
        average_valuation = average_valuation_processor(context, transactions)
        fifo_valuation = fifo_valuation_processor(context, transactions)
        instruments = {}
        display_str = "%s %d %s shares at USD %.2f / share on %s"
        string_values = []
        for transaction in transactions:
            action = 'Bought' if transaction.buy_or_sell == 'BUY' else 'Sold'
            quantity = transaction.quantity
            if transaction.position_id not in instruments:
                instruments[transaction.position_id] = Instrument.fetch_by_id(
                    context, transaction.position_id).name
            company = instruments[transaction.position_id]
            price = transaction.price 
            date = transaction.date
            if type(date) == datetime:
                date = date.strftime("%d-%b-%y")
            else:
                date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")\
                        .strftime("%d-%b-%y")
            string_values.append(display_str % (action, quantity, company, 
                                                price, date))
        string_values.append("FIFO Valuation: $%.2f" % fifo_valuation)
        string_values.append(
            "Average Cost Valuation: $%.2f" % average_valuation)
        print '\n'.join(string_values)
        return string_values


class ValuationProcessor:
    """
    Interface for calculating valuation given the transactions
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def calculate(self):
        pass

    def __call__(self, context, transactions):
        assert 'TransactionRepository' in context
        assert 'InstrumentRepository' in context
        self.transaction_repository = context['TransactionRepository']
        self.instrument_repository = context['InstrumentRepository']
        self.transactions = list(transactions)
        _instrument_ids = [u.position_id for u in self.transactions]
        self.instruments = dict((u.identity, u)
                                for u in Instrument.fetch_by_ids(
                                    context,
                                    _instrument_ids))
        return self.calculate()


class AverageValuationProcessor(ValuationProcessor):

    def calculate(self):
        """
        Calculate the weighted average cost 
        TODO: Not sure what to return:
            a) the Average Value
            b) The Total Cost Worth
            So currently returning average value 
            with the assumption that is what was needed
        """
        stock_count = 0
        total_cost_worth = 0
        for transaction in self.transactions:
            quantity, price = transaction.quantity, transaction.price
            if transaction.buy_or_sell == 'BUY':
                stock_count += quantity
                total_cost_worth += (quantity * price)
            else:
                stock_count -= quantity
                total_cost_worth -= (quantity * price)
        return float(total_cost_worth) / float(stock_count)


class FIFOValuationProcessor(ValuationProcessor):

    def calculate(self):

        instrument_wise_collection = defaultdict(float)
        for instrument_id, instrument in self.instruments.iteritems():
            sold = [(u.price, u.quantity) 
                    for u in self.transactions if 
                    u.position_id == instrument_id 
                    and u.buy_or_sell == 'SELL']
            bought = [(u.price, u.quantity) 
                      for u in self.transactions if 
                      u.position_id == instrument_id 
                      and u.buy_or_sell == 'BUY']
            buy_counter = 0
            cumm_buy_quantity, cumm_buy_cost = 0, 0
            total_fifo_valuation = 0
            sell_counter = 0
            while sell_counter < len(sold):
                sell_price, sell_quantity = sold[sell_counter]
                buy_price, buy_quantity = bought[buy_counter]
                while cumm_buy_quantity + buy_quantity < sell_quantity:
                    cumm_buy_quantity += buy_quantity
                    cumm_buy_cost += (buy_quantity * buy_price)
                    buy_counter += 1
                    buy_price, buy_quantity = bought[buy_counter]

                if cumm_buy_quantity + buy_quantity > sell_quantity:
                    left = ((cumm_buy_quantity + buy_quantity) - sell_quantity)
                    bought[buy_counter] = (buy_price, left)
                    buy_quantity -= left
                    cumm_buy_quantity += buy_quantity
                    cumm_buy_cost += (buy_quantity * buy_price)
                total_fifo_valuation += ((sell_price * sell_quantity)
                                         - cumm_buy_cost)
                cumm_buy_quantity, cumm_buy_cost = 0, 0
                sell_counter += 1
            while buy_counter < len(bought):
                buy_price, buy_quantity = bought[buy_counter]
                total_fifo_valuation += (instrument.current_price *
                                         buy_quantity)
                buy_counter += 1

            instrument_wise_collection[instrument_id] = total_fifo_valuation
        print instrument_wise_collection
        return sum(v for v in instrument_wise_collection.values())
