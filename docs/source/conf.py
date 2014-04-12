# -*- coding: utf-8 -*-
import os
import pkg_resources

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mailme.settings.development")


try:
    import sphinx_rtd_theme
except ImportError:
    sphinx_rtd_theme = None


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

if sphinx_rtd_theme:
    html_theme = "sphinx_rtd_theme"
    html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
else:
    html_theme = "default"

html_static_path = ['_static']

htmlhelp_basename = 'mailmedoc'

latex_elements = {}

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
