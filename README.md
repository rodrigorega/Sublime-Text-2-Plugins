# Sublime Text 2 Plugins

This is just a handy place to store some plugins I wrote for ST2.

## whitespace.py

This plugin handles some common whitespace-related issues, including trimming
whitespace from line endings, ensuring a specific number of newlines at the
end of a file, and expanding tabs into spaces.

There are specific commands to achieve each of these, as well as an
EventListener with settings to run these commands automatically on-save.

```
{
    'expand_tabs_on_save': true,
    'trim_trailing_whitespace_on_save': true,
    'ensure_newline_at_eof_on_save': true
}
```

## python_validation.py

This plugin provides a GUI facility for running common python validation
programs, including pylint and pep8.  Extending ehamiter's code, this plugin
pop-ups a list of validation errors, and allows the user to jump to the
offending line.

You can ignore specific pylint and pep8 errors by specifying an array of ignored
error codes in 'pylint_ignored_ids' or 'pep8_ignored_ids':

```
{
    'pep8_ignored_ids': ['E501'], // Ignore long line errors
    'pylint_ignored_ids': ['C0111'] // Ignore docstring errors
}
```

###Installation
Copy **Main.sublime-menu**, **Context.sublime-menu** and **python_validation.py** into your Sublime Text 2 User packages folder *(Sublime Text 2 > Preferences > Browse Packages... > User)*

**This plugin is dependent on pep8 and pylint, which you must install yourself.** You can install, upgrade, uninstall pep8.py with these commands:


    $ sudo pip install pep8
    $ sudo pip install --upgrade pep8
    $ sudo pip uninstall pep8
 

    $ sudo pip install pylint
    $ sudo pip install --upgrade pylint
    $ sudo pip uninstall pylint
