#!/usr/bin/env bash

target=$1

# yum install -y java-1.7.0-openjdk-devel
ls /opt/python/
python=/opt/python/$target/python
$python -m pip install -U setuptools wheel cython
$python setup.py bdist_wheel
