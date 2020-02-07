# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from sqlalchemy.orm import sessionmaker
from .models import Threads, Posts, Forums, db_connect, create_table


class DataakForumPipeline(object):
    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """Save deals in the database.

        This method is called for every item pipeline component.
        """
        session = self.Session()

        if item.get('url'):

            forumdb = Forums()
            # forumdb.forum

            threaddb = Threads()
            threaddb.thread = item["thread"]
            threaddb.forum = item["forum"]
        #     threaddb.url = item["url"]
        #
        #     try:
        #         session.add(threaddb)
        #         session.commit()
        #     except:
        #         session.rollback()
        #     raise
        # finally:
        #     session.close()
        #
        # return item
