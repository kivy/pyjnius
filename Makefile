.PHONY: build_ext tests

JAVAC_OPTS=-target 1.6 -source 1.6
JAVAC=javac $(JAVAC_OPTS)

build_ext:
	$(JAVAC) jnius/src/org/jnius/NativeInvocationHandler.java
	python setup.py build_ext --inplace -f -g

clean:
	find . -name "*.class" -exec rm {} \;
	rm -rf build

html:
	$(MAKE) -C docs html

tests: build_ext
	cd tests && $(JAVAC) org/jnius/HelloWorld.java
	cd tests && $(JAVAC) org/jnius/BasicsTest.java
	cd tests && $(JAVAC) org/jnius/MultipleMethods.java
	cd tests && $(JAVAC) org/jnius/SimpleEnum.java
	cd tests && $(JAVAC) org/jnius/InterfaceWithPublicEnum.java
	cd tests && $(JAVAC) org/jnius/ClassArgument.java
	cd tests && $(JAVAC) org/jnius/MultipleDimensions.java
	cp jnius/src/org/jnius/NativeInvocationHandler.class tests/org/jnius
	cd tests && env PYTHONPATH=..:$(PYTHONPATH) nosetests-2.7 -v
