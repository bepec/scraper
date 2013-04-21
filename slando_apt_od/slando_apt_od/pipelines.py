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
        self.message = "New items:<br><br>\n"
        self.counter = 0

    def process_item(self, item, spider):
        text = "<br>".join([': '.join([key, item.get(key, 'no data')]) for key in item.fields.keys()])
        self.message += text + "<br><br>\n"
        self.counter += 1
        return item

    def close_spider(self, spider):
        if self.counter == 0:
            return
        subject = '{0} new items in {1}!'.format(self.counter, spider.name)
        mail.SendMail('loafshock@gmail.com', subject, self.message)


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
