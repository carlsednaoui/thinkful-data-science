import scrapy
from scrapy.crawler import CrawlerProcess

class ClistSpider(scrapy.Spider):
    name = "WS"
    
    # Here is where we insert our scraper.
    start_urls = [
        'https://newyork.craigslist.org/search/sss?query=couch&sort=rel'
        ]

    # Identifying the information we want from the query response and extracting it using xpath.
    def parse(self, response):
        for res in response.xpath('//*[@id="sortable-results"]/ul/li'):
            # print(res.xpath('*/a[@class="result-title hdrlnk"]/@href').extract_first())

            # Yield a dictionary with the values we want.
            yield {
                'title': res.xpath('*/a[@class="result-title hdrlnk"]/text()').extract_first(),
                'price': res.xpath('*/span[@class="result-price"]/text()').extract_first(),
                'url': res.xpath('*/a[@class="result-title hdrlnk"]/@href').extract_first()
            }
        # Get the URL of the previous page.
        next_page = response.xpath('//*[@id="searchform"]/div[3]/div[3]/span[2]/a[3]/@href').extract_first()
        
        # There are a LOT of pages here.  For our example, we'll just scrape the first 9.
        # This finds the page number. The next segment of code prevents us from going beyond page 9.
        pagenum = int(response.xpath('//*[@id="searchform"]/div[3]/div[3]/span[2]/span[3]/span[1]/span[2]/text()').extract_first())
        print(pagenum)
        
        # Recursively call the spider to run on the next page, if it exists.
        if next_page is not None and pagenum < 360:
            next_page = response.urljoin(next_page)
            # Request the next page and recursively parse it the same way we did above
            yield scrapy.Request(next_page, callback=self.parse)

# Tell the script how to run the crawler by passing in settings.
# The new settings have to do with scraping etiquette.          
process = CrawlerProcess({
    'FEED_FORMAT': 'json',         # Store data in JSON format.
    'FEED_URI': './coursework/unit_5/clist.json',       # Name our storage file.
    'LOG_ENABLED': False,          # Turn off logging for now.
    'ROBOTSTXT_OBEY': True,
    'USER_AGENT': 'ThinkfulDataScienceBootcampCrawler (thinkful.com)',
    'AUTOTHROTTLE_ENABLED': True,
    'HTTPCACHE_ENABLED': True
})

# Start the crawler with our spider.
process.crawl(ClistSpider)
process.start()
print('Success!')