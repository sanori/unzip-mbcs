#! python
######################## BEGIN LICENSE BLOCK ########################
# Copyright 2016 Joo-Won Jung
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
######################### END LICENSE BLOCK #########################
"""
UnZip for non-UTF8 encoding

Extract zip files that MBCS(multi-byte character set) encoded file names,
such as ZIP files created in MS Windows, especially East Asian environment.
"""
import sys
import os
import zipfile
import zlib
import argparse

def fixZipFilename(filename, enc):
    """
    Fix `filename` as UNICODE string which is originally encoded as `enc`.
    Works for both Python 2 and 3.
    """
    if sys.version_info[0] == 2:
        bstr = filename
    else:
        bstr = bytes(filename, 'cp437')

    try:
        result = bstr.decode(enc)
    except UnicodeDecodeError as e:
        # try to fix sjis backslash -> slash conversion
        if enc == 'sjis' and bstr[e.start + 1] == '/':
            bstr[e.start + 1] = '\\'
            result = bstr.decode()
        else:
            raise e
    return result


def _extractFileFromZip(z, fn, ofn):
    """
    extract a file `fn` in ZipFile `z` as `ofn`
    """
    f = open(ofn, 'wb')
    f.write(z.read(fn))
    f.close()


def extractZip(filename, encoding='utf-8', filters=None):
    """
    Extract files in zip archive `filename` on current directory.
    Assume that the file names in zip archive are encoded as `encoding`.
    Only the files prefixed the values of `filters` list are extracted
    if `filters` are provided.
    """
    z = zipfile.ZipFile(filename, 'r')
    l = z.namelist()
    for fn in l:
        if len(fn) == 0 or fn[-1] == '/':
            continue
        try:
            ofn = fixZipFilename(fn, encoding)
        except UnicodeDecodeError as e:
            print('Decode error. Continue')
            ofn = fn
        if filters and (not ofn.startswith(tuple(filters))):
            continue
        if ofn[0] == '/':
            ofn = ofn[1:]
        try:
            print('Extracting %s...' % ofn)
        except UnicodeEncodeError as e:
            print(e)
            print('Continue to extract...')
        try:
            _extractFileFromZip(z, fn, ofn)
        except IOError:
            # create directories
            l2 = ofn.split('/')
            p = ""
            for dirs in l2[:-1]:
                p += dirs
                try:
                    os.mkdir(p)
                except OSError:
                    pass
                p += '/'
            _extractFileFromZip(z, fn, ofn)
        except (zlib.error, zipfile.BadZipfile):
            print('Error in file', ofn, '. Continue')
    z.close()


def listZip(filename, encoding='utf-8'):
    """
    Return the information of the files in zip archive `filename`
    with character `encoding`
    """
    typestr = {zipfile.ZIP_STORED: 'stored',
               zipfile.ZIP_DEFLATED: 'deflated'}

    z = zipfile.ZipFile(filename, 'r')
    zil = z.infolist()
    return map(lambda zi: (
        fixZipFilename(zi.filename, encoding),
        zi.file_size,
        zi.date_time,
        typestr[zi.compress_type]
    ), zil)


def _main():
    parser = argparse.ArgumentParser(
        description='unzip for non-UTF8 filenames in zip archive')
    parser.add_argument('cmd', help='commands: l(list), x(extract)')
    parser.add_argument('-e', '--encoding',
                        help='character encoding of filename in the .zip',
                        default='utf-8')
    parser.add_argument('zipfile', help='.zip file to unzip')
    parser.add_argument('target', nargs='*',
                        help='file prefix to extract')
    args = parser.parse_args()

    if args.cmd == 'l':
        l = listZip(args.zipfile, encoding=args.encoding)
        print('  Length     Date    Time   Name')
        print('--------- ---------- ----- -----------')
        for entry in l:
            print('%9d %4d-%02d-%02d %02d:%02d %s'
                  % tuple([entry[1]] + list(entry[2][:-1]) + [entry[0]]))
    elif args.cmd == 'x':
        extractZip(args.zipfile, encoding=args.encoding,
                   filters=args.target)
    else:
        print('Unknown command:', args.cmd)

if __name__ == '__main__':
    _main()
