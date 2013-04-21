from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from slando_apt_od.items import EbayItem
from slando_apt_od.id_db import IdTable
from exceptions import IndexError


class VansSpider(BaseSpider):

    name = "vans"
    allowed_domains = ["ebay.com"]
    start_urls = [
        'http://www.ebay.com/sch/Mens-Shoes-/93427/i.html?_from=R40&_samihi&_oexkw&_stpos=07014&_sop=15&_okw&_ipg=200&US%2BShoe%2BSize%2B%28Men%27s%29=8%252E5&LH_BIN=1&LH_ItemCondition=1000%7C1500%7C1750&_localstpos=07014&_samilow&_clu=2&_udhi=41&_ftrt=901&_sabdhi&_udlo&_ftrv=1&_sabdlo&_adv=1&gbr=1&_dmd=1&_mPrRngCbx=1&_nkw=vans&LH_LocatedIn=1&_dcat=15709&US%2520Shoe%2520Size%2520%2528Men%2527s%2529=8%252E5&rt=nc&_fcid=1'
    ]

    def parse(self, response):
        id_table = IdTable(self.name)
        id_list = [item[0] for item in id_table.select_all()]
        hxs = HtmlXPathSelector(response)
        offers = hxs.select('//div[@id="ResultSetItems"]//tr[@itemprop="offers"]')
        self.log('Got {0} items'.format(len(offers)))
        for offer in offers:
            item = EbayItem()
            item['id'] = offer.select('.//@iid').extract()[0]
            if int(item['id']) in id_list:
                self.log('Item {0} is in db, ignore'.format(item['id']))
                continue
            try:
                item['title'] = offer.select('.//a[@itemprop="name"]/@title').extract()[0]
                item['link'] = offer.select('.//a[@itemprop="name"]/@href').extract()[0]
                item['time'] = offer.select('.//span[@class="tme"]//@timems').extract()[0]
                item['price'] = offer.select('.//div[@itemprop="price"]/text()').extract()[0].strip()
                item['shipping'] = ''.join(offer.select('.//span[@class="ship"]//child::text()').extract()).strip()
                yield item
            except IndexError as e:
                self.log("Error while parsing {0}:\n'{1}'".format(offer.extract(), e))
