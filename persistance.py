import sqlite3
import json
from time import strftime

class Sqlite():

    def __init__(self, db, table):
        self.conn = sqlite3.connect(db, check_same_thread=False)
        self.table = table
        self.setup(table)

    def now(self):
        return strftime("%Y-%m-%d-%H-%M-%S")

    def transform(self, result):
        id, data, updated_on, created_on = result
        res = json.loads(data)
        res.update(dict(id=id, created_on=created_on, updated_on=updated_on))
        return res

    def setup(self, table):
        create_table = '''
        CREATE TABLE IF NOT EXISTS
        {table} (
          id integer primary key autoincrement,
          data text,
          updated_on text,
          created_on text
        )'''.format(table=table)
        cursor = self.conn.cursor()
        cursor.execute(create_table)
        self.conn.commit()


    def get(self, id):
        cursor = self.conn.cursor()
        query = "select * from {table} where id = (?) limit 1".format(table=self.table)
        results = list(cursor.execute(query, (id, )))
        if len(results) == 0:
            return None
        return self.transform(results[0])
        id, data, updated_on, created_on = results[0]
        result = json.loads(data)
        result.update(dict(id=id, created_on=created_on, updated_on=updated_on))
        return result

    def add(self, item):
        cursor = self.conn.cursor()
        query = '''
        INSERT into
        {table} (data, updated_on, created_on)
        VALUES (?, ?, ?)
        '''.format(table=self.table)
        created_on = self.now()
        updated_on = self.now()
        data = json.dumps(item)
        cursor.execute(query, (data, updated_on, created_on))
        self.conn.commit()
        [(id,)] = list(self.conn.execute("select last_insert_rowid()"))
        result = item.copy()
        result.update(id=id, updated_on=updated_on, created_on=created_on)
        return result


    def update(self, id, item):
        cursor = self.conn.cursor()
        data = item.copy()

        if ('id' in data):
            del data['id']
        if ('created_on' in data):
            del data['created_on']
        if ('updated_on' in data):
            del data['updated_on']

        updated_on = self.now()

        query = '''
        UPDATE
        {table}
        SET
        data = (?),
        updated_on = (?)
        WHERE id = (?)
        '''.format(table=self.table)

        result = cursor.execute(query, (json.dumps(data), updated_on, id))
        self.conn.commit()
        return True if cursor.rowcount else False


    def delete(self, id):
        cursor = self.conn.cursor()

        query = '''
        DELETE from
        {table}
        WHERE id = (?)
        '''.format(table=self.table)


        result = cursor.execute(query, (id, ))
        self.conn.commit()
        return True if cursor.rowcount else False


    def list(self):
        query = '''
        SELECT *
        FROM {table}
        '''.format(table=self.table)

        cursor = self.conn.cursor()
        return list(map(self.transform, cursor.execute(query)))

