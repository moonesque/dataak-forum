# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import FormRequest, Request
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader

from ..items import DataakForumItem


class ForumGrabSpider(CrawlSpider):
    name = "forum-grab"
    allowed_domains = ["forum.dataak.com"]
    user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 ' \
                 'Safari/537.36 '

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//td/strong/a')),
        Rule(LinkExtractor(restrict_xpaths='//a[@class="pagination_next"])')),
        Rule(LinkExtractor(restrict_xpaths='//span[@class=" subject_old"]/a'), follow=True, callback='parse_thread'),
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
            callback=self.after_login
        )

    # def after_login(self, response):
    #     with open('myfile.html', 'w') as f:
    #         f.write(response.body)

    def parse_thread(self, response):
        pass




    def parse(self, response):
        item = ItemLoader(item=DataakForumItem(), response=response)

