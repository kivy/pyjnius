.PHONY: build_ext tests

build_ext:
	javac jnius/src/org/jnius/NativeInvocationHandler.java
	python setup.py build_ext --inplace -f -g

html:
	$(MAKE) -C docs html

compile-tests: build_ext
	cd tests && javac org/jnius/HelloWorld.java
	cd tests && javac org/jnius/BasicsTest.java
	cd tests && javac org/jnius/MultipleMethods.java
	cd tests && javac org/jnius/SimpleEnum.java
	cd tests && javac org/jnius/InterfaceWithPublicEnum.java
	cd tests && javac org/jnius/ClassArgument.java

tests: compile-tests
	cd tests && env PYTHONPATH=..:$(PYTHONPATH) nosetests-2.7 -v
