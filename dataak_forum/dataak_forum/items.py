import scrapy


class DataakForumItem(scrapy.Item):

    subject = scrapy.Field()
    user = scrapy.Field()
    post = scrapy.Field()

