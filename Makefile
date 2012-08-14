.PHONY: build_ext tests

build_ext:
	python setup.py build_ext --inplace -f

tests: build_ext
	cd tests && javac org/jnius/HelloWorld.java
	cd tests && env PYTHONPATH=..:$(PYTHONPATH) python test_simple.py
	cd tests && env PYTHONPATH=..:$(PYTHONPATH) python test_reflect.py
