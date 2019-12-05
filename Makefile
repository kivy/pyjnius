all: build_ext

.PHONY: build_ext tests

PYTHON=python
PYTEST=pytest

JAVA_TARGET ?= $(shell $(PYTHON) -c "import re; print('1.6' if int(re.findall(r'\d+', '$(shell javac -version 2>&1)')[0]) < 12 else '1.7')" )
JAVAC_OPTS=-target $(JAVA_TARGET) -source $(JAVA_TARGET)
JAVAC=javac $(JAVAC_OPTS)

ANT=ant -Dant.build.javac.source=$(JAVA_TARGET) -Dant.build.javac.target=$(JAVA_TARGET)

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
