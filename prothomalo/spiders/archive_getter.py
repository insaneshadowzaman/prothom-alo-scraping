import scrapy
from selenium import webdriver
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException


class ProthomSpider(scrapy.Spider):
    name = "prothom"
    start_urls = [
        'https://www.prothomalo.com/archive/2017-01-31'
    ]

    def __init__(self, date):
        self.driver = webdriver.Firefox()
        ProthomSpider.start_urls = [
            'https://www.prothomalo.com/archive/' + date
        ]

    def parse(self, response):
        for div in response.xpath("//div[@class='listing']/div"):  # Xpath language
            yield {  # dictionary
                'title-index': div.xpath(".//h2/span/text()").extract_first(),
                'link-index': div.xpath("./a/@href").extract_first()
            }
            for link in div.xpath("./a"):
                yield response.follow(link, callback=self.parse_content)

    def parse_content(self, response):

        browser = self.driver.get(response.url)

        delay = 2  # seconds

        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # javascript execute in browser
        time.sleep(delay)  # sleep
        # comment = self.driver.find_element_by_css_selector("//div[@class='comment_portion']//p")
        try:
            comment = self.driver.find_elements_by_css_selector(
                "ul.comments_holder_ul>li p")  # css selector to get array
        except NoSuchElementException:
            comment = None  # if no comments
        comments = [c.text for c in comment]  # get only text from the gathered comments

        yield {  # return dictionary that scrapy will convert to json and write in output file.
            'title-page': response.xpath("//h1/text()").extract_first(),
            'content': response.xpath("//article/div//p/text()").extract(),
            'comment': comments
        }
