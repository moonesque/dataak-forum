import scrapy


class DataakForumItem(scrapy.Item):
    """
    This item will be populated with details of a post,
    each field pointing to it's respective namesake.
    """

    thread = scrapy.Field()
    author = scrapy.Field()
    body = scrapy.Field()
    url = scrapy.Field()
    forum = scrapy.Field()


class ForumItem(scrapy.Item):
    """
    This item will be populated with a forum name
    """
    forum = scrapy.Field()
