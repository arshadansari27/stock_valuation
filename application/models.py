"""
Models module for all the entities
"""


class Instrument(object):
    """
    Instrument class for each Stock type
    """

    def __init__(self, instrument_id, ticker, name, current_price):
        self.identity = instrument_id
        self.ticker = ticker
        self.name = name
        self.current_price = float(current_price)

    @classmethod
    def fetch_by_id(cls, context, instrument_id):
        repository = context.get('InstrumentRepository')
        if not repository:
            raise Exception("Configuration Error: "
                            "InstrumentRepository is not found")
        instrument_data = repository.get_by_id(instrument_id)
        return Instrument(*instrument_data)

    @classmethod
    def fetch_by_ids(cls, context, instrument_ids):
        repository = context.get('InstrumentRepository')
        if not repository:
            raise Exception("Configuration Error: "
                            "InstrumentRepository is not found")
        return [Instrument(*u) for u in repository.get_by_ids(instrument_ids)]


class Transaction(object):
    """
    Transaction for each user regarding buy or sell
    """

    def __init__(self, tranaction_id, position_id, user_id,
                 buy_or_sell, quantity, price, date):
        self.identity = tranaction_id
        self.position_id = position_id
        self.user_id = user_id
        self.buy_or_sell = buy_or_sell
        self.quantity = int(quantity)
        self.price = float(price)
        self.date = date

    @classmethod
    def fetch_by_id(cls, context, transaction_id):
        repository = context.get('TransactionRepository')
        if not repository:
            raise Exception("Configuration Error: "
                            "TransactionRepository is not found")
        transaction_data = repository.get_by_id(transaction_id)
        return Transaction(*transaction_data)

    @classmethod
    def fetch_by_user_id(cls, context, user_id):
        repository = context.get('TransactionRepository')
        if not repository:
            raise Exception("Configuration Error: "
                            "TransactionRepository is not found")
        transactions_data = repository.get_by_user_id(user_id)
        return (Transaction(*u) for u in transactions_data)

    @classmethod
    def fetch_by_ids(cls, context, instrument_ids):
        repository = context.get('TransactionRepository')
        if not repository:
            raise Exception("Configuration Error: "
                            "TransactionRepository is not found")
        return [Transaction(*u) for u in repository.get_by_ids(instrument_ids)]
