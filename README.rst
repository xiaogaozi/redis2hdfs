redis2hdfs
==========

.. image:: https://img.shields.io/travis/xiaogaozi/redis2hdfs.svg?style=flat
   :target: https://travis-ci.org/xiaogaozi/redis2hdfs
   :alt: Build Status

.. image:: https://pypip.in/version/redis2hdfs/badge.svg?style=flat
   :target: https://pypi.python.org/pypi/redis2hdfs
   :alt: Latest Version

.. image:: https://pypip.in/py_versions/redis2hdfs/badge.svg?style=flat
   :target: https://pypi.python.org/pypi/redis2hdfs
   :alt: Supported Python versions

.. image:: https://pypip.in/status/redis2hdfs/badge.svg?style=flat
   :target: https://pypi.python.org/pypi/redis2hdfs
   :alt: Development Status

.. image:: https://pypip.in/license/redis2hdfs/badge.svg?style=flat
   :target: https://pypi.python.org/pypi/redis2hdfs
   :alt: License

redis2hdfs is a command line tool to help you export Redis data to HDFS. It use `SCAN <http://redis.io/commands/scan>`_ related commands to iterate elements (no ``KEYS``), so you can use in production safely.

NOTE: ensure WebHDFS is enabled.

Installation
------------

::

    $ pip install redis2hdfs

Usage
-----

::

    $ redis2hdfs --redis-key myzset --namenode-host namenode.example.com --hdfs-username hdfs --hdfs-path /tmp/myzset.lzo --compress-format lzo

redis2hdfs could compress file before copy to HDFS, through ``--compress-format`` option. Currently supported compress formats are: LZO.

If you want to use LZO format, you need install `lzop <http://www.lzop.org>`_ first.

redis2hdfs supports `Redis global-style key pattern <http://redis.io/commands/keys>`_, so you can specify ``--redis-key`` like ``*abc*``. redis2hdfs will copy all matched keys' data to HDFS, at this time the ``--hdfs-path`` option will be the parent directory to store data.

For more information, just run ``redis2hdfs --help``.

Development
-----------

::

    $ mkvirtualenv redis2hdfs
    $ python setup.py develop
    $ pip install -r tests-req.txt
    $ nosetests -v
