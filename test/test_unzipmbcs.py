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
        if (sys.getfilesystemencoding() != 'UTF-8') and (not os.environ.get('PYTHONIOENCODING')):
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

if __name__ == '__main__':
    unittest.main()
