import sys
import os

sys.path.append('../')
# os.chdir('')
# 是否设置不显示输出
test_save = ''
os.system(r'python -u ./ernie/run_predict.py --test_save {}'.format(test_save))

