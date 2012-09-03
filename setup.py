#!/usr/bin/env python
from setuptools import setup, find_packages
import langkawi

METADATA = dict(
    name='langkawi',
    version=langkawi.__version__,
    author='Jason Gao',
    author_email='gaopeng@tukeq.com',
    description='Django app providing registration through a variety of APIs',
    long_description=open('README.md').read(),
    url='http://github.com/tyrchen/langkawi',
    keywords='django weibo tencent renren douban oauth2',
    packages=['langkawi'],
    install_requires=['requests', 'requests_oauth2'],
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Environment :: Web Environment',
        'Topic :: Internet',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    zip_safe=False,
    #packages=find_packages(),
)

if __name__ == '__main__':
    setup(**METADATA)

