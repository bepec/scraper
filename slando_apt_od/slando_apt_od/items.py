# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class SlandoAptOdItem(Item):
    id    = Field()
    num   = Field()
    title = Field()
    link  = Field()
    price = Field()
    desc  = Field()
    addr  = Field()


class EbayItem(Item):

    id = Field()
    title = Field()
    link = Field()
    price = Field()
    shipping = Field()
    time = Field()
    image = Field()
