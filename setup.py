# -*- coding: utf-8 -*-

from setuptools import find_packages, setup
from redis2hdfs import __version__

setup(
    name='redis2hdfs',
    version=__version__,
    url='https://github.com/xiaogaozi/redis2hdfs',
    license='MIT License',
    description='Export Redis data to HDFS',
    long_description=open('README.md').read(),
    author='xiaogaozi',
    author_email='gaochangjian@gmail.com',
    packages=find_packages(exclude=['tests']),
    package_data={'redis2hdfs': ['CHANGES', 'README.md', 'tests-req.txt']},
    zip_safe=False,
    install_requires=[
        'WebHDFS',
        'redis',
    ],
    tests_require=open('tests-req.txt').readlines(),
    entry_points={
        'console_scripts': [
            'redis2hdfs = redis2hdfs.redis2hdfs:main'
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Utilities',
    ],
)
