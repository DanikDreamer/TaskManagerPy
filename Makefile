test:
	coverage run -m pytest
	coverage xml
	coveralls
