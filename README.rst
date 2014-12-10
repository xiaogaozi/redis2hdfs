redis2hdfs
==========

.. image:: https://pypip.in/version/redis2hdfs/badge.svg
    :target: https://pypi.python.org/pypi/redis2hdfs
    :alt: Latest Version

.. image:: https://pypip.in/py_versions/redis2hdfs/badge.svg
    :target: https://pypi.python.org/pypi/redis2hdfs
    :alt: Supported Python versions

.. image:: https://pypip.in/status/redis2hdfs/badge.svg
    :target: https://pypi.python.org/pypi/redis2hdfs
    :alt: Development Status

.. image:: https://pypip.in/license/redis2hdfs/badge.svg
    :target: https://pypi.python.org/pypi/redis2hdfs
    :alt: License

redis2hdfs is a command line tool to help you export Redis data to HDFS.

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

Development
-----------

::

    $ mkvirtualenv redis2hdfs
    $ python setup.py develop
