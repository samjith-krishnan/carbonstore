import scrapy

class CarbonSpider(scrapy.Spider):
    name='carbon'
    start_urls=['https://carbon38.com/en-in/collections/tops?filter.p.m.custom.available_or_waitlist=1']

    def parse(self,response):
        for product in response.css('div.ProductItem'):
            try:
                yield{
                    'name': product.css('h2.ProductItem__Title.Heading a::text').get(),
                    'price': product.css('span.ProductItem__Price.Price::text').get().replace('Rs. ',''),
                    'link': product.css('a.ProductItem__ImageWrapper.ProductItem__ImageWrapper--withAlternateImage').attrib['href'],

                }
            except:
                yield{
                    'name': product.css('h2.ProductItem__Title.Heading a::text').get(),
                    'price': 'sold out',
                    'link': product.css('a.ProductItem__ImageWrapper.ProductItem__ImageWrapper--withAlternateImage').attrib['href'],

                }

        next_page= response.css('a.Pagination__NavItem.Link.Link--primary').attrib['href']
        if next_page is not None:
            yield response.follow(next_page,callback=self.parse)
                    

        
