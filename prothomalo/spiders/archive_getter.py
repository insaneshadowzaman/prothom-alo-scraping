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

    def __init__(self):
        self.driver = webdriver.Firefox()

    def parse(self, response):
        for div in response.xpath("//div[@class='listing']/div"):
            yield {
                'title-index': div.xpath(".//h2/span/text()").extract_first(),
                'link-index': div.xpath("./a/@href").extract_first()
            }
            for link in div.xpath("./a"):
                yield response.follow(link, callback=self.parse_content)
    
    def parse_content(self, response):

        browser = self.driver.get(response.url)

        # nn = self.driver.find_element_by_xpath("//div[@class='comment_portion']/p")

        delay = 5 # seconds
        comment = None

        try:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
            # comment = self.driver.find_element_by_css_selector("//div[@class='comment_portion']//p")
            try:
                comment = self.driver.find_element_by_css_selector("div.comment_portion").text
            except NoSuchElementException:
                comment = None
            print()
            print()
            print()
            print()
            print()
            print(comment)
            print()
            print()
            print()
            print()
            print()
            # comment = self.driver.find_element_by_xpath("//div[@class='comment_portion']//p/text()")
            # comment = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, "//div[@id='comments']//p")))
        except TimeoutException:
            pass

        yield {
            'title-page': response.xpath("//h1/text()").extract_first(),
            'content': response.xpath("//article/div//p/text()").extract(),
            'comment': comment
        }