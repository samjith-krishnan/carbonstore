import scrapy

class CarbonSpider(scrapy.Spider):
    name='carbon'
    start_urls=['https://carbon38.com/en-in/collections/tops?filter.p.m.custom.available_or_waitlist=1']

    def parse(self,response):
        for product in response.css('div.ProductItem'):
            product_url= product.css('h2.ProductItem__Title.Heading a').attrib['href']

            if product_url:
                yield response.follow(product_url, callback=self.parse_profile)

        next_page= response.css('a[rel="next"]::attr(href)').get()
        if next_page is not None:
          yield response.follow(next_page,callback=self.parse)




    def parse_profile(self,response):
                try:
                    yield{
                        'primary_image_url':response.css('div.AspectRatio.AspectRatio--withFallback img').attrib['src'],
                        'brand':response.css('h2.ProductMeta__Vendor.Heading.u-h1 a::text').get() or response.css('h2.ProductMeta__Vendor.Heading.u-h1::text').get(),
                        'product_name': response.css('h1.ProductMeta__Title.Heading.u-h3::text').get(),
                        'price': response.css('span.ProductMeta__Price.Price::text').get(),
                        'reviews':response.css('div.yotpo-sr-bottom-line-text.yotpo-sr-bottom-line-text--right-panel::text').get() or '0 Reviews',
                        'colour':response.css('span.ProductForm__SelectedValue::text').get() or 'out of stock',
                        'sizes':response.css('ul.SizeSwatchList.HorizontalList.HorizontalList--spacingTight li label::text').getall(),
                        'description':response.css('div.Faq__Answer.Rte span::text').get() or 'No Description',
                        'product_url': response.url,
                        'image_urls':response.css('div.Product__SlideshowNavScroller a::attr(href)').getall(),


                    }
                except:
                    yield{
                        'primary_image_url':response.css('div.AspectRatio.AspectRatio--withFallback img').attrib['src'],
                        'brand':response.css('h2.ProductMeta__Vendor.Heading.u-h1 a::text').get(),
                        'product_name': response.css('h1.ProductMeta__Title.Heading.u-h3::text').get(),
                        'price': 'out of stock',
                        'reviews':response.css('div.yotpo-sr-bottom-line-text.yotpo-sr-bottom-line-text--right-panel::text').get() or '0 Reviews', 
                        'colour':'not available',
                        'sizes':[],
                        'description':response.css('div.Faq__Answer.Rte span::text').get() or 'No Description',
                        'product_url': response.url,
                        'image_urls':response.css('div.Product__SlideshowNavScroller a::attr(href)').getall(),
                    }

        
