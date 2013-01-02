.PHONY: build_ext tests

build_ext:
	python setup.py build_ext --inplace -f

html:
	$(MAKE) -C docs html

tests: build_ext
	cd tests && javac org/jnius/HelloWorld.java
	cd tests && javac org/jnius/BasicsTest.java
	cd tests && javac org/jnius/MultipleMethods.java
	cd tests && javac org/jnius/SimpleEnum.java
	cd tests && javac org/jnius/InterfaceWithPublicEnum.java
	cd tests && javac org/jnius/ClassArgument.java
	cd tests && env PYTHONPATH=..:$(PYTHONPATH) nosetests-2.7 -v

testimpl: build_ext
	javac jnius/NativeInvocationHandler.java
	python -c 'import jnius.jnius; jnius.jnius.test()'
