#!/usr/bin/env python3

"""Converts files in a directory to syntax-highlighted HTML files."""

import os
from fnmatch import fnmatch
from jinja2 import Template
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import guess_lexer_for_filename, TextLexer
from pygments.util import ClassNotFound


IGNORED_DIRECTORIES = ['.git', '.vagrant']
IGNORED_FILENAMES = ['.DS_Store', '*.pyc']


def main():
    formatter = HtmlFormatter(linenos=True)

    with open('template.html') as f:
        template = Template(f.read())

    for root, directories, filenames in os.walk('in'):
        # Skip walking down excluded directories.
        # We modify the original list because this is how os.walk is designed.
        directories[:] = filter(include_directory, directories)

        # Skip excluded files.
        filenames = filter(include_filename, filenames)

        for filename in filenames:
            path = os.path.join(root, filename)

            try:
                highlighted = highlight_file(path, formatter)
            except UnicodeDecodeError:
                # Skip files which can't be decoded (e.g. binary files).
                pass
            else:
                save_highlighted(path, template, highlighted)


def include_directory(directory):
    """Returns true if the given directory is not on the ignore list."""
    return directory not in IGNORED_DIRECTORIES


def include_filename(filename):
    """Returns true if the given file is not on the ignore list."""
    return not any(fnmatch(filename, pattern) for pattern in IGNORED_FILENAMES)


def highlight_file(path, formatter):
    """Converts the contents of a file to a syntax-highlighted HTML snippet."""
    with open(path) as f:
        text = f.read()

    try:
        lexer = guess_lexer_for_filename(path, text)
    except ClassNotFound:
        lexer = TextLexer()

    highlighted = highlight(text, lexer, formatter)
    return highlighted


def save_highlighted(path, template, highlighted):
    """Writes a highlighted code snippet to an HTML file."""
    new_path = os.path.join('out', path)

    # Ensure the directory tree exists for the output file.
    new_root = os.path.dirname(new_path)
    os.makedirs(new_root, exist_ok=True)

    with open(new_path, 'w') as f:
        rendered = template.render(title=path, content=highlighted)
        f.write(rendered)


if __name__ == '__main__':
    main()
