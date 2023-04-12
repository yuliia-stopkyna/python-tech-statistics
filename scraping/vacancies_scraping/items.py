# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Vacancy(scrapy.Item):
    company = scrapy.Field()
    tags = scrapy.Field()
    experience = scrapy.Field()
    salary = scrapy.Field()
    views = scrapy.Field()
    applications = scrapy.Field()
