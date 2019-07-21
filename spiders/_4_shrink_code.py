import scrapy
from scrapy.loader import ItemLoader
from demo1.items import QuoteItem


# shrink the code 

class GoodReadsSpider(scrapy.Spider):
    #identity
    name = 'cleanquote' 

 

    # requests

    # use below code if you give function name other then "parse"
    #def start_requests(self):
       # url= 'https://www.goodreads.com/quotes?page=1'
       # yield scrapy.Request(url=url,callback=self.parse)
    
    # instead of above code we can also just give 
    start_url=[ 
        'https://www.goodreads.com/quotes?page=1'
    ]   # make sure its always list even single url or multiple url

    # it only work when give the function name as def "parse"




    # response
    def parse(self,response):
        #for quote in response.selector.xpath("//div[@class='quote']"):
        # removing selector 
        for quote in response.xpath("//div[@class='quote']"):
           loader = ItemLoader(item=QuoteItem(), selector=quote,response=response)
           loader.add_xpath('text',".//div[@class='quoteText']/text()[1]")
           loader.add_xpath('author',"//div[@class='quoteText']/child::span")
           loader.add_xpath('tags',".//div[@class='greyText smallText left']/a")
           yield loader.load_item()
          
            # removing selector
        # next_page= response.selector.xpath("//a[@class='next_page']/@href").extract_first()
        next_page= response.xpath("//a[@class='next_page']/@href").extract_first()
        if next_page is not None:
            next_page_link= response.urljoin(next_page)
            yield scrapy.Request(url=next_page_link, callback=self.parse)