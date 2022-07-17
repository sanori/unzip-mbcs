# encoding: utf-8
import os
import os.path
import sys
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import unzipmbcs

def setUpModule():
    if (sys.getfilesystemencoding().lower() != 'utf-8') and (not os.environ.get('PYTHONIOENCODING')):
        raise Exception('non-UTF8 filesystem. set PYTHONIOENCODING as your filesystem encoding!')

def clearFiles(fileList):
    for entry in fileList:
        if (os.path.isfile(entry)):
            os.remove(entry)
        elif (len(os.listdir(entry)) == 0):
            os.rmdir(entry)
        entry = os.path.dirname(entry)
        while entry != '':
            if len(os.listdir(entry)) > 0:
                break;
            os.rmdir(entry)
            entry = os.path.dirname(entry)

class TestFromZip(unittest.TestCase):
    filename = 'win-default.zip'
    encoding = 'cp949'
    expected = [u'똠방각하.txt', u'한글 디렉토리/새 텍스트 문서.txt']

    def testListZip(self):
        result = unzipmbcs.listZip(self.filename, self.encoding)
        self.assertEqual(list(map(lambda x: x[0], result)), self.expected)

    def testExtractZip(self):
        unzipmbcs.extractZip(self.filename, self.encoding)
        map(lambda x: self.assertTrue(os.path.exists(x), x + ' not exist'),
            self.expected)
        clearFiles(self.expected)

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
        clearFiles(self.expected)

if __name__ == '__main__':
    unittest.main()
