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
    name = "marginfi-borrow"
    allowed_domains = ["app.marginfi.com"]

    def start_requests(self):
        url = "https://app.marginfi.com/"
        yield scrapy.Request(url, meta=dict(
            playwright=True,
            playwright_include_page=True,
            # f"The element '{record_variable}' is found in the received data"
            playwright_page_methods=[
                PageMethod("click", "button[type=button]"),
                PageMethod("click", "button[aria-label=Borrow]"),
                PageMethod("wait_for_timeout", 10000)
            ]
        ))

    def parse(self, response):
        coin_div = response.xpath(
            '//tr[contains(@class, "transition-colors")]')

        coin_div = coin_div[1:]
        for coin in coin_div:
            coin_table = coin.xpath('.//td[contains(@class, "align-middle")]')
            try:
                name = coin_table[0].xpath(
                    './/div[contains(@class, "flex")]/div/text()').get()

                if (name in supportedCoins):
                    item = {}
                    item['item'] = 'marginfi'
                    item['name'] = name
                    item['borrow'] = coin_table[2].xpath(
                        './/div[contains(@class, "flex")]/div/text()').get()

                    yield item
            except:
                continue


class ScrapingMagnifiLandSpider(scrapy.Spider):
    name = "marginfi-land"
    allowed_domains = ["app.marginfi.com"]

    def start_requests(self):
        url = "https://app.marginfi.com/"
        yield scrapy.Request(url, meta=dict(
            playwright=True,
            playwright_include_page=True,
            # f"The element '{record_variable}' is found in the received data"
            playwright_page_methods=[
                PageMethod("wait_for_timeout", 10000)
            ]
        ))

    def parse(self, response):
        coin_div = response.xpath(
            '//tr[contains(@class, "transition-colors")]')

        coin_div = coin_div[1:]
        for coin in coin_div:

            coin_table = coin.xpath('.//td[contains(@class, "align-middle")]')
            try:
                name = coin_table[0].xpath(
                    './/div[contains(@class, "flex")]/div/text()').get()
                if (name in supportedCoins):
                    item = {}
                    item['item'] = 'marginfi'
                    item['name'] = name
                    item['deposit'] = coin_table[2].xpath(
                        './/div[contains(@class, "flex")]/div/text()').get()
                    print("🐍 File: spiders/cripto.py | Line: 126 | parse ~ item", item)

                    yield item
            except:
                continue


class ScrapingDriftSpider(scrapy.Spider):
    name = "drift"
    allowed_domains = ["app.drift.trade"]
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


class ScrapingMarinadeSpider(scrapy.Spider):
    name = "marinade"
    urls = ['https://marinade.finance/app/']

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

        coin_div = response.xpath(
            '//span[contains(@class, "text-2xl md:text-[40px] font-semibold text-primary")]')

        item = {}
        item['item'] = 'marinade'
        item['name'] = "SOL"
        staking = coin_div[1].xpath('./text()').get().strip()
        item['staking'] = staking
        yield item


class ScrapingSolblazeSpider(scrapy.Spider):
    name = "solblaze"
    urls = ['https://stake.solblaze.org/app/']

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
        coin_div = response.xpath(
            '//div[contains(@class, "stat-body")]')
        item = {}
        item['item'] = 'solblaze'
        item['name'] = "SOL"
        staking = coin_div[-1].xpath('./text()').get().strip()
        item['staking'] = staking
        print("🐍 File: spiders/cripto.py | Line: 217 | parse ~ item", item)
        yield item
