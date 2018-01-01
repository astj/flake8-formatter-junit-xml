# make tasks for ME to upload releases :-)

all: clean deps build upload

clean:
	rm -rf dist/

deps:
	pip install wheel twine

build:
	python setup.py sdist
	python setup.py bdist_wheel

upload:
	ls -l dist/
	echo "\nEnsure version is correct and proper distributions are built.\nHit a return to release. C-c to abort:"
	read answer
	twine upload dist/*

.PHONY: all clean deps build upload
