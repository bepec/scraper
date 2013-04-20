# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
import id_db
from scrapy import log
from slando_apt_od.helpers import mail

id_db.log_handle = log


class MailPipeline(object):

    def __init__(self):
        pass

    def open_spider(self, spider):
        self.message = "New items:\n\n"
        self.subject = 'New items from {0}!'.format(spider.name)

    def process_item(self, spider, item):
        text = "\n".join([':'.join(list(key, item[key])) for key in item.keys()])
        self.message += text

    def close_spider(self, spider):
        mail.SendMail('loafshock@gmail.com', self.subject, self.message)


class WriteDbPipeline(object):

    def __init__(self):
        pass

    def open_spider(self, spider):
        self.offersTable = id_db.IdTable(spider.name)

    def process_item(self, item, spider):
        self.offersTable.insert_item(item)
        return item


class DropOldPipeline(object):

    def process_item(self, item, spider):
        pass
