import shelve
import os


class KVStoreShelve(object):
    def __init__(self, data_dir='', db_name=None, writeback=True):
        self.db_name = db_name or 'kv_database'
        self.file_path = os.path.join(data_dir, self.db_name)
        self.inst = None
        self.writeback = writeback

    def make_db_open(self):
        if self.inst is None:
            self.inst = shelve.open(self.file_path, writeback=self.writeback)

    def close(self):
        if self.inst:
            self.inst.close()
        self.inst = None

    def put(self, key, value):
        self.make_db_open()
        self.inst[key] = value
        self.inst.sync()

    def get(self, key):
        self.make_db_open()
        return self.inst[key]

    def __str__(self):
        self.make_db_open()
        return str(self.inst)


if __name__ == '__main__':
    kv = KVStoreShelve()
    print kv