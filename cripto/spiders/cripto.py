import scrapy
import re
import json
import hashlib
from pathlib import Path


import scrapy


from scrapy_playwright.page import PageMethod


class ScrapingKaminoSpider(scrapy.Spider):
    name = "kamino"
    allowed_domains = ["app.kamino.finance"]

    def start_requests(self):
        url = "https://app.kamino.finance/?filter=all"
        yield scrapy.Request(url, meta=dict(
            playwright=True,
            playwright_include_page=True,
            playwright_page_methods=[
                PageMethod("wait_for_timeout", 8000)
            ]
        ))

    def parse(self, response):
        # iterate over the product elements
        # print(response)
        # with open("a.html", 'w') as html_file:
        #     html_file.write(str(response.xpath('//tr[contains(@class, "__clickable_iresq_108")]').extract()))

        coin_siv = response.xpath(
            '//tr[contains(@class, "__clickable_iresq_108")]')
        item = {}
        for coin in coin_siv:
            coins = coin.xpath('.//td')
            item['name'] = coins[0].xpath(
                './/div[contains(@class, "_reserveName_1nycx_12")]/p/text()').get()
            item['total_supply'] = coins[1].xpath(
                './/div[contains(@class, "_iconContainer_19edf_434")]/p/text()').get()
            item['total_borrow'] = coins[2].xpath(
                './/div[contains(@class, "_iconContainer_19edf_434")]/p/text()').get()
            item['maxLtv'] = coins[3].xpath(
                './/div[contains(@class, "_cell_1nycx_1")]/p/text()').get()
            item['supply_aPY'] = coins[4].xpath(
                './/div[contains(@class, "_cell_1nycx_1")]/p/text()').get()
            item['borrow_aPY'] = coins[6].xpath(
                './/div[contains(@class, "_cell_1nycx_1")]/p/text()').get()

            print("results", item['name'], item['total_supply'], item['total_borrow'],
                  item['maxLtv'],  item['supply_aPY'], item['borrow_aPY'])
            yield item


class ScrapingMagnifiSpider(scrapy.Spider):
    name = "marginfi"
    allowed_domains = ["app.marginfi.com"]

    def start_requests(self):
        url = "https://app.marginfi.com/"
        yield scrapy.Request(url, meta=dict(
            playwright=True,
            playwright_include_page=True,
            playwright_page_methods=[
                PageMethod("wait_for_timeout", 8000)
            ]
        ))

    def parse(self, response):
        # iterate over the product elements
        # print(response)

        coin_div = response.xpath(
            '//tr[contains(@class, "transition-colors")]')
        item = {}
        coin_div = coin_div[1:]

        # with open("a.html", 'w') as html_file:
        #     html_file.write(
        #         str(coin_div.extract()))

        for coin in coin_div:

            # print(coin.extract())
            coin_table = coin.xpath('.//td[contains(@class, "align-middle")]')

            with open("a.html", 'w') as html_file:
                html_file.write(
                    str(coin_table.extract()))
            item['coinName'] = coin_table[0].xpath(
                './/div[contains(@class, "flex")]/div/text()').get()
            item['price'] = coin_table[1].xpath(
                './/div[contains(@class, "flex")]/div/text()').get()
            item['apy'] = coin_table[2].xpath(
                './/div[contains(@class, "flex")]/div/text()').get()
            item['weight'] = coin_table[3].xpath(
                './/div/text()').get()
            item['deposits'] = coin_table[4].xpath(
                './/span/text()').get()
            item['globalLimit'] = coin_table[5].xpath(
                './/div/text()').get()
            item['utilisation'] = coin_table[6].xpath(
                './/div/text()').get()
            
            yield item