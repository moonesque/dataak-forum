# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import FormRequest, Request
from scrapy.linkextractors import LinkExtractor

from ..items import DataakForumItem, ForumItem


class ForumGrabSpider(CrawlSpider):
    """
    This spider crawls every forum page on forum.dataak.com,
    scraping every post and every forum title.
    """
    name = "forum-grab"
    allowed_domains = ["forum.dataak.com"]
    user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 ' \
                 'Safari/537.36 '

    # Rules used to extract urls, vertically and horizontally
    rules = (
        Rule(LinkExtractor(restrict_xpaths='//td/strong/a'), follow=True, callback='parse_forum'),
        Rule(LinkExtractor(restrict_xpaths='//a[@class="pagination_next"][1]'), follow=True, callback='parse_thread'),
        Rule(LinkExtractor(restrict_xpaths='//span[@class=" subject_old" or @class=" subject_new" or '
                                           '@class="subject_editable subject_old"]/a'),
             follow=True, callback='parse_thread'),
    )

    def start_requests(self):
        """
        GET request to the login page to get the login form,
        the callback method handles login process.
        """
        return [
            Request(
                'http://forum.dataak.com/member.php?action=login',
                callback=self.parse_login

            )
        ]

    def parse_login(self, response):
        """
        POST request to the login page, providing credentials
        """
        return FormRequest.from_response(
            response,
            formnumber=1,
            formdata={'quick_username': 'mahan', 'quick_password': '@123456'},
        )

    def parse_thread(self, response):
        """
        Thread parser, yielding items populated with thread details
        """
        item = DataakForumItem()

        # xpath selectors
        thread = '//span[@class="active"]/text()'
        navpath = '//div[@class="navigation"]/a/text()'
        posts = '//div[@class="post "]'
        # author_not_admin = '//div[@class="author_information"]//a/text()'
        author = './/div[@class="author_information"]//a/text() | .//div[@class="author_information"]//em/text()'
        body = './/div[@class="post_body scaleimages"]/text() | .//div[@class="post_body scaleimages"]//*/text()'

        posts_selector = response.xpath(posts)
        for post in posts_selector:
            item['url'] = response.url
            # self.log(response.url)

            item['thread'] = response.xpath(thread).extract_first()
            # self.log("thread: %s" % response.xpath(thread).extract())

            # get the last item which is the forum name
            item['forum'] = response.xpath(navpath).extract()[-1]
            # self.log("nav path: %s" % response.xpath(navpath).extract())

            item['author'] = post.xpath(author).extract_first()
            # self.log("author: %s" % post.xpath(author).extract())

            item['body'] = post.xpath(body).extract()
            # self.log("body: %s" % post.xpath(body).extract())

            yield item

    def parse_forum(self, response):
        """
        Forum parser, yielding items populated with forum names
        """

        item = ForumItem()
        item['forum'] = response.xpath('//span[@class="active"]/text()').extract_first()
        yield item

