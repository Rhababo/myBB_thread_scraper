import scrapy

class ForumSpider(scrapy.Spider):
    name = 'forumspider'
    start_urls = ['https://quotes.toscrape.com']

    def parse(self, response):
        authors = response.css("small.author::text").extract()
        yield {"listAuthors": authors}

