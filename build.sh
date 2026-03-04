#!/bin/bash

if [ ! -d .venv ];then
    which python3
    if [ $? -eq 0 ];then
        mod_python=$(module avail python 2>&1 | grep -Pm 1 "python/(?:3\.[19]\d*\.\d|latest)")
        if [ ! $? -eq 0 ];then
            echo "Could not find python. Aborting."
            exit 10
        fi
        module load $mod_python
    fi
    py_ver=$(pyhton --version | grep -Pm "3\.[19]\d*\.\d")
    if [ ! $? -eq 0 ];then
        echo "Python version seems to be out of date. Aborting."
        exit 11
    fi
    python -m venv .venv
fi

. .venv/bin/activate
pip show uv
if [ ! $? -eq 0 ];then
    pip isntall uv
    if [ ! $? -eq 0 ];then
        echo "uv failed to install. Aborting."
        exit 12
    fi
fi

uv build
ls dist/asgs_gui*.whl
if [ ! $? -eq 0 ];then 
    echo "uv failed to build whl file. Aborting."
    exit 13
fi