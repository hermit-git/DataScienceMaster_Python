import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/',
            #'http://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        for q in response.css('div.quote'):
            text=q.css('span.text::text').get()
            author=q.css('small.author::text').get()
            tags=q.css('a.tag::text').getall()
            yield {
            "text":text,
            "Author":author,
            "tags":tags

            }
            # with open(filename, 'wb') as f:
            #f.write(response.body)
        #self.log('Saved file %s' % filename)
         
        # Now for recursive crawler
        next_page=response.css('li.next a::attr(href)').get)(
        if next_page is not None:
            next_page=response.urljoin(next_page)
            yield scrapy.Request(next_page,callback=self.parse)
