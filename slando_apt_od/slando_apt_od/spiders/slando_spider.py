import re
# from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy import log
from slando_apt_od.items import SlandoAptOdItem
from slando_apt_od.slando_db import OffersTable

class SlandoSpider(CrawlSpider):
    name = "slando"
    allowed_domains = ["slando.ua"]
    start_urls = [
	"http://odessa.od.slando.ua/nedvizhimost/?all_categories=1&search[filter_float_price%3Afrom]=2400&search[filter_float_price%3Ato]=3200",
    ]

    rules = (
	Rule(SgmlLinkExtractor(allow=('obyavlenie',)), callback='parse_item', process_links='process_links'),
    )

    def process_links(self, links):
	return self.links_not_in_db(links)

    def parse_item(self, response):
	hxs = HtmlXPathSelector(response)
	content = hxs.select('//div[@class="content"]')
	header = content.select('div[@class="margintop20 clr"]')
	item = SlandoAptOdItem()
	item['link'] = response.url 
	item['id'] = re.search(r'-ID(.{5})\.html', response.url).group(1)
	item['num'] = header.select('p/small/span/span/span/text()').extract()[0].strip()
	item['title'] = header.select('h1/text()').extract()[0].strip()
	item['desc'] = content.select('div[2]/div[1]/div[2]/p/text()').extract()[0].strip()
	item['price'] = content.select('div[2]/div[2]/div[1]/div[1]/div[1]/strong/text()').extract()[0].strip()
	item['addr'] = content.select('div[2]/div[2]/div[1]/div[4]/table//address/p[2]/text()').extract()[0].strip()
	return item

    def links_not_in_db(self, links):
        offersList = OffersTable().select_all()
        idList = [ offer[0] for offer in offersList ]
        filteredLinks = list()
	for link in links:
	    id = re.search(r'-ID(.{5})\.html', link.url).group(1)
	    if not id in idList: 
		filteredLinks.append(link)
	    else:
		log.msg("Item with ID={0} is already in db, skipping.".format(id))
	return filteredLinks

