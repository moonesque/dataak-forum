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
        """

        This method is called for every item pipeline component.
        """
        session = self.Session()

        if item.get('url'):
            thread = session.query(Threads).filter_by(url=item['url']).first()
            if not thread:
                thread = Threads(thread=item['thread'], forum=item['forum'], url=item['url'])
                session.add(thread)
                session.commit()

            postdb = Posts(thread_id=thread.id)
            postdb.body = ''.join(item['body'])
            postdb.author = item['author']

            try:
                session.add(thread)
                session.add(postdb)
                session.commit()
            except:
                session.rollback()
                raise
            finally:
                session.close()
            return item

        elif item.get('forum'):
            forumdb = Forums()
            forumdb.forum = item['forum']
            try:
                session.add(forumdb)
                session.commit()
            except:
                session.rollback()
                raise
            finally:
                session.close()
            return item
