# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3
import psycopg2
import os


class CriptoPipeline:
    def process_item(self, item, spider):
        return item


class SqlitePipeline:

    def __init__(self):
        hostname = os.environ.get('POSTGRES_HOST')
        username = os.environ.get('POSTGRES_USER')
        password = os.environ.get('POSTGRES_PASSWORD')
        database = os.environ.get('POSTGRES_DATABASE')
        port = os.environ.get('POSTGRES_PORT')
        self.connection = psycopg2.connect(
            host=hostname, user=username, password=password, port=port, dbname=database)

        # Create/Connect to database
        # self.con = sqlite3.connect('../demo.db')

        # Create cursor, used to execute commands
        self.cur = self.connection.cursor()

        # Create quotes table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS coins(
            name text,
            item text,
            deposit text,
            borrow text
        )
        """)

    def process_item(self, item, spider):
        if (not 'deposit' in item):
            item['deposit'] = ''
        if (not 'borrow' in item):
            item['borrow'] = ''

        # Check to see if text is already in database
        self.cur.execute(
            "select * from coins where name = %s and item = %s", (item['name'], item['item']))
        result = self.cur.fetchone()
        if result:
            if (item['deposit'] == ''):
                item['deposit'] = result[3]
            if (item['borrow'] == ''):
                item['borrow'] = result[4]

            self.cur.execute('update coins set deposit=%s , borrow=%s where name =%s and item =%s',
                             (
                                 item['deposit'],
                                 item['borrow'],
                                 item['name'],
                                 item['item']
                             ))

            # Execute insert of data into database
            self.connection.commit()

        # If text isn't in the DB, insert data
        else:
            # Define insert statement
            self.cur.execute("INSERT INTO coins (name, item, deposit, borrow) VALUES ( %s, %s, %s, %s)",
                             (
                                 item['name'],
                                 item['item'],
                                 item['deposit'],
                                 item['borrow']
                             ))

            # Execute insert of data into database
            self.connection.commit()

        return item
