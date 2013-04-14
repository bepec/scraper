from scrapy import log
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from slando_apt_od.items import EbayItem


class VansSpider(BaseSpider):

    name = "vans"
    allowed_domains = ["ebay.com"]
    start_urls = [
        'http://www.ebay.com/sch/Mens-Shoes-/93427/i.html?_ipg=200&_dcat=15709&LH_ItemCondition=1000%7C1500%7C1750&_sop=15&US%2520Shoe%2520Size%2520%2528Men%2527s%2529=8%252E5&_from=R40&_mPrRngCbx=1&_udhi=39&_nkw=vans&LH_PrefLoc=1&rt=nc&_dmd=1'
    ]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        offers = hxs.select('//div[@id="ResultSetItems"]//tr[@itemprop="offers"]')
        self.log('Got {0} items'.format(len(offers)))
        for offer in offers:
            item = EbayItem()
            item['id'] = offer.select('.//@iid').extract()[0]
            item['title'] = offer.select('.//a[@itemprop="name"]/@title').extract()[0]
            item['link'] = offer.select('.//a[@itemprop="name"]/@href').extract()[0]
            item['time'] = offer.select('.//span[@class="tme"]//@timems').extract()[0]
            item['price'] = offer.select('.//div[@itemprop="price"]/text()').extract()[0]
            item['shipping'] = offer.select('.//span[@class="fee"]/text()').extract()[0].strip()
            yield item
