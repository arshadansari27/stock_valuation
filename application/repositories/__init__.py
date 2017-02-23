from interfaces import InstrumentRepository,\
        TransactionRepository

import MySQLdb
from .mysql_repositories import MySqlInstrumentRepository
from .mysql_repositories import MySqlTransactionRepository


class RepositoryFactory(object):

    @classmethod
    def factory(cls, config, store):
        if store != 'mysql':
            raise Exception("Unsupported factory parameter")
        conn = MySQLdb.connect(host=config['host'], port=config['port'], 
                               user=config['user'], passwd=config['password'], 
                               db=config['db'])

        return {
            'InstrumentRepository': MySqlInstrumentRepository(conn),
            'TransactionRepository': MySqlTransactionRepository(conn)
        }
