all: build_ext

.PHONY: build_ext tests tests3

ifdef PYTHON3
PYTHON=python3
NOSETESTS=nosetests-3
else
PYTHON=python
NOSETESTS=nosetests-2.7
endif

ANT=ant

build_ext:
	$(ANT) all
	$(PYTHON) setup.py build_ext --inplace -f -g

clean:
	$(ANT) clean
	rm -rf build jnius/config.pxi

html:
	$(MAKE) -C docs html

tests: 
	(cd tests; env CLASSPATH=../build/test-classes:../build/classes PYTHONPATH=..:$(PYTHONPATH) $(NOSETESTS) -v)
