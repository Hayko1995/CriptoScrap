# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3


class CriptoPipeline:
    def process_item(self, item, spider):
        return item


class SqlitePipeline:

    def __init__(self):

        # Create/Connect to database
        self.con = sqlite3.connect('demo.db')

        # Create cursor, used to execute commands
        self.cur = self.con.cursor()

        # Create quotes table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS coins(
            name TEXT,
            item TEXT,
            depositAPY TEXT,
            borrowAPY TEXT
        )
        """)

    def process_item(self, item, spider):
        print("🐍 File: cripto/pipelines.py | Line: 38 | __init__ ~ item",item)

        if (not 'depositAPY' in item):
            item['depositAPY'] = ''
        if (not 'borrowAPY' in item):
            item['borrowAPY'] = ''

        # Check to see if text is already in database
        self.cur.execute(
            "select * from coins where name = ? and item = ?", (item['name'], item['item']))
        result = self.cur.fetchone()
        if result:
            if (item['depositAPY'] == ''):
                item['depositAPY'] = result[2]
            if (item['borrowAPY'] == ''):
                item['borrowAPY'] = result[3]

            self.cur.execute('''update coins set depositAPY=? , borrowAPY=? where name == ? and item = ?''',
                             (

                                item['depositAPY'],
                                item['borrowAPY'],
                                item['name'],
                                item['item']
                             ))

            # Execute insert of data into database
            self.con.commit()

        # If text isn't in the DB, insert data
        else:

            # Define insert statement
            self.cur.execute("""
                INSERT INTO coins (name, item, depositAPY, borrowAPY) VALUES (?, ?, ?, ?)
            """,
                             (
                                 item['name'],
                                 item['item'],
                                 item['depositAPY'],
                                 item['borrowAPY']
                             ))

            # Execute insert of data into database
            self.con.commit()

        return item
