import scrapy


class DataakForumItem(scrapy.Item):

    thread = scrapy.Field()
    author = scrapy.Field()
    body = scrapy.Field()
    url = scrapy.Field()
    navpath = scrapy.Field()

