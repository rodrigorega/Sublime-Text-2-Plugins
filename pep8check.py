import os
import re
from subprocess import Popen
from subprocess import PIPE

import sublime
import sublime_plugin


class Pep8CheckCommand(sublime_plugin.TextCommand):

    """ This will invoke PEP8 checking on the given file and
    provide a pop-up with validation errors that will jump to
    the line-in-question.

    The pep8 executable must be in your system's path for this to work.
    """

    def goto_error(self, index):
        # TODO: Highlight line...
        # TODO: Goto column

        if index >= 0:
            line = int(self.index_to_line[index]) - 1

            sublime.status_message("PEP8: %s" % self.errors[index])

            pt = self.view.text_point(line, 0)

            self.view.sel().clear()
            self.view.sel().add(sublime.Region(pt))

            self.view.show(pt)
        else:
            if len(self.errors) == 0:
                sublime.status_message("PEP8 Valid!")

    def run(self, edit):
        if self.view.file_name().endswith('.py'):
            sublime.status_message("Running PEP8 " + self.view.file_name())
            output = Popen(["/usr/local/bin/pep8",
                            self.view.file_name(),
                            "--repeat"], stdout=PIPE).communicate()[0]
            self.errors = []
            self.index_to_line = {}
            pep8_regex = re.compile('(.*):(.*):(.*): (....) (.*)')
            for line in output.split('\n'):
                print line
                if len(line) > 0:
                    _, row, col, err, msg = re.match(pep8_regex, line).groups()
                    self.index_to_line[len(self.errors)] = row
                    self.errors.append("Line %s: %s %s" % (row, err, msg))

            self.view.window().show_quick_panel(self.errors, self.goto_error)
            sublime.status_message("%s PEP8 errors " % len(self.errors))

    def is_enabled(self):
        return self.view.file_name() and self.view.file_name().endswith('.py')
