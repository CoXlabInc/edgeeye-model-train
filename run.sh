#!/usr/bin/env bash
while getopts c:f:d:t:a: flag
do
    case ${flag} in
        c) class=${OPTARG};;
        f) confirmed=${OPTARG};;
        d) dataset=${OPTARG};;
        t) token=${OPTARG};;
        a) address=${OPTARG};;
    esac
done
if [ -z $class ] ; then
    echo "Not Class Parameter"
    exit 0
elif [ -z $confirmed ] ; then
    echo "Not confirmed Parameter"
    exit 0
elif [ -z $dataset ] ; then 
    echo "Not dataset Parameter"
    exit 0
elif [ -z $token ] ; then
    echo "Not token Parameter"
    exit 0
elif [ -z $address ] ; then
    echo "Not address Parameter"
    exit 0    
else 
    echo "========================================="
    echo "EdgeEye Model Train Ver 0.1"
    echo "========================================="
    echo "Start Model Download From IoT.own Server..."
fi


model_root_path="./models/train-version-RFB/$class"
log_dir="$model_root_path/logs"
log="$log_dir/log"
mkdir -p "$log_dir"

download_data(){
    python3 download_data_iotown.py -a $address -c $class -t $token -f $confirmed -d $dataset;
}
download_res=$(download_data) 
if [ $download_res != "success" ];then
    echo "Error while downloading data"
    echo "Reason -----------------------------------------------========"
    echo $download_res
    echo "------------------------------------------------------========"
    exit 0
fi
echo "Dataset Download Success"
echo "Training Start!"

python3 -u train.py \
  --datasets \
  ./data/iotown_data_$class\
  --validation_dataset \
  ./data/iotown_data_$class\
  --net \
  RFB \
  --num_epochs \
  200 \
  --milestones \
  "95,150" \
  --lr \
  1e-2 \
  --batch_size \
  24 \
  --input_size \
  320 \
  --checkpoint_folder \
  ${model_root_path} \
  --num_workers \
  0 \
  --log_dir \
  ${log_dir} \
  --cuda_index \
  0 \
  2>&1 | tee "$log"
