# -*- coding: utf-8 -*-

import pkg_resources

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage']

templates_path = ['_templates']

source_suffix = '.rst'

master_doc = 'index'

project = u'mailme'
copyright = u'2014, mailme'

dist = pkg_resources.get_distribution('mailme')
version = release = dist.version

exclude_patterns = []

pygments_style = 'sphinx'

html_theme = 'default'

html_static_path = ['_static']

htmlhelp_basename = 'mailmedoc'

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #'preamble': '',
}

latex_documents = [
    ('index', 'mailme.tex', u'mailme Documentation',
     u'mailme', 'manual'),
]

man_pages = [
    ('index', 'mailme', u'mailme Documentation',
     [u'mailme'], 1)
]

texinfo_documents = [
    ('index', 'mailme', u'mailme Documentation',
     u'mailme', 'mailme', 'One line description of project.',
     'Miscellaneous'),
]

epub_title = u'mailme'
epub_author = u'mailme'
epub_publisher = u'mailme'
epub_copyright = u'2014, mailme'

intersphinx_mapping = {'http://docs.python.org/': None}
