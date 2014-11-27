#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
import argparse
import tempfile

import redis
from webhdfs.webhdfs import WebHDFS

from redis2hdfs import __version__

parser = argparse.ArgumentParser(description='Export Redis data to HDFS')
parser.add_argument('--version', action='version',
                    version='redis2hdfs %s' % __version__)
parser.add_argument('--redis-host', default='localhost',
                    help='Redis hostname (default: localhost)')
parser.add_argument('--redis-port', default=6379,
                    help='Redis port (default: 6379)')
parser.add_argument('--redis-db', default=0,
                    help='Redis database number (default: 0)')
parser.add_argument('--redis-key', required=True, help='Redis key')
parser.add_argument('--namenode-host', required=True, help='NameNode hostname')
parser.add_argument('--webhdfs-port', default=50070,
                    help='WebHDFS port of NameNode (default: 50070)')
parser.add_argument('--hdfs-username', required=True, help='HDFS username')
parser.add_argument('--hdfs-path', required=True,
                    help='HDFS file path to store data, '
                         'should be absolute path')
args = parser.parse_args()

redis_client = redis.StrictRedis(host=args.redis_host,
                                 port=args.redis_port,
                                 db=args.redis_db)
hdfs_client = WebHDFS(args.namenode_host, args.webhdfs_port,
                      args.hdfs_username)


def copy_from_local_to_hdfs(local_path):
    print 'Copy {} => webhdfs://{}:{}{}'.format(local_path, args.namenode_host,
                                                args.webhdfs_port,
                                                args.hdfs_path)
    hdfs_client.copyFromLocal(local_path, args.hdfs_path)


def migrate_set():
    with tempfile.NamedTemporaryFile() as f:
        for member in redis_client.sscan_iter(args.redis_key):
            f.write('{}\n'.format(member))
        f.flush()
        copy_from_local_to_hdfs(f.name)


def migrate_hash():
    with tempfile.NamedTemporaryFile() as f:
        for field, value in redis_client.hscan_iter(args.redis_key):
            f.write('{} {}\n'.format(field, value))
        f.flush()
        copy_from_local_to_hdfs(f.name)


def migrate_zset():
    with tempfile.NamedTemporaryFile() as f:
        for member, score in redis_client.zscan_iter(args.redis_key):
            f.write('{} {}\n'.format(member, score))
        f.flush()
        copy_from_local_to_hdfs(f.name)


def main():
    """Main progress."""
    key_type = redis_client.type(args.redis_key)
    if key_type == 'set':
        migrate_set()
    elif key_type == 'hash':
        migrate_hash()
    elif key_type == 'zset':
        migrate_zset()
    else:
        print 'Unsupported Redis key type'

if __name__ == "__main__":
    main()
