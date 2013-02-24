# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
import sqlite3

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
			       ,addr text)''')
	self.cursor.execute("insert into offers(id, title) values('abc', 'a big cock')")

    def process_item(self, item, spider):
	values = (item['id'], item['num'], item['title'], item['link'], item['price'], item['desc'], item['addr'])
	print "executing INSERT statement"
	cursor = self.conn.cursor()
	# print cursor.execute("INSERT INTO offers VALUES(?, ?, ?, ?, ?, ?, ?)", values)
	print self.conn.execute("INSERT INTO offers VALUES(?, ?, ?, ?, ?, ?, ?)", values)
	# print cursor.execute("INSERT INTO offers(id, title) VALUES(?, ?)", (item['id'], item['title']))
	self.conn.commit()
        return item

    def table_exists(self):
	self.cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='offers'")
	result = self.cursor.fetchone()
	return (result[0] > 0)

