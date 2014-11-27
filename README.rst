redis2hdfs
==========

redis2hdfs is a command line tool to help you export Redis data to HDFS.

NOTE: ensure WebHDFS is enabled.

Installation
------------

::

    $ pip install redis2hdfs

Getting Started
---------------

::

    $ redis2hdfs --redis-key myzset --namenode-host namenode.example.com --hdfs-username hdfs --hdfs-path '/tmp/myzset'

Development
-----------

::

    $ mkvirtualenv redis2hdfs
    $ python setup.py develop
