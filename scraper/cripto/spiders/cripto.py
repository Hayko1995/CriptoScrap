import scrapy
import re
import json
import hashlib
from pathlib import Path
import scrapy
from scrapy_playwright.page import PageMethod

supportedCoins = ['USDC', 'SOL']


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
        coin_siv = response.xpath(
            '//tr[contains(@class, "__clickable_iresq_108")]')
        item = {}
        for coin in coin_siv:
            coins = coin.xpath('.//td')
            name = coins[0].xpath(
                './/div[contains(@class, "_reserveName_1nycx_12")]/p/text()').get()
            
            if (name in supportedCoins):
                item['name'] = name
                item['item'] = "kamino"
                item['deposit'] = coins[4].xpath(
                    './/div[contains(@class, "_cell_1nycx_1")]/p/text()').get()
                item['borrow'] = coins[6].xpath(
                    './/div[contains(@class, "_cell_1nycx_1")]/p/text()').get()
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
                PageMethod("wait_for_timeout", 10000)
            ]
        ))

    def parse(self, response):
        coin_div = response.xpath(
            '//tr[contains(@class, "transition-colors")]')
        item = {}
        coin_div = coin_div[1:]
        for coin in coin_div:
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


class ScrapingDriftSpider(scrapy.Spider):
    name = "drift"
    allowed_domains = ["app.marginfi.com"]
    urls = ['https://app.drift.trade/earn/lend-borrow/deposits',
            'https://app.drift.trade/earn/lend-borrow/borrow']

    def start_requests(self):

        for url in self.urls:
            yield scrapy.Request(url, meta=dict(
                playwright=True,
                playwright_include_page=True,
                playwright_page_methods=[
                    PageMethod("wait_for_timeout", 10000)
                ]
            ))

    def parse(self, response):
        if response.url == self.urls[0]:
            coin_div = response.xpath(
                '//div[contains(@class, "bg-container-bg hover:bg-container-bg-hover py-2 css-yv7tq1 ej8o9vq1")]')

            for coin in coin_div:
                item = {}
                item['item'] = 'drift'
                coin_table = coin.xpath('.//div[contains(@class, "w-full")]')
                name = coin_table[0].xpath(
                    './/span[contains(@class, "font-[300] text-[13px] leading-[16px] mt-0.5 text-text-emphasis")]/text()').get().strip()
                if (name in supportedCoins):
                    item['name'] = name
                    item['deposit'] = coin_table[2].xpath(
                        './/span[contains(@class, "whitespace-nowrap")]/text()').get()

                    yield item

        if response.url == self.urls[1]:
            coin_div = response.xpath(
                '//div[contains(@class, "bg-container-bg hover:bg-container-bg-hover py-2 css-1ojaps7 ej8o9vq1")]')
            for coin in coin_div:
                item = {}
                item['item'] = 'drift'
                coin_table = coin.xpath('.//div[contains(@class, "w-full")]')
                name = coin_table[0].xpath(
                    './/span[contains(@class, "font-[300] text-[13px] leading-[16px] mt-0.5 text-text-emphasis")]/text()').get().strip()
                if (name in supportedCoins):
                    item['name'] = name
                    item['borrow'] = coin_table[3].xpath(
                        './/span[contains(@class, "whitespace-nowrap")]/text()').get()
                    yield item
                    
                    
