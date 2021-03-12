import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from finca.items import Article


class FincaSpider(scrapy.Spider):
    name = 'finca'
    start_urls = ['https://www.finca.ge/category/%e1%83%a1%e1%83%98%e1%83%90%e1%83%ae%e1%83%9a%e1%83%94%e1%83%94%e1%83%91%e1%83%98/']

    def parse(self, response):
        links = response.xpath('//a[@class="fusion-read-more"]/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        if 'pdf' in response.url:
            return

        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//h1/text()').get()
        if title:
            title = title.strip()

        date = response.xpath('//div[@class="fusion-meta-info-wrapper"]/span/text()').get()
        if date:
            date = date.strip()

        content = response.xpath('//div[@class="post-content"]//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content).strip()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
