# encoding: utf-8
import os
import os.path
import sys
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import unzipmbcs


class TestFromZip(unittest.TestCase):
    filename = 'NewFolder.zip'
    encoding = 'cp949'
    expected = [u'새 텍스트 문서.txt', u'새 폴더/', u'새 폴더/한글문서.txt']

    def testListZip(self):
        result = unzipmbcs.listZip(self.filename, self.encoding)
        self.assertEqual(list(map(lambda x: x[0], result)), self.expected)

    def testExtractZip(self):
        if (sys.getfilesystemencoding().lower() != 'utf-8') and (not os.environ.get('PYTHONIOENCODING')):
            print('Warning: non-UTF8 filesystem.',
                  'set PYTHONIOENCODING as your filesystem encoding!')
            return
        unzipmbcs.extractZip(self.filename, self.encoding)
        map(lambda x: self.assertTrue(os.path.exists(x), x + ' not exist'),
            self.expected)

        # clean-up
        files = list(self.expected)   # clone the list
        files.reverse()
        for f in files:
            if (os.path.isfile(f)):
                os.remove(f)
            else:
                os.rmdir(f)

class TestEncryptedZip(unittest.TestCase):
    filename = 'lhaplus-zkenc.zip'
    encoding = 'sjis'
    expected = [u'ローマ字テキスト.txt', u'秘密/パスワード.txt']
    password = '全角暗号'

    # ListZip should work without password
    def testListZip(self):
        result = unzipmbcs.listZip(self.filename, self.encoding)
        self.assertEqual(list(map(lambda x: x[0], result)), self.expected)

    def testExtractWithoutPassword(self):
        with self.assertRaises(RuntimeError):
            unzipmbcs.extractZip(self.filename, self.encoding)

    def testExtractWithWrongPassword(self):
        with self.assertRaises(RuntimeError):
            unzipmbcs.extractZip(self.filename, self.encoding, password='wrongpass')

    def testExtractWithPassword(self):
        unzipmbcs.extractZip(self.filename, self.encoding, password=self.password)
        map(lambda x: self.assertTrue(os.path.exists(x), x + ' not exist'),
            self.expected)

        # clean-up
        files = list(self.expected)   # clone the list
        files.reverse()
        for f in files:
            if (os.path.isfile(f)):
                os.remove(f)
            else:
                os.rmdir(f)

if __name__ == '__main__':
    unittest.main()
