import sublime, sublime_plugin

class ExpandTabs(sublime_plugin.EventListener):
    def on_pre_save(self, view):
        if view.settings().get("expand_tabs_on_save") == True:
            view.run_command('expand_tabs')

class TrimTrailingWhiteSpace(sublime_plugin.EventListener):
    def on_pre_save(self, view):
        if view.settings().get("trim_trailing_white_space_on_save") == True:
            trailing_white_space = view.find_all("[\t ]+$")
            trailing_white_space.reverse()
            edit = view.begin_edit()
            for r in trailing_white_space:
                view.erase(edit, r)
            view.end_edit(edit)

class EnsureNewlineAtEof(sublime_plugin.EventListener):
    def on_pre_save(self, view):
        if view.settings().get("ensure_newline_at_eof_on_save") == True:
            # Remove up to 'max_lines' empty lines on save
            max_lines = 20
            i = 0
            edit = view.begin_edit()
            while i <= max_lines and view.size() > 0 and view.substr(view.full_line(view.size() - 1)) == '\n':
                i = i + 1
                # print "%d: Last line is a newline, removing" % i
                view.erase(edit, view.full_line(int(view.size() - 1)))

            # Only apply last 'max_lines' edits
            if i < max_lines:
                view.end_edit(edit)
            # Add a newline if necesary
            if view.size() > 0 and view.substr(view.size() - 1) != '\n':
                # print "Last line is NOT a newline, adding..."
                edit = view.begin_edit()
                view.insert(edit, view.size(), "\n")
                view.end_edit(edit)
