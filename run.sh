#!/usr/bin/env bash
while getopts c:f:d:t: flag
do
    case ${flag} in
        c) class=${OPTARG};;
        f) confirmed=${OPTARG};;
        d) dataset=${OPTARG};;
        t) token=${OPTARG};;
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
else 
    echo "PASS"
fi


model_root_path="./models/train-version-RFB"
log_dir="$model_root_path/logs"
log="$log_dir/log"
mkdir -p "$log_dir"

echo "Dataset";
python3 test.py;
python3 test2.py;
# python3 -u train.py \
#   --datasets \
#   ./data/wider_face_add_lm_10_10 \
#   --validation_dataset \
#   ./data/wider_face_add_lm_10_10 \
#   --net \
#   RFB \
#   --num_epochs \
#   200 \
#   --milestones \
#   "95,150" \
#   --lr \
#   1e-2 \
#   --batch_size \
#   24 \
#   --input_size \
#   320 \
#   --checkpoint_folder \
#   ${model_root_path} \
#   --num_workers \
#   0 \
#   --log_dir \
#   ${log_dir} \
#   --cuda_index \
#   0 \
#   2>&1 | tee "$log"
