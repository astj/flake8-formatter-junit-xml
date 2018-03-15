import unittest
import optparse
import os
import tempfile
from flake8_formatter_junit_xml import JUnitXmlFormatter
from flake8 import style_guide
from junit_xml import TestSuite, TestCase

filename = 'some/filename.py'
error = style_guide.Violation('A000', filename, 2, 1, 'wrong wrong wrong', 'import os')


def create_formatter(**kwargs):
    kwargs.setdefault('output_file', None)
    kwargs.setdefault('tee', False)
    return JUnitXmlFormatter(optparse.Values(kwargs))


class TestJunitXmlFormatter(unittest.TestCase):

    def test_beginning(self):
        f = create_formatter()
        f.beginning(filename)
        self.assertIsInstance(f.test_suites[filename], TestSuite)
        self.assertEqual('flake8.some/filename_py', f.test_suites[filename].name)

    def test_handle(self):
        f = create_formatter()
        f.beginning(filename)
        f.handle(error)
        self.assertIsNotNone(f.test_suites[filename].test_cases)
        self.assertIsInstance(f.test_suites[filename].test_cases[0], TestCase)

    def test_scenario(self):
        (fd, tempfilename) = tempfile.mkstemp()

        # If formatter opens this file with `a`, tests should fail due to pre-written content.
        with os.fdopen(fd, 'w') as f:
            f.write("some pre-existing texts!!\n")

        with open(os.path.dirname(os.path.abspath(__file__)) + '/expected.xml', 'r') as f:
            xml_content = f.read()

        formatter = create_formatter(output_file=tempfilename)
        formatter.start()
        # a file with error
        formatter.beginning(filename)
        formatter.handle(error)
        formatter.finished(filename)
        # another file without error
        formatter.beginning("some/noerror.py")
        formatter.finished("some/noerror.py")
        formatter.stop()

        with open(tempfilename) as f:
            content = f.read()
            # print(content)
            self.assertEqual(xml_content, content)

        os.remove(tempfilename)
