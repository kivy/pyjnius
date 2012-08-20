.PHONY: build_ext tests

build_ext:
	python setup.py build_ext --inplace -f

html:
	$(MAKE) -C docs html

tests: build_ext
	cd tests && javac org/jnius/HelloWorld.java
	cd tests && javac org/jnius/BasicsTest.java
	cd tests && env PYTHONPATH=..:$(PYTHONPATH) nosetests -v
