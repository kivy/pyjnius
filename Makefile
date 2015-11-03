all: build_ext

.PHONY: build_ext tests

ifdef PYTHON3
PYTHON=python3
NOSETESTS=nosetests-3.4
else
PYTHON=python
NOSETESTS=nosetests-2.7
endif

JAVAC_OPTS=-target 1.6 -source 1.6
JAVAC=javac $(JAVAC_OPTS)

ANT=ant

build_ext:
	$(ANT) all
	$(PYTHON) setup.py build_ext --inplace -f -g

clean:
	$(ANT) clean
	rm -rf build jnius/config.pxi

html:
	$(MAKE) -C docs html

tests: test2 test3

tests2: 
	(cd tests; env CLASSPATH=../build/test-classes:../build/classes PYTHONPATH=..:$(PYTHONPATH) $(NOSETESTS) -v)
tests3: 
	make tests2 PYTHON3=1
