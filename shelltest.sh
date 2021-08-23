#!/bin/bash
get_pythonRES (){
    python3 test.py;
}
ret=$(get_pythonRES)
echo $ret