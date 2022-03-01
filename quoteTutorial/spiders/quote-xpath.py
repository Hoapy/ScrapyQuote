import scrapy
from ..items import QuotetutorialItem


class QuoteSpider(scrapy.Spider):
    name = "quotes-xpath"
    page_number = 2
    start_urls = ["https://quotes.toscrape.com/page/1/"]

    def parse(self, response):
        item = QuotetutorialItem()
        all_div_quotes = response.xpath('//div[@class="quote"]')
        for quotes in all_div_quotes:
            title = quotes.xpath(".//span[@class='text']//text()").extract()
            author = quotes.xpath(".//small[@class='author']//text()").extract()
            tag = quotes.xpath(".//div[@class='tags']//a//text()").extract()

            item["title"] = title
            item["author"] = author
            item["tag"] = tag
            yield item
         
        next_page = 'https://quotes.toscrape.com/page/' + str(QuoteSpider.page_number) + '/'
        if QuoteSpider.page_number < 11:
            QuoteSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse)