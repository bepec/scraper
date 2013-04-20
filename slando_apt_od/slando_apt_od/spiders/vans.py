from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from slando_apt_od.items import EbayItem
from slando_apt_od.id_db import IdTable


class VansSpider(BaseSpider):

    name = "vans"
    allowed_domains = ["ebay.com"]
    start_urls = [
        'http://www.ebay.com/sch/Mens-Shoes-/93427/i.html?_from=R40&_samihi=&_oexkw=&_stpos=07024&_sop=15&_okw=&_ipg=200&US+Shoe+Size+%28Men%27s%29=8%252E5&LH_BIN=1&LH_ItemCondition=1000%7C1500%7C1750&_localstpos=07024&_samilow=&_clu=2&_udhi=41&_ftrt=901&_sabdhi=&_udlo=&_ftrv=1&_sabdlo=&_adv=1&gbr=1&_dmd=1&_mPrRngCbx=1&_nkw=vans&LH_LocatedIn=1&_dcat=15709&US%2520Shoe%2520Size%2520%2528Men%2527s%2529=8%252E5&rt=nc'
    ]

    def parse(self, response):
        id_table = IdTable(self.name)
        id_list = [item[0] for item in id_table.select_all()]
        self.log('In db items: {0}'.format(len(id_list)))
        self.log('Content: {0}'.format(id_list))
        hxs = HtmlXPathSelector(response)
        offers = hxs.select('//div[@id="ResultSetItems"]//tr[@itemprop="offers"]')
        self.log('Got {0} items'.format(len(offers)))
        for offer in offers:
            item = EbayItem()
            item['id'] = offer.select('.//@iid').extract()[0]
            if int(item['id']) in id_list:
                self.log('Item {0} is in db, ignore'.format(item['id']))
                continue
            item['title'] = offer.select('.//a[@itemprop="name"]/@title').extract()[0]
            item['link'] = offer.select('.//a[@itemprop="name"]/@href').extract()[0]
            item['time'] = offer.select('.//span[@class="tme"]//@timems').extract()[0]
            item['price'] = offer.select('.//div[@itemprop="price"]/text()').extract()[0]
            item['shipping'] = offer.select('.//span[@class="fee"]/text()').extract()[0].strip()
            yield item
