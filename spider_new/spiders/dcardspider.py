from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from spider_new.items import SpiderNewItem


class DCardSpider(CrawlSpider):
    name = "dcardspider"
    allowed_domains = ["www.dcard.tw"]
    start_urls = [
        "https://www.dcard.tw/f/sex"
        # "http://technews.tw"
    ]
    rules = (
        Rule(LinkExtractor(allow=r'^https://www.dcard.tw/f/sex/p'),
             callback='parse_items',
             follow=True),
    )

    def parse_items(self, response):
        self.logger.info('Test, item page! %s', response.url)
        item = SpiderNewItem()
        item['title'] = response.xpath('//h1[starts-with(@class, "Post_title")]//text()').extract()
        item['image_urls'] = response.xpath('//div[starts-with(@class, "Post_content")]//div/img/@src').extract()
        item['link'] = response.url
        yield item
