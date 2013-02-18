import re
# from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from slando_apt_od.items import SlandoAptOdItem

class SlandoSpider(CrawlSpider):
    name = "slando"
    allowed_domains = ["slando.ua"]
    start_urls = [
	"http://odessa.od.slando.ua/nedvizhimost/?all_categories=1&search[filter_float_price%3Afrom]=2400&search[filter_float_price%3Ato]=3200",
    ]

    rules = (
	Rule(SgmlLinkExtractor(allow=('obyavlenie',)), callback='parse_item'),
    )

    def parse_item(self, response):
#	self.log('parsing %s' % response.url)
	hxs = HtmlXPathSelector(response)
	content = hxs.select('//div[@class="content"]')
	header = content.select('div[@class="margintop20 clr"]')
	item = SlandoAptOdItem()
	item['link'] = response.url 
	item['id'] = re.search(r'-ID(.{5})\.html', response.url).group(1)
	item['num'] = header.select('p/small/span/span/text()').extract()[0].strip()
	item['title'] = header.select('h1/text()').extract()[0].strip()
	print 'item'
	# print item
	item['desc'] = content.select('div[2]/div[1]/div[2]/p/text()').extract()[0].strip()
	item['price'] = content.select('div[2]/div[2]/div[1]/div[1]/div[1]/strong/text()').extract()[0].strip()
	item['addr'] = content.select('div[2]/div[2]/div[1]/div[4]/table//address/p[2]/text()').extract()[0].strip()
	return item


class SandoSpider:
    name = "slando"
    allowed_domains = ["slando.ua"]
    start_urls = [
	    "http://odessa.od.slando.ua/nedvizhimost/?all_categories=1&search[filter_float_price%3Afrom]=2400&search[filter_float_price%3Ato]=3200",
	    # "http://odessa.od.slando.ua/nedvizhimost/?all_categories=1&search[filter_float_price%3Afrom]=2400&search[filter_float_price%3Ato]=3200&page=2",
	    # "http://odessa.od.slando.ua/nedvizhimost/?all_categories=1&search[filter_float_price%3Afrom]=2400&search[filter_float_price%3Ato]=3200&page=3" 
    ]

    def parse(self, response):
	hxs = HtmlXPathSelector(response)
	offers = hxs.select('//table[@id="offers_table"]/tbody/tr/td/table/tbody/tr')
	print "offers found: {0}".format(len(offers))
	items = []
	for offer in offers:
	    header = offer.select('td/h3')
	    item = SlandoAptOdItem()
	    item['link'] = header.select('a/@href').extract()[0].strip()
	    item['id'] = re.search(r'-ID(.{5})\.html', item['link']).group(1)
	    item['title'] = header.select('a/span/text()').extract()[0].strip()
	    item['price'] = offer.select('td/div/p/strong/text()').extract()[0].strip()
	    items.append(item)
	return items
	    # string = title + ': ' + price
	    # print string.encode('utf-8')
