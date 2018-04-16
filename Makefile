.PHONY: tests coverage

tests:
	nosetests tests

coverage:
	nosetests --with-coverage --cover-package=zaif tests
	coverage html --include='zaif*'
