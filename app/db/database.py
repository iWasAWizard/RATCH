import os
import json
import time
import logging
import psycopg2
from psycopg2 import NamedTupleCursor

RETRY_LIMIT = 5

class Database():
    def __init__(self, host, db='ratch_db', user='ratch_user',
                 password='ratch_pass'):
        self.host = host
        self.db = db
        self.user = user
        self.password = password
        self.port = '5432'
        self.conn = None
        self.cur = None
        self.reconnect = True

    def cursor(self):
        if not self.cur or self.cur.closed:
            if not self.conn:
                self.connect()
            self.cur = self.conn.cursor(cursor_factory=NamedTupleCursor)
        return self.cur

    def init(self):
        self.connect()
        self.cursor()

    def connect(self):
        if not self.conn:
            try:
                self.conn = psycopg2.connect(user=self.user,
                                             password=self.password,
                                             host=self.host,
                                             port=self.port,
                                             database=self.db,
                                             connect_timeout=5)
                retry_counter = 0
                self.conn.autocommit = True
            except psycopg2.OperationalError as e:
                if not self.reconnect or self.retry_counter >= RETRY_LIMIT:
                    raise e
                retry_counter += 1
                time.sleep(5)
                self.connect(retry_counter)
            except (Exception, psycopg2.Error) as e:
                raise e