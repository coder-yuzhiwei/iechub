set -eux

export CPU_NUM=32
# export CUDA_VISIBLE_DEVICES=4,5,6
export TASK_DATA_PATH=./data/
export DEV_FILE=test.csv
export MODEL_PATH=./pretrained_model/
export CHECKPOINT=./checkpoints/step_10201/
export TEST_SAVE=./data/

export FLAGS_sync_nccl_allreduce=1
export PYTHONPATH=./ernie:${PYTHONPATH:-}
python -u ./ernie/run_duie.py \
                   --use_cuda true \
                   --do_train false \
                   --do_val false \
                   --do_test true \
                   --batch_size 8 \
                   --init_checkpoint ${CHECKPOINT} \
                   --num_labels 118 \
                   --label_map_config ${TASK_DATA_PATH}re4.json \
                   --spo_label_map_config ${TASK_DATA_PATH}lab4.json \
                   --test_set ${TASK_DATA_PATH}${DEV_FILE} \
                   --test_save ${TEST_SAVE}predev_31.json \
                   --vocab_path ${MODEL_PATH}vocab.txt \
                   --ernie_config_path ${MODEL_PATH}ernie_config.json \
                   --use_fp16 false \
                   --max_seq_len 256 \
                   --skip_steps 10 \
                   --random_seed 1 
