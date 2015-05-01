all: build_ext

.PHONY: build_ext tests

ANT=ant

build_ext:
	$(ANT) all
	python setup.py build_ext --inplace -f -g

clean:
	$(ANT) clean
	rm -rf build

html:
	$(MAKE) -C docs html

tests: build_ext
	(cd tests; env CLASSPATH=../build/test-classes:../build/classes PYTHONPATH=..:$(PYTHONPATH) nosetests-2.7 -v)
