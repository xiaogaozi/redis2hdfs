#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
import argparse
import re
import subprocess
import tempfile

import redis
import webhdfs

from redis2hdfs import __version__

parser = argparse.ArgumentParser(description='Export Redis data to HDFS')
parser.add_argument('--version', action='version',
                    version='redis2hdfs {}'.format(__version__))
parser.add_argument('--redis-host', default='localhost',
                    help='Redis hostname (default: localhost)')
parser.add_argument('--redis-port', default=6379,
                    help='Redis port (default: 6379)')
parser.add_argument('--redis-db', default=0,
                    help='Redis database number (default: 0)')
parser.add_argument('--redis-key', required=True,
                    help='Redis key, support glob-style pattern, '
                         'e.g. *abc*')
parser.add_argument('--namenode-host', required=True, help='NameNode hostname')
parser.add_argument('--webhdfs-port', default=50070,
                    help='WebHDFS port of NameNode (default: 50070)')
parser.add_argument('--hdfs-username', required=True, help='HDFS username')
parser.add_argument('--hdfs-path', required=True,
                    help='HDFS file path to store data, '
                         'should be absolute path, e.g. '
                         '/user/redis/myzset.lzo')
parser.add_argument('--compress-format',
                    help='if specified output file will be compressed, '
                         'supported formats: lzo')


def is_glob_style_pattern(key):
    # globle-style pattern in this doc: http://redis.io/commands/keys
    if re.match(r'[\?\*\[\]]', key) is not None:
        return True
    else:
        return False


class Migrationer(object):
    """Migrate Redis data to HDFS"""

    def __init__(self, redis_host, redis_port, redis_db, redis_key,
                 namenode_host, webhdfs_port, hdfs_username, hdfs_path,
                 compress_format):
        self.redis_key = redis_key
        self.namenode_host = namenode_host
        self.webhdfs_port = webhdfs_port
        self.hdfs_path = hdfs_path
        self.compress_format = compress_format
        self.redis_client = redis.StrictRedis(host=redis_host, port=redis_port,
                                              db=redis_db)
        self.hdfs_client = webhdfs.webhdfs.WebHDFS(namenode_host, webhdfs_port,
                                                   hdfs_username)

    def get_all_redis_keys(self):
        if is_glob_style_pattern(self.redis_key):
            keys = set()
            for k in self.redis_client.scan_iter(match=self.redis_key,
                                                 count=100):
                keys.add(k)
            self.hdfs_client.mkdir(self.hdfs_path)
        else:
            keys = set([self.redis_key])
        return keys

    def migrate_set(self, key):
        with tempfile.NamedTemporaryFile() as f:
            for member in self.redis_client.sscan_iter(key):
                f.write('{}\n'.format(member))
            f.flush()
            self.copy_from_local_to_hdfs(f.name, key)

    def migrate_hash(self, key):
        with tempfile.NamedTemporaryFile() as f:
            for field, value in self.redis_client.hscan_iter(key):
                f.write('{} {}\n'.format(field, value))
            f.flush()
            self.copy_from_local_to_hdfs(f.name, key)

    def migrate_zset(self, key):
        with tempfile.NamedTemporaryFile() as f:
            for member, score in self.redis_client.zscan_iter(key):
                f.write('{} {}\n'.format(member, score))
            f.flush()
            self.copy_from_local_to_hdfs(f.name, key)

    def copy_from_local_to_hdfs(self, local_path, key):
        if self.compress_format == 'lzo':
            print 'Compress {} using LZO'.format(local_path)
            subprocess.call('lzop -f {}'.format(local_path), shell=True)
            local_path = local_path + '.lzo'
        if is_glob_style_pattern(self.redis_key):
            remote_path = '{}/{}'.format(self.hdfs_path, key)
        else:
            remote_path = self.hdfs_path
        print 'Copy {} => webhdfs://{}:{}{}'.format(local_path,
                                                    self.namenode_host,
                                                    self.webhdfs_port,
                                                    remote_path)
        self.hdfs_client.copyFromLocal(local_path, remote_path)
        return remote_path


def main():
    """Main progress."""
    args = parser.parse_args()
    migrationer = Migrationer(args.redis_host, args.redis_port, args.redis_db,
                              args.redis_key, args.namenode_host,
                              args.webhdfs_port, args.hdfs_username,
                              args.hdfs_path, args.compress_format)
    for key in migrationer.get_all_redis_keys():
        key_type = migrationer.redis_client.type(key)
        if key_type == 'set':
            migrationer.migrate_set(key)
        elif key_type == 'hash':
            migrationer.migrate_hash(key)
        elif key_type == 'zset':
            migrationer.migrate_zset(key)
        else:
            print 'Unsupported Redis key type: {}'.format(key)

if __name__ == "__main__":
    main()
