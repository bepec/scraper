import sqlite3
import time
import datetime

DB_NAME = '/home/bepec/.db/scraper.db'

_db = sqlite3.connect(DB_NAME)
log_handle = None


def _log(message):
    if (log_handle):
        log_handle.msg('DB: {0}'.format(message))


class IdTable:

    def __init__(self, name):
        self.cursor = _db.cursor()
        self.name = name
        if not self.__table_exists():
            self.__create_table()

    def insert_item(self, item):
        values = (item['id'],)
        _db.execute("INSERT INTO {0} VALUES(?)".format(self.name), values)
        _db.commit()
        _log("Inserted item with ID={0} into db".format(item['id']))
        return item

    def select_all(self):
        self.cursor.execute('SELECT * FROM {0}'.format(self.name))
        return self.cursor.fetchall()

    def __create_table(self):
        self.cursor.execute('CREATE TABLE {0}(id int)'.format(self.name))
        _log("Created table '{0}' in db".format(self.name))

    def __table_exists(self):
        self.cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='{0}'".format(self.name))
        result = self.cursor.fetchone()
        return (result[0] > 0)

    def timestamp(self):
        return time.mktime(datetime.datetime.now().timetuple())
