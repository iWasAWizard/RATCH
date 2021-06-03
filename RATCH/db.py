import time
import psycopg2

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
                self.connect(5)
            self.cur = self.conn.cursor()
        return self.cur

    def init(self):
        self.connect()
        self.cursor()

    def connect(self):
        if not self.conn:
            retry_counter = 0
            try:
                self.conn = psycopg2.connect(user=self.user,
                                             password=self.password,
                                             host=self.host,
                                             port=self.port,
                                             database=self.db,
                                             connect_timeout=5)
                self.conn.autocommit = True
            except psycopg2.OperationalError as e:
                if not self.reconnect or retry_counter >= RETRY_LIMIT:
                    raise e
                retry_counter += 1
                time.sleep(5)
                self.connect()
            except (Exception, psycopg2.Error) as e:
                raise e

    def query(self, query, args=(), one=False):
        cur = self.cur
        cur.execute(query, args)
        r = [dict((cur.description[i][0], value)
                  for i, value in enumerate(row)) for row in cur.fetchall()]
        cur.connection.close()
        return (r[0] if r else None) if one else r
