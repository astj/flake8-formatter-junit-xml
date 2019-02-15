from flake8.formatting import base, default
import optparse
from junit_xml import TestSuite, TestCase


class JUnitXmlFormatter(base.BaseFormatter):
    """JUnit XML formatter for Flake8."""

    def after_init(self):
        self.test_suites = {}
        display_formatter_opts = {
            'output_file': None,
            'tee': False,
            'show_source': self.options.show_source,
            'format': 'default',
        }
        self.display_formatter = default.Default(optparse.Values(display_formatter_opts))

    def beginning(self, filename):
        name = '{0}.{1}'.format("flake8", filename.replace('.', '_'))
        self.test_suites[filename] = TestSuite(name, file=filename)

    # This formatter overwrites the target file, in contrast to flake8 base formatter which appends to the file.
    def start(self):
        if self.filename:
            self.output_fd = open(self.filename, 'w')
        # I know this does nothing because display_formatter.output_fd is None, but for safe
        self.display_formatter.start()

    def should_print_screen(self):
        return self.options.tee or self.output_fd is None

    # Store each error as a TestCase
    def handle(self, error):
        name = '{0}, {1}'.format(error.code, error.text)
        test_case = TestCase(name, file=error.filename, line=error.line_number)
        test_case.add_failure_info(message=self.format(error), output=self.show_source(error))
        self.test_suites[error.filename].test_cases.append(test_case)
        if self.should_print_screen():
            self.display_formatter.handle(error)

    def format(self, error):
        return '%(path)s:%(row)d:%(col)d: %(code)s %(text)s' % {
            "code": error.code,
            "text": error.text,
            "path": error.filename,
            "row": error.line_number,
            "col": error.column_number,
        }

    # Add a dummy test if no error found
    def finished(self, filename):
        if len(self.test_suites[filename].test_cases) == 0:
            dummy_case = TestCase("Check passed", file=filename)
            self.test_suites[filename].test_cases.append(dummy_case)

    # sort to generate a stable output
    def sorted_suites(self):
        return map(lambda x: x[1], sorted(self.test_suites.items()))

    # junit-formatter itself does not print output to screen (display_formatter will do)
    def write_xml(self, output):
        if self.output_fd is not None:
            self.output_fd.write(output + self.newline)

    # writes results to file after all files are processed
    def stop(self):
        self.write_xml(TestSuite.to_xml_string(iter(self.sorted_suites())))
        super(JUnitXmlFormatter, self).stop()
        # I know this does nothing because display_formatter.output_fd is None, but for safe
        self.display_formatter.stop()
