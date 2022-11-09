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
            event_id text,
            event_date text,
            categoryCode text,
            categoryName text,
            subCategoryCode text,
            subCategoryName text,
            title text,
            subtitle text,
            content text,
            location text,
            latitude text,
            longitude text,
            counties text,
            districts text,
            update_info text,
            event_url text)
            """)
    def process_item(self, item, spider):

        self.store_db(item)
        return item

    def store_db(self, item):
        if len(item)>0:
            outp="(?"+", ?"*(len(item)-1)+")"
            self.curs.execute(f"""insert into events_table ({','.join([str(k) for k in item])}) values {outp}""", [str(v) for v in item.values()])
            self.conn.commit()