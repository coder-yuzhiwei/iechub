from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import sys

sys.path.append('../')

import paddle_serving_client.io as serving_io
import os
import time
import six
import logging
import multiprocessing
from io import open
import numpy as np
import json

import paddle
import logging
import paddle.fluid as fluid

# NOTE(paddle-dev): All of these flags should be
# set before `import paddle`. Otherwise, it would
# not take any effect.
os.environ['FLAGS_eager_delete_tensor_gb'] = '0'  # enable gc

import codecs
import paddle.fluid as fluid

import reader.task_reader as task_reader
from model.ernie import ErnieConfig
from model.ernie import ErnieModel
from optimization import optimization
from utils.init import init_pretraining_params, init_checkpoint
from utils.args import print_arguments, check_cuda, prepare_logger
from finetune.relation_extraction_multi_cls import create_model, evaluate, predict, calculate_acc
from finetune_args import parser

args = parser.parse_args()
log = logging.getLogger()

BATCH_SIZE = 32
LR = 2e-5
EPOCH = 600
SAVE_STEPS = 7000
SAVE_PATH = './'
TASK_DATA_PATH = './data/'
MODEL_PATH = '../pretrained_model/'
TRAIN_FILE = 'all_new_data5.json'
DEV_FILE = 'test_data_31.json'
CHECKPOINT = '../checkpoints/step_10201/'
TEST_SAVE = './data/'

FLAGS_sync_nccl_allreduce = 1
# PYTHONPATH=./ernie:${PYTHONPATH:-}

'''
# train
args.use_cuda = False
args.do_train = False
args.do_val = False
args.do_test = True
args.batch_size = BATCH_SIZE
# args.init_checkpoint='./pretrained_model/params'
args.num_labels = 118
args.chunk_scheme = "IOB"
args.label_map_config = '../data/re4.json'
args.spo_label_map_config = '../data/lab4.json'
args.train_set = '../data/all_new_data5.json'
args.dev_set = '../data/dev4.json'
args.vocab_path = '../pretrained_model/vocab.txt'
args.ernie_config_path = '../pretrained_model/ernie_config.json'
args.checkpoints = '../checkpoints'
args.save_steps = SAVE_STEPS
args.validation_steps = SAVE_STEPS
args.weight_decay = 0.01
args.warmup_proportion = 0.0
args.use_fp16 = False
args.epoch = EPOCH
args.max_seq_len = 128
args.learning_rate = LR
args.skip_steps = 10
args.num_iteration_per_drop_scope = 1
args.random_seed = 1
# predict
args.init_checkpoint = '../checkpoints/step_10201/'
args.test_set = '../data/test_data_31.json'
args.test_save = '../data/predev_31.json'
'''

def test():
    ernie_config = ErnieConfig(args.ernie_config_path)
    ernie_config.print_config()

    if args.use_cuda:
        dev_list = fluid.cuda_places()
        place = dev_list[0]
        dev_count = len(dev_list)
    else:
        place = fluid.CPUPlace()
        dev_count = int(os.environ.get('CPU_NUM', multiprocessing.cpu_count()))

    reader = task_reader.RelationExtractionMultiCLSReader(
        vocab_path=args.vocab_path,
        label_map_config=args.label_map_config,
        spo_label_map_config=args.spo_label_map_config,
        max_seq_len=args.max_seq_len,
        do_lower_case=args.do_lower_case,
        in_tokens=args.in_tokens,
        random_seed=args.random_seed,
        task_id=args.task_id,
        num_labels=args.num_labels)

    batch_size = args.batch_size if args.predict_batch_size is None else args.predict_batch_size

    train_pyreader = fluid.layers.py_reader(
        capacity=50,
        shapes=[[-1, args.max_seq_len, 1], [-1, args.max_seq_len, 1],
                [-1, args.max_seq_len, 1], [-1, args.max_seq_len, 1],
                [-1, args.max_seq_len, 1],
                [-1, args.max_seq_len, args.num_labels], [-1, 1], [-1, 1],
                [-1, args.max_seq_len, 1], [-1, args.max_seq_len, 1]],
        dtypes=[
            'int64', 'int64', 'int64', 'int64', 'float32', 'float32', 'int64',
            'int64', 'int64', 'int64'
        ],
        lod_levels=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        name='train_reader',
        use_double_buffer=True)

    train_data_generator = reader.data_generator(
        args.dev_set,
        batch_size=batch_size,
        epoch=1,
        dev_count=1,
        shuffle=False)

    train_pyreader.decorate_tensor_provider(train_data_generator)

    (src_ids, sent_ids, pos_ids, task_ids, input_mask, labels, seq_lens,
     example_index, tok_to_orig_start_index,
     tok_to_orig_end_index) = fluid.layers.read_file(train_pyreader)
    fluid.layers.read_file(train_pyreader)

    print("*****START2*****")
    print(fluid.layers.read_file(train_pyreader)[0])

    for a_batch in reader.data_post_proccess(
            args.dev_set,
            batch_size=batch_size,
            epoch=1,
            dev_count=1,
            shuffle=False):
        yield a_batch

'''
if __name__ == '__main__':
    pass
'''