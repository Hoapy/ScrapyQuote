import scrapy
from ..items import QuotetutorialItem
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser


class QuoteSpider(scrapy.Spider):
    name = "quotes-css"
    next_number = 2
    start_urls = ["https://quotes.toscrape.com/login"]

    def parse(self, response):
        token = response.css("form input::attr(value)").extract_first()
        return FormRequest(
            url=self.start_urls[0],
            formdata={
                "csrf_token": token,
                "username": "hoanguyen",
                "password": "124vq",
            },
            callback=self.start_scraping,
        )

    def start_scraping(self, response):
        open_in_browser(response)
        item = QuotetutorialItem()

        all_div_quotes = response.css("div.quote")
        for quotes in all_div_quotes:

            title = quotes.css("span.text::text").extract()
            author = quotes.css(".author::text").extract()
            tag = quotes.css(".tag::text").extract()

            item["title"] = title
            item["author"] = author
            item["tag"] = tag

            yield item
     