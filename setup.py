from distutils.core import setup
setup(
    name='unzipmbcs',
    py_modules=['unzipmbcs'],
    version='0.1.1',
    description='UnZip for non-UTF8 encoding such as cp949, sjis, gbk, euc-kr, euc-jp, and gb2312',
    author='Joo-Won Jung',
    author_email='sanori@gmail.com',
    url='https://github.com/sanori/unzip-mbcs',
    download_url='https://github.com/sanori/unzip-mbcs/tarball/0.1.1',
    keywords=['unzip', 'pkzip', 'non-UTF8', 'mbcs', 'cp949',
              'sjis', 'shift_jis', 'gbk', 'gb18030'],
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: OSI Approved :: Apache Software License',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 3'],
    entry_points={
        'console_scripts': [
            'unzipmbcs=unzipmbcs:_main',
        ],
    },
)
