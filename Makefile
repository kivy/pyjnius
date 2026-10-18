all: build_ext

.PHONY: build_ext tests

PYTHON=python
PYTEST=pytest

JAVA_TARGET ?= 8

ANT=ant -Dant.build.javac.source=$(JAVA_TARGET) -Dant.build.javac.target=$(JAVA_TARGET) -Dant.build.javac.release=$(JAVA_TARGET)

build_ext:
	$(ANT) all
	$(PYTHON) setup.py build_ext --inplace -g

clean:
	$(ANT) clean
	rm -rf build jnius/config.pxi

html:
	$(MAKE) -C docs html

# for use in travis; tests whatever you got.
# use PYTHON3=1 to force python3 in other environments.
tests:
	(cd tests; env CLASSPATH=../build/test-classes:../build/classes PYTHONPATH=..:$(PYTHONPATH) $(PYTEST) -v)
