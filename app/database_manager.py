import sqlite3
import threading
import queue

class DatabaseManager:
    def __init__(self, db_file):
        self.lock = threading.Lock()
        self.db_file = db_file
        self.connection_pool = queue.Queue(maxsize=10)

    def __enter__(self):
        if self.connection_pool.qsize() < 10:
            connection = sqlite3.connect(self.db_file, check_same_thread=False)
            self.connection_pool.put(connection)
        return self.connection_pool.get()

    def __exit__(self, exc_type, exc_value, traceback):
        connection = self.get_connection()
        self.release_connection(connection)

    def get_connection(self):
        if self.connection_pool.qsize() < 10:
            connection = sqlite3.connect(self.db_file, check_same_thread=False)
            self.connection_pool.put(connection)
        return self.connection_pool.get()

    def release_connection(self, connection):
        self.connection_pool.put(connection)

    def execute(self, query, args=None):
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            with self.lock:
                if args:
                    cursor.execute(query, args)
                else:
                    cursor.execute(query)
        except Exception as e:
            connection.rollback()
            print(e)
        else:
            return cursor
        finally:
            self.release_connection(connection)