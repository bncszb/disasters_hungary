# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class EventsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    event_url=scrapy.Field()
    event_id=scrapy.Field()
    event_date=scrapy.Field()
    categoryCode=scrapy.Field()
    categoryName=scrapy.Field()
    subCategoryCode=scrapy.Field()
    subCategoryName=scrapy.Field()
    title=scrapy.Field()
    subtitle=scrapy.Field()
    content=scrapy.Field()
    location=scrapy.Field()
    latitude=scrapy.Field()
    longitude=scrapy.Field()
    counties=scrapy.Field()
    districts=scrapy.Field()
    update_info=scrapy.Field()
