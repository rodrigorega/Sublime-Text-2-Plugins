import os.path
import re
import subprocess

import sublime
import sublime_plugin


def find_binary(name):
    dirs = ['/usr/local/sbin', '/usr/local/bin', '/usr/sbin',
            '/usr/bin', '/sbin', '/bin']
    for directory in dirs:
        path = os.path.join(directory, name)
        if os.path.exists(path):
            return path

    raise Exception('The binary %s could not be located' % name)


class PythonValidateCommand(sublime_plugin.TextCommand):
    def __init__(self, *args):
        sublime_plugin.TextCommand.__init__(self, *args)
        self.errors = []
        self.index_to_line = {}

    def validate(self):
        """Subclass to add errors."""
        pass

    def validator(self):
        """Subclass to specify validator."""
        pass

    def run(self, edit):
        self.errors = []
        if self.view.file_name().endswith('.py'):
            sublime.status_message("Running %s on %s" % (self.view.file_name(),
                                                         self.validator()))
            self.validate()
            sublime.status_message("%s %s errors " % (len(self.errors),
                                                      self.validator()))
            self.view.window().show_quick_panel(self.errors, self.goto_error)

    def goto_error(self, index):
        # TODO: Highlight line...
        # TODO: Goto column

        if index >= 0:
            line = int(self.index_to_line[index]) - 1

            sublime.status_message("Validation Error: %s" % self.errors[index])

            pt = self.view.text_point(line, 0)

            self.view.sel().clear()
            self.view.sel().add(sublime.Region(pt))

            self.view.show(pt)
        else:
            if len(self.errors) == 0:
                sublime.status_message("No validation errors!")

    def execute(self, args=None):
        if not args:
            args = []
        args.insert(0, self.view.file_name())
        args.insert(0, find_binary(self.validator()))
        proc = subprocess.Popen(args, stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        output = proc.stdout.read()
        return output

    def add_error(self, row, msg, err):
        """Adds a validation error"""
        ignored_ids_key = '%s_ignored_ids' % self.validator()
        ignored_ids = []  # self.view.settings().get(ignored_ids_key, [])
        if err not in ignored_ids:
            self.index_to_line[len(self.errors)] = row
            self.errors.append('Line %s: %s' % (row, msg))

    def is_enabled(self):
        """Enable for Python files."""
        return self.view.file_name() and self.view.file_name().endswith('.py')


class Pep8ValidateCommand(PythonValidateCommand):
    """ This will invoke PEP8 checking on the given file and
    provide a pop-up with validation errors that will jump to
    the line-in-question.

    The pep8 executable must be in your system's path for this to work.
    """
    def validator(self):
        return "pep8"

    def validate(self):
        output = self.execute(['--repeat'])
        pep8_regex = re.compile('(.*):(.*):(.*): (....) (.*)')
        for line in output.split('\n'):
            re_result = re.match(pep8_regex, line)
            if re_result:
                _, row, col, err_id, msg = re_result.groups()
                self.add_error(row, "%s %s" % (err_id, msg), err_id)


class PylintValidateCommand(PythonValidateCommand):
    """ This will invoke pylint validation on the given file and provide
    a pop-up with validation errors that will jump to the line-in-question.

    The pylint executable must be in your system's path fro this to work.
    """
    def validator(self):
        return "pylint"

    def validate(self):
        output = self.execute(['--reports=no', '--include-ids=yes'])
        pylint_regex = re.compile('^(.*): (\d+),(\d+):(.+):\s+(.+)')
        for line in output.split('\n'):
            re_result = re.match(pylint_regex, line)
            if re_result:
                err_id, row, col, __, msg = re_result.groups()
                self.add_error(row, '(%s) %s' % (err_id, msg), err_id)
