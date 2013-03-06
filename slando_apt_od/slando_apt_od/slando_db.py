import sqlite3
import time, datetime

DB_NAME = '/home/bepec/.db/slando.db'

_db = sqlite3.connect(DB_NAME)
log_handle = None

def _log(message):
    if (log_handle):
        log_handle.msg('DB: {0}'.format(message))

class OffersTable:

    def __init__(self):
	self.cursor = _db.cursor()
	if not self.__table_exists():
            self.__create_table()

    def insert_item(self, item):
	values = (item['id'], item['num'], item['title'], item['link'], item['price'], item['desc'], item['addr'], self.timestamp())
	_db.execute("INSERT INTO offers VALUES(?, ?, ?, ?, ?, ?, ?, ?)", values)
	_db.commit()
	_log("Inserted item with ID={0} into db".format(item['id']))
        return item

    def select_all(self):
	self.cursor.execute('SELECT * FROM offers')
	return self.cursor.fetchall()

    def __create_table(self):
	self.cursor.execute('''
	    CREATE TABLE offers(id text
			       ,num integer
			       ,title text
			       ,link text
			       ,price float
			       ,desc text
			       ,addr text
			       ,added int)''')
	_log("Created table 'offers' in db")

    def __table_exists(self):
	self.cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='offers'")
	result = self.cursor.fetchone()
	return (result[0] > 0)

    def timestamp(self):
	return time.mktime(datetime.datetime.now().timetuple())

