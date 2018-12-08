import scrapy
from selenium import webdriver
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException


class ArticleCommentsSpider(scrapy.Spider):
    name = "article"
    start_urls = []

    def __init__(self, link):
        self.driver = webdriver.Firefox()
        ArticleCommentsSpider.start_urls = [
            link
        ]

    def parse(self, response):
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

