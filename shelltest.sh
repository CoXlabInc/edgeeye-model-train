#!/bin/bash
get_pythonRES (){
    python3 test.py;
}
ret=$(get_pythonRES)
echo $ret


download_data(){
    python3 download_data_iotown.py -a $address -c $class -t $token -f $confirmed -d $dataset -i $modelid;
}
download_res=$(download_data) 