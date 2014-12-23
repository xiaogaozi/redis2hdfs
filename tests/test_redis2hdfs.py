# -*- coding: utf-8 -*-

import unittest

from mock import patch
from mockredis import mock_strict_redis_client

from redis2hdfs import redis2hdfs


class DummyWebHDFS(object):

    def __init__(self, *args, **kwargs):
        pass

    def mkdir(self, *args, **kwargs):
        pass

    def copyFromLocal(self, *args, **kwargs):
        pass


class Redis2HDFSTest(unittest.TestCase):

    def _get_migrationer(self, args):
        return redis2hdfs.Migrationer(args.redis_host, args.redis_port,
                                      args.redis_db, args.redis_key,
                                      args.namenode_host,
                                      args.webhdfs_port,
                                      args.hdfs_username,
                                      args.hdfs_path,
                                      args.compress_format)

    def test_is_glob_style_pattern(self):
        r = redis2hdfs.is_glob_style_pattern('abc')
        self.assertFalse(r)
        r = redis2hdfs.is_glob_style_pattern('*abc*')
        self.assertTrue(r)
        r = redis2hdfs.is_glob_style_pattern('?abc')
        self.assertTrue(r)
        r = redis2hdfs.is_glob_style_pattern('[abc]')
        self.assertTrue(r)

    def test_with_empty_args(self):
        with self.assertRaises(SystemExit):
            redis2hdfs.parser.parse_args([])

    @patch('redis.StrictRedis', mock_strict_redis_client)
    @patch('webhdfs.webhdfs.WebHDFS', DummyWebHDFS)
    def test_get_all_redis_keys(self):
        # global-style pattern key
        args = redis2hdfs.parser.parse_args(['--redis-key', '*abc*',
                                             '--namenode-host', 'localhost',
                                             '--hdfs-username', 'hdfs',
                                             '--hdfs-path', '/user/hdfs/test'])
        migrationer = self._get_migrationer(args)
        migrationer.redis_client.mset({'abc1': 'a', '1abc': 'a'})
        keys = migrationer.get_all_redis_keys()
        self.assertSetEqual(keys, set(['abc1', '1abc']))

        # normal key
        args = redis2hdfs.parser.parse_args(['--redis-key', 'abc',
                                             '--namenode-host', 'localhost',
                                             '--hdfs-username', 'hdfs',
                                             '--hdfs-path', '/user/hdfs/test'])
        migrationer = self._get_migrationer(args)
        migrationer.redis_client.mset({'abc1': 'a', 'abc': 'a'})
        keys = migrationer.get_all_redis_keys()
        self.assertSetEqual(keys, set(['abc']))

    @patch('redis.StrictRedis', mock_strict_redis_client)
    @patch('webhdfs.webhdfs.WebHDFS', DummyWebHDFS)
    def test_copy_from_local_to_hdfs(self):
        # global-style pattern key
        args = redis2hdfs.parser.parse_args(['--redis-key', '*abc*',
                                             '--namenode-host', 'localhost',
                                             '--hdfs-username', 'hdfs',
                                             '--hdfs-path', '/user/hdfs/test'])
        migrationer = self._get_migrationer(args)
        remote_path = migrationer.copy_from_local_to_hdfs('', 'abc')
        self.assertEqual(remote_path, '/user/hdfs/test/abc')

        # normal key
        args = redis2hdfs.parser.parse_args(['--redis-key', 'abc',
                                             '--namenode-host', 'localhost',
                                             '--hdfs-username', 'hdfs',
                                             '--hdfs-path', '/user/hdfs/test'])
        migrationer = self._get_migrationer(args)
        remote_path = migrationer.copy_from_local_to_hdfs('', 'abc')
        self.assertEqual(remote_path, '/user/hdfs/test')
