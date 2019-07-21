import scrapy

# 1 getting contect from a particular tags 
# 2 automatically scrap data from all pages

class GoodReadsSpider(scrapy.Spider):
    #identity
    name = 'getcontent'

    # requests
    def start_requests(self):
        url= 'https://www.goodreads.com/quotes?page=1'
        yield scrapy.Request(url=url,callback=self.parse)
    
    # response
    def parse(self,response):
        for quote in response.selector.xpath("//div[@class='quote']"):
           yield{
               'text': quote.xpath(".//div[@class='quoteText']/text()[1]").extract_first(),
               'author': quote.xpath(".//span[@class='authorOrTitle']/text()").extract_first(),  #  //div[@class='quoteText']/child::a/text()
               'tags': quote.xpath(".//div[@class='greyText smallText left']/a/text()").extract()    #  //div[@class='greyText smallText left']/a/text()
           }
            # /quotes?page=2
        next_page= response.selector.xpath("//a[@class='next_page']/@href").extract_first()
        if next_page is not None:
            next_page_link= response.urljoin(next_page)
            yield scrapy.Request(url=next_page_link, callback=self.parse)