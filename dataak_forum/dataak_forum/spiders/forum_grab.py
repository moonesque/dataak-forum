# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest
from scrapy.loader import ItemLoader
from ..items import DataakForumItem


class ForumGrabSpider(scrapy.Spider):
    name = "forum-grab"
    allowed_domains = ["forum.dataak.com"]
    user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 ' \
                 'Safari/537.36 '

    # start_urls = (
    #     'http://forum.dataak.com',
    # )

    def start_requests(self):
        return [
            FormRequest(
                "http://forum.dataak.com/member.php?action=login",
                formdata={'action': 'do_login',
                          'quick_login': '1', 'my_post_key': 'ba5af38b9c7da114b0ad8181f56eb31b',
                          'quick_username': 'mahan', 'quick_password': '@123456', 'quick_remember': 'yes',
                          'submit': u'\u0648\u0631\u0648\u062f', 'url': 'http://forum.dataak.com/index.php'}
            )]

    def parse(self, response):
        item = ItemLoader(item=DataakForumItem(), response=response)

