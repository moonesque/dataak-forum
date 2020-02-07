import scrapy


class DataakForumItem(scrapy.Item):
    thread = scrapy.Field()
    author = scrapy.Field()
    body = scrapy.Field()
    url = scrapy.Field()
    forum = scrapy.Field()


class ForumItem(scrapy.Item):
    forum = scrapy.Field()
