import scrapy
from scrapy.loader import ItemLoader
from demo1.items import QuoteItem

# adding loader to cleaning the data and stored in json correctly
# removing \n unicodes and more from json formats

class GoodReadsSpider(scrapy.Spider):
    #identity
    name = 'cleanquote'

    # requests
    def start_requests(self):
        url= 'https://www.goodreads.com/quotes?page=1'
        yield scrapy.Request(url=url,callback=self.parse)
    
    # response
    def parse(self,response):
        for quote in response.selector.xpath("//div[@class='quote']"):
           loader = ItemLoader(item=QuoteItem(), selector=quote,response=response)
           loader.add_xpath('text',".//div[@class='quoteText']/text()[1]")
           loader.add_xpath('author',"//div[@class='quoteText']/child::span")
           loader.add_xpath('tags',".//div[@class='greyText smallText left']/a")
           yield loader.load_item()
            # /quotes?page=2
        next_page= response.selector.xpath("//a[@class='next_page']/@href").extract_first()
        if next_page is not None:
            next_page_link= response.urljoin(next_page)
            yield scrapy.Request(url=next_page_link, callback=self.parse)