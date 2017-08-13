# import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.linkextractors import LinkExtractor
from spider_new.items import SpiderNewItem


class NewSpider(CrawlSpider):
    download_delay = 1
    name = "tnspider"
    site = 'technews'
    allowed_domains = ["technews.tw"]
    start_urls = [
        "http://technews.tw"
    ]
    rules = (
        # and follow links from them (since no callback means follow=True by default).
        Rule(LinkExtractor(allow=(r'^http:\/\/technews\.tw\/page\/[2-5]', )),
                            callback='parse_items',
                            follow=False),
    )

    def parse_start_url(self, response):
        return self.parse_items(response)

    def parse_items(self, response):
        hxs = HtmlXPathSelector(response)
        for sel in hxs.select('//article'):

            item = SpiderNewItem()

            title = sel.select('.//tr/td[@class="maintitle"]//a/text()').extract()
            link = sel.select('.//tr/td[@class="maintitle"]//a/@href').extract()
            post_id = sel.select('./@id').extract()[0]
            item['title'] = title
            item['link'] = link
            item['post_id'] = post_id
            item['site'] = self.site
            yield item
