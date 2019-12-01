#!/usr/bin/env bash

yum install -y java-1.7.0-openjdk-devel

for target in $(ls /opt/python/); do
    python=/opt/python/$target/bin/python
    $python -m pip install -U setuptools cython
    $python setup.py bdist_wheel
done

for whl in dist/*.whl; do
    auditwheel repair $whl
done

rm dist/*-linux_*.whl
mv wheelhouse/*.whl dist/
