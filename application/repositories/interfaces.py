"""
Interface declarations for repository
"""


import abc


class InstrumentRepository:
    """
    Instrument Respository Interface
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_by_id(self, instrument_id):
        """
        Get Instrument By Id
        """
        pass

    @abc.abstractmethod
    def get_by_ids(self, instrument_ids):
        """
        Get Instrument By List of Ids
        """
        pass


class TransactionRepository:
    """
    Transaction Respository Interface
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_by_id(self, transaction_id):
        """
        Get Transaction By Id
        """
        pass

    @abc.abstractmethod
    def get_by_ids(self, instrument_ids):
        """
        Get Transaction By List of Ids
        """
        pass

    @abc.abstractmethod
    def get_by_user_id(self, user_id):
        """
        Get Transactions By User Id
        """
        pass
