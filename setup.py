from setuptools import setup
import pypandoc

long_description = pypandoc.convert('README.md', 'rst')

def find_version(filename):
    with open(filename) as f:
        for line in f:
            if line.startswith('__version__'):
                return eval(line.split('=')[-1])

setup(
    name='unzipmbcs',
    version=find_version('unzipmbcs.py'),
    description='UnZip for non-UTF8 encoding such as cp949, sjis, gbk, euc-kr, euc-jp, and gb2312',
    long_description=long_description,
    keywords='unzip, pkzip, non-UTF8, mbcs, cp949, sjis, shift_jis, gbk, gb18030',
    author='Joo-Won Jung',
    author_email='sanori@gmail.com',
    url='https://github.com/sanori/unzip-mbcs',
    py_modules=['unzipmbcs'],
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: OSI Approved :: Apache Software License',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 3'],
    entry_points={
        'console_scripts': [
            'unzipmbcs = unzipmbcs:_main',
        ],
    },
)
