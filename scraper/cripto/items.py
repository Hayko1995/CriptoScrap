# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class CriptoItem(scrapy.Item):
    # define the fields for your item here like:
    name = Field()
    item = Field()
    deposit = Field()
    borrow = Field()
    staking = Field()
