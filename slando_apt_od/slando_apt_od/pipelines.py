# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
import sqlite3
import time, datetime
from scrapy import log

class WriteDbPipeline(object):

    DB_NAME = '/tmp/slando.db'

    def __init__(self):
	self.conn = sqlite3.connect(self.DB_NAME)
	self.cursor = self.conn.cursor()
	if not self.table_exists():
	    self.cursor.execute('''
		CREATE TABLE offers(id text
			       ,num integer
			       ,title text
			       ,link text
			       ,price float
			       ,desc text
			       ,addr text
			       ,added int)''')
	    log.msg("Created table 'offers' in db")

    def process_item(self, item, spider):
	timestamp = time.mktime(datetime.datetime.now().timetuple())
	values = (item['id'], item['num'], item['title'], item['link'], item['price'], item['desc'], item['addr'], timestamp)
	cursor = self.conn.cursor()
	self.conn.execute("INSERT INTO offers VALUES(?, ?, ?, ?, ?, ?, ?, ?)", values)
	self.conn.commit()
	log.msg("Inserted item with ID={0} into db".format(item['id']))
        return item

    def table_exists(self):
	self.cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='offers'")
	result = self.cursor.fetchone()
	return (result[0] > 0)

