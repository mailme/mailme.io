#
# MailMe Makefile
# ~~~~~~~~~~~~~~~
#
# Shortcuts for various tasks.
#

documentation:
	@(cd docs; make html)


test:
	tox

doctest:
	@(cd docs; sphinx-build -b doctest . _build/doctest)

clean:
	rm -rf docs/_build/*
