# UnZip for non-UTF8 encoding
Extract zip files that MBCS(multi-byte character set) encoded file names,
such as ZIP files created in MS Windows, especially East Asian environment.

Major non-UTF8 encodings by languages:
 * Korean: cp949, euc-kr
 * Japanese: sjis (shift_jis), cp932, euc-jp
 * Chinese: gbk, gb18030, gb2312, cp936, hkscs, big5, cp950

## Install
```
pip install unzipmbcs
```

## CLI Usage
```
usage: unzipmbcs [-h] [-e ENCODING] cmd zipfile [target [target ...]]

unzip for non-UTF8 filenames in zip archive

positional arguments:
  cmd                   commands: l(list), x(extract)
  zipfile               .zip file to unzip
  target                file prefix to extract

optional arguments:
  -h, --help            show this help message and exit
  -e ENCODING, --encoding ENCODING
                        character encoding of filename in the .zip
```


## API
### listZip(filename, encoding='utf-8')
Return the information of the files in zip archive `filename`
with character `encoding`

### extractZip(filename, encoding='utf-8', filters=None)
Extract files in zip archive `filename` on current directory.
Assume that the file names in zip archive are encoded as `encoding`.
Only the files prefixed the values of `filters` list are extracted
if `filters` are provided.

### fixZipFilename(filename, enc)
Fix `filename` as UNICODE string which is originally encoded as `enc`.
Works for both Python 2 and 3.


## Motivation
The .ZIP format, PKZIP compression, have been widely used. Some valuable data are archived as .zip file.
But, in non-ASCII, non-Western environment, it makes trouble due to filenames.

Since ZIP format was created too old (1993), there is no standard character encoding about the file name of zip archive entries.
Most of zip file entries are encoded as legacy character encoding, local charset.

In modern UNICODE based environment or global data processing environment such as Linux, this makes inconvinience, less portability, mangled file names, fail to extract the file, and so on.

This module may mitigate the inconviniences.
