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
        self.con = sqlite3.connect('../demo.db')

        # Create cursor, used to execute commands
        self.cur = self.con.cursor()

        # Create quotes table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS app_coins(
            name TEXT,
            item TEXT,
            depositAPY TEXT,
            borrowAPY TEXT
        )
        """)

    def process_item(self, item, spider):
        if (not 'depositAPY' in item):
            item['depositAPY'] = ''
        if (not 'borrowAPY' in item):
            item['borrowAPY'] = ''

        print("🐍 File: cripto/pipelines.py | Line: 42 | process_item ~ item", item)

        # Check to see if text is already in database
        self.cur.execute(
            "select * from app_coins where name = ? and item = ?", (item['name'], item['item']))
        result = self.cur.fetchone()
        if result:
            print("🐍 File: cripto/pipelines.py | Line: 50 | process_item ~ result",result)
            if (item['depositAPY'] == ''):
                item['depositAPY'] = result[3]
            if (item['borrowAPY'] == ''):
                item['borrowAPY'] = result[4]
                print("🐍 File: cripto/pipelines.py | Line: 55 | process_item ~ result[3]",result[3])

            self.cur.execute('''update app_coins set depositAPY=? , borrowAPY=? where name == ? and item = ?''',
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
                INSERT INTO app_coins (name, item, depositAPY, borrowAPY) VALUES (?, ?, ?, ?)
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
