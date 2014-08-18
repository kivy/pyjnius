.PHONY: build_ext tests

build_ext:
	javac jnius/src/org/jnius/NativeInvocationHandler.java
	python setup.py build_ext --inplace -f -g
	#python setup.py build_ext --inplace -f

html:
	$(MAKE) -C docs html

tests: build_ext
	cd tests && javac org/jnius/HelloWorld.java
	cd tests && javac org/jnius/BasicsTest.java
	cd tests && javac org/jnius/MultipleMethods.java
	cd tests && javac org/jnius/SimpleEnum.java
	cd tests && javac org/jnius/InterfaceWithPublicEnum.java
	cd tests && javac org/jnius/ClassArgument.java
	cd tests && env PYTHONPATH=..:$(PYTHONPATH) nosetests -v

clean:
	rm -rf build/
	rm -f jnius/config.pxi
	rm -f jnius/jnius.c
	rm -f jnius/*.so
	find . -iname '*.pyc' -delete
	find . -iname '*.class' -delete
