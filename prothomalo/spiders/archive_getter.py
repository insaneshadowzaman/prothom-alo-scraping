import scrapy


class ProthomSpider(scrapy.Spider):
    name = "prothom"
    start_urls = [
        'https://www.prothomalo.com/archive/2017-01-31'
    ]

    def parse(self, response):
        for div in response.xpath("//div[@class='listing']/div"):
            yield {
                'title-index': div.xpath(".//h2/span/text()").extract_first(),
                'link-index': div.xpath("./a/@href").extract_first()
            }
            for link in div.xpath("./a"):
                yield response.follow(link, callback=self.parse_content)
    
    def parse_content(self, response):
        yield {
            # 'title-page': response.xpath("//h1[@class='title']").extract_first()
            'title-page': response.xpath("/**").extract_first
        }