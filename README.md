Recursively steps through a folder of code and converts the files to
syntax-highlighted HTML for easy viewing.

Requires that Python 3 be installed as well as [Jinja2](http://jinja.pocoo.org)
(for template rendering) and [Pygments](http://pygments.org) (for syntax
highlighting).

    pip3 install -r requirements.txt
    python3 code2html.py

The directory of files to convert should be named `in`. The output is written
to a directory named `out`. Before running this script, customize
`template.html` as desired.
