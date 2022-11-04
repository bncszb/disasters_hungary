# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3

class EventsPipeline:

    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn=sqlite3.connect("database/events.db")
        self.curs=self.conn.cursor()

    def create_table(self):
        self.curs.execute("""drop table if exists events_table""")
        self.curs.execute("""create table events_table(
            title text,
            date text,
            category text,
            url text)
            """)
    def process_item(self, item, spider):

        self.store_db(item)
        return item

    def store_db(self, item):
        self.curs.execute(f"""insert into events_table values (\"{item['title']}\",\"{item['date']}\",\"{item['category']}\",\"{item['url']}\")""")
        self.conn.commit()