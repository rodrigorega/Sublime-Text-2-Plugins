import os
import sublime
import sublime_plugin


class WhitespaceListener(sublime_plugin.EventListener):
    def on_pre_save(self, view):
        if view.settings().get('expand_tabs_on_save') == True:
            view.run_command('expand_tabs')
        if view.settings().get('trim_trailing_whitespace_on_save') == True:
            view.run_command('trim_trailing_whitespace')
        if view.settings().get('ensure_newline_at_eof_on_save') == True:
            view.run_command('ensure_newline_at_eof')
        # view.run_command('pep8_check')


class TrimTrailingWhitespace(sublime_plugin.TextCommand):
    def run(self, edit):
        trailing_white_space = self.view.find_all("[\t ]+$").reverse()
        for match in trailing_white_space:
            self.view.erase(edit, match)
        self.view.end_edit(edit)


class EnsureNewlineAtEof(sublime_plugin.TextCommand):
    def run(self, edit):
        max_removals = self.view.settings().get('max_newline_removals', 20)
        for i in range(max_removals):
            size = self.view.size()
            last_line = self.view.full_line(size - 1)
            if size > 0 and self.view.substr(last_line) == '\n':
                self.view.erase(edit, last_line)

        if not self.view.substr(last_line).endswith('\n'):
            self.view.insert(edit, self.view.size(), '\n')

        self.view.end_edit(edit)
