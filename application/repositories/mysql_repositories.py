"""
Concrete declarations for repository interface specific to mysql
"""

from interfaces import InstrumentRepository, \
        TransactionRepository


class MySqlInstrumentRepository(InstrumentRepository):
    """
    MySQL Instrument Respository Implementation
    """

    def __init__(self, connection):
        self.connection = connection

    def get_by_id(self, instrument_id):
        try:
            curr = self.connection.cursor()
            curr.execute("SELECT * FROM Instrument WHERE ID = {}"
                         .format(instrument_id))
            result = curr.fetchone()
            self.connection.commit()
            return result
        except:
            self.connection.rollback()
            raise
        finally:
            curr.close()

    def get_by_ids(self, instrument_ids):
        if len(instrument_ids) is 0:
            return []
        try:
            curr = self.connection.cursor()
            curr.execute("SELECT * FROM Instrument WHERE ID IN ({})"
                         .format(','.join(str(u) for u in instrument_ids)))
            result = curr.fetchall()
            self.connection.commit()
            return result
        except:
            self.connection.rollback()
            raise
        finally:
            curr.close()


class MySqlTransactionRepository(TransactionRepository):
    """
    MySQL Transaction Respository Implementation
    """

    def __init__(self, connection):
        self.connection = connection

    def get_by_id(self, transaction_id):
        try:
            curr = self.connection.cursor()
            curr.execute("SELECT * FROM Transaction WHERE ID = {}"
                         .format(transaction_id))
            result = curr.fetchone()
            self.connection.commit()
            return result
        except:
            self.connection.rollback()
            raise

    def get_by_user_id(self, user_id):
        try:
            curr = self.connection.cursor()
            curr.execute("SELECT * FROM Transaction WHERE User_ID = {}"
                         .format(user_id))
            result = curr.fetchall()
            self.connection.commit()
            return result
        except:
            self.connection.rollback()
            raise
        finally:
            curr.close()

    def get_by_ids(self, transaction_ids):
        if len(transaction_ids) is 0:
            return []
        try:
            curr = self.connection.cursor()
            curr.execute("SELECT * FROM Transaction WHERE ID IN ({})"
                         .format(','.join(str(u) for u in transaction_ids)))
            result = curr.fetchone()
            self.connection.commit()
            return result
        except:
            self.connection.rollback()
            raise
        finally:
            curr.close()
