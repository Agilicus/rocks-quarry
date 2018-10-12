import logging
import rocksdb

from rocks_quarry import arguments
from rocks_quarry.server import Server

def main():
    args = arguments.get_args()

    db = rocksdb.DB(args.data_dir, rocksdb.Options(create_if_missing=True))
    server = Server(db, args.port)
    server.run()
