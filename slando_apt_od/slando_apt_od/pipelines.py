# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
import slando_db
from scrapy import log

slando_db.log_handle = log


class WriteDbPipeline(object):

    def __init__(self):
	self.offersTable = slando_db.OffersTable()

    def process_item(self, item, spider):
	self.offersTable.insert_item(item)
        return item


class DropOldPipeline(object):

    def process_item(self, item, spider):
	pass
