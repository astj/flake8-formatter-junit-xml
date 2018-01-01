from flake8.formatting import base
from junit_xml import TestSuite, TestCase


class JUnitXmlFormatter(base.BaseFormatter):
    """JUnit XML formatter for Flake8."""

    def after_init(self):
        self.test_suites = {}

    def beginning(self, filename):
        name = '{0}.{1}'.format("flake8", filename.replace('.', '_'))
        self.test_suites[filename] = TestSuite(name, file=filename)

    # Do not write each error
    def handle(self, error):
        name = '{0}, {1}'.format(error.code, error.text)
        test_case = TestCase(name, file=error.filename, line=error.line_number)
        message = '%(path)s:%(row)d:%(col)d: %(code)s %(text)s' % {
            "code": error.code,
            "text": error.text,
            "path": error.filename,
            "row": error.line_number,
            "col": error.column_number,
        }
        test_case.add_failure_info(message)
        self.test_suites[error.filename].test_cases.append(test_case)

    # Add a dummy test if no error found
    def finished(self, filename):
        if len(self.test_suites[filename].test_cases) == 0:
            dummy_case = TestCase("Check passed", file=filename)
            self.test_suites[filename].test_cases.append(dummy_case)

    # writes results to file after all files are processed
    def stop(self):
        self._write(TestSuite.to_xml_string(iter(self.test_suites.values())))
        super(JUnitXmlFormatter, self).stop()
