# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobOpeningItem(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    company = scrapy.Field()
    department = scrapy.Field()
    location = scrapy.Field()
    description = scrapy.Field()
    requirements = scrapy.Field()
    link = scrapy.Field()

    def __repr__(self):
        """only print out title after exiting the Pipeline"""
        return repr({"title": self['title']})
