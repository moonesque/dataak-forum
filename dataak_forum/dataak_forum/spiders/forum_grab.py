# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import FormRequest, Request
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader

from ..items import DataakForumItem, ForumItem


class ForumGrabSpider(CrawlSpider):
    name = "forum-grab"
    allowed_domains = ["forum.dataak.com"]
    user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 ' \
                 'Safari/537.36 '

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//td/strong/a'), follow=True, callback='parse_forum'),
        Rule(LinkExtractor(restrict_xpaths='//a[@class="pagination_next"][1]'), follow=True, callback='parse_thread'),
        Rule(LinkExtractor(restrict_xpaths='//span[@class=" subject_old" or @class=" subject_new" or '
                                           '@class="subject_editable subject_old"]/a'),
             follow=True, callback='parse_thread'),
    )

    def start_requests(self):
        return [
            Request(
                'http://forum.dataak.com/member.php?action=login',
                callback=self.parse_login

            )
        ]

    def parse_login(self, response):
        return FormRequest.from_response(
            response,
            formnumber=1,
            formdata={'quick_username': 'mahan', 'quick_password': '@123456'},
            # callback=self.after_login
        )

    # def after_login(self, response, **kwargs):
    #     forum_obj = response.xpath('//td/strong/a')
    #     for f in forum_obj:
    #         yield Request(f.extract(), callback=self.after_login, cb_kwargs={'forums': forums})

    def parse_thread(self, response):
        item = DataakForumItem()

        # self.log("thread: %s" % response.xpath(
        #     '//span[@class="active"]/text()').extract())
        # a = input("Something?")

        thread = '//span[@class="active"]/text()'
        navpath = '//div[@class="navigation"]/a/text()'
        posts = '//div[@class="post "]'
        author_not_admin = '//div[@class="author_information"]//a/text()'
        author = './/div[@class="author_information"]//a/text() | .//div[@class="author_information"]//em/text()'
        body = './/div[@class="post_body scaleimages"]/text() | .//div[@class="post_body scaleimages"]//*/text()'

        posts_selector = response.xpath(posts)
        for post in posts_selector:
            item['url'] = response.url
            self.log(response.url)

            item['thread'] = response.xpath(thread).extract_first()
            self.log("thread: %s" % response.xpath(thread).extract())

            item['forum'] = response.xpath(navpath).extract()[-1]  # get the last item which is the forum name
            self.log("nav path: %s" % response.xpath(navpath).extract())

            item['author'] = post.xpath(author).extract_first()
            self.log("author: %s" % post.xpath(author).extract())

            item['body'] = post.xpath(body).extract()
            self.log("body: %s" % post.xpath(body).extract())

            yield item

    def parse_forum(self, response):

        item = ForumItem()
        item['forum'] = response.xpath('//span[@class="active"]/text()').extract_first()
        yield item

