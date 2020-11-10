all: install

.PHONY: install dist upload clean

install:
	python3 setup.py install

dist:
	python3 setup.py sdist bdist_wheel

upload:
	python3 -m twine upload dist/*

test-upload:
	python3 -m twine upload --repository testpypi dist/*

clean:
	rm -rf dist/ build/ *.egg-info/
