import os
from yacs.config import CfgNode as CN

# ----------------------------------------------------------------------------------- #
# Config definition
# ----------------------------------------------------------------------------------- #
"""
config system:
This file specifies default config options. You should not change values in this file. 
Instead, you should write a config file (in yaml) and use merge_cfg_from_file(yaml_file) 
to load it and override the default options.
"""

_C = CN()
cfg = _C
# ---------------------------------------------------------------------------- #
# DATA options
# ---------------------------------------------------------------------------- #
_C.DATA = CN()
_C.DATA.DATASET = 'ade20k'
_C.DATA.TRAIN_JSON = ""
_C.DATA.VAL_JSON = ""
_C.DATA.TEST_JSON = ""
_C.DATA.CLASSES = 150
_C.DATA.MEAN = [0.485, 0.456, 0.406]
_C.DATA.STD = [0.229, 0.224, 0.225]

# ---------------------------------------------------------------------------- #
# TRAIN options
# ---------------------------------------------------------------------------- #
_C.TRAIN = CN()
_C.TRAIN.AUGMENTATIONS = ['RandomFlip', 'RandomResize', 'RandomCrop', 'RandomRotate']
_C.TRAIN.BATCH_SIZE = 8
# Probability of using RandomFlip
_C.TRAIN.PROB = 0.5
# Ratio of using RandomResize
_C.TRAIN.RATIO = (0.5, 2)
# crop_size of using RandomCrop
# int: a square crop (crop_size, crop_size) is made
# list: [640, 512]
_C.TRAIN.CROP_SIZE = 512
# prams of using RandomRotate: PADDING for img, IGNORE_LABEL for mask
_C.TRAIN.ROTATE = (-10, 10)
_C.TRAIN.PADDING = (0, 0, 0)
_C.TRAIN.IGNORE_LABEL = 255
_C.TRAIN.START_EPOCH = 1
_C.TRAIN.MAX_EPOCH = 100

# ---------------------------------------------------------------------------- #
# Model options
# ---------------------------------------------------------------------------- #
_C.MODEL = CN()
_C.MODEL.BACKBONE_NAME = 'resnet18'
_C.MODEL.BACKBONE_PRETRAINED = True
_C.MODEL.BACKBONE_WEIGHT = "pretrained/"
_C.MODEL.NORM_LAYER = 'bn'  # bn or syncbn
_C.MODEL.OUTPUT_STRIDE = 8  # 8, 16, 32
_C.MODEL.HEAD7X7 = False  # only for resnet backbone
_C.MODEL.PHASE = 'train'  # if test mode, RESUME and FINETUNE must be False
_C.MODEL.RESUME = False
_C.MODEL.FINETUNE = False
_C.MODEL.NAME = 'psp'
_C.MODEL.PRETRAINED = True
_C.MODEL.MODEL_WEIGHT = "ckpts/ade20k/model.pth"
_C.MODEL.STATE_WEIGHT = "ckpts/ade20k/state.pth"
# output.size * room_factor
_C.MODEL.ZOOM_FACTOR = 8
_C.MODEL.MULTIPLIER = 1.0  # for mobilenetv1-v2 shufflenetv1-v2 backbone
_C.MODEL.DROP_RATE = 0.1  # for densenet

# ---------------------------------------------------------------------------- #
# PSP(PPM) options
# ---------------------------------------------------------------------------- #
# supported backbone: resnet mobilenetv1 mobilenetv2 shufflenetv2
_C.PPM = CN()
_C.PPM.POOL_SCALES = (1, 2, 3, 6)
_C.PPM.PPM_HIDDEN_DIM = 512
_C.PPM.PPM_OUT_DIM = 512
_C.PPM.DROP_OUT = 0.1
_C.PPM.USE_AUX = True  # c3 must be not None if USE_AUX is True
_C.PPM.AUX_LOSS_WEIGHT = 0.4

# ---------------------------------------------------------------------------- #
# FCN options
# ---------------------------------------------------------------------------- #
# supported backbone: only vgg
_C.FCN = CN()
_C.FCN.DROP_OUT = 0.1

# ---------------------------------------------------------------------------- #
# deeplabv3(ASPP) options
# ---------------------------------------------------------------------------- #
# supported backbone: resnet mobilenetv1 mobilenetv2 shufflenetv2
_C.ASPP = CN()
_C.ASPP.OUTPUT_STRIDE = 8  # 8 or 16
_C.ASPP.OUT_CHANNELS = 512
_C.ASPP.DROPOUT = 0.5
_C.ASPP.USE_AUX = True  # c3 must be not None if USE_AUX is True

# ---------------------------------------------------------------------------- #
# deeplabv3plus options
# ---------------------------------------------------------------------------- #
_C.DEEPLABV3PLUS = CN()
_C.DEEPLABV3PLUS.LOW_LEVEL_FEATURE_CHANNELS = 48  # 48 or 32
_C.DEEPLABV3PLUS.OUTPUT_STRIDE = 16  # only 16 for deeplabv3plus
_C.DEEPLABV3PLUS.USE_AUX = True
_C.DEEPLABV3PLUS.DROPOUT = 0.1

# ---------------------------------------------------------------------------- #
# lraspp options
# ---------------------------------------------------------------------------- #
_C.LRASPP = CN()
_C.LRASPP.OUTPUT_STRIDE = 8
_C.LRASPP.INTER_CHANNELS = 128  # default

# ---------------------------------------------------------------------------- #
# denseaspp options
# ---------------------------------------------------------------------------- #
_C.DENSEASPP = CN()
_C.DENSEASPP.OUTPUT_STRIDE = 8
_C.DENSEASPP.INTER_CHANNELS = 256  # default
_C.DENSEASPP.OUT_CHANNELS = 64  # default
_C.DENSEASPP.ATROUS_RATE = [3, 6, 12, 18, 24]  # default
_C.DENSEASPP.DROP_RATE = 0.1
_C.DENSEASPP.USE_AUX = True

# ---------------------------------------------------------------------------- #
# bisenet options
# ---------------------------------------------------------------------------- #
_C.BISENET = CN()
_C.BISENET.IN_CHANNELS = 3
_C.BISENET.SPATIAL_PATH_OUT_CHANNELS = 128
_C.BISENET.CONTEXT_PATH_OUT_CHANNELS = 128
_C.BISENET.DROP_RATE = 0.1
_C.BISENET.USE_AUX = True

# ---------------------------------------------------------------------------- #
# contextnet options
# ---------------------------------------------------------------------------- #
_C.ContextNet = CN()
_C.ContextNet.IN_CHANNELS = 3
_C.ContextNet.CHANNELS = [32, 32, 48, 64, 96, 128]
_C.ContextNet.EXPANSION_FACTOR = [1, 6, 6, 6, 6, 6]
_C.ContextNet.LAYERS = [1, 1, 3, 3, 2, 2]
_C.ContextNet.HIDDEN_CHANNELS1 = 32
_C.ContextNet.HIDDEN_CHANNELS2 = 64
_C.ContextNet.OUT_CHANNELS = 128
_C.ContextNet.USE_AUX = False

# ---------------------------------------------------------------------------- #
# SOLVER options
# ---------------------------------------------------------------------------- #
_C.SOLVER = CN()
_C.SOLVER.LOSS_NAME = ''
_C.SOLVER.LOSS_WEIGHT = []
_C.SOLVER.IGNORE_LABEL = 255
_C.SOLVER.OPTIMIZER_NAME = 'sgd'
_C.SOLVER.LR = 0.02
_C.SOLVER.MOMENTUM = 0.99
_C.SOLVER.WEIGHT_DECAY = 4e-5
_C.SOLVER.EPS = 1e-8  # Adadelta: 1e-6; Adam,Adamax,RMSprop: 1e-8; Adagrad: 1e-10
_C.SOLVER.BETAS = (0.9, 0.999)  # for Adam, Adamax
_C.SOLVER.AMSGRAD = False  # for Adam
_C.SOLVER.LAMBD = 1e-4  # for ASGD
_C.SOLVER.ALPHA = 0.75  # for ASGD:0.75; RMSprop:0.99
_C.SOLVER.T0 = 1e6  # for ASGD
_C.SOLVER.RTO = 0.9  # for Adadelta
_C.SOLVER.LR_DECAY = 0  # for Adagrad

# 'step', 'multistep', 'exponential', 'CosineAnnealing'
# (lr update by epoch method)
_C.SOLVER.SCHEDULER_NAME = 'step'
_C.SOLVER.GAMMA = 0.1
_C.SOLVER.STEP_SIZE = 10  # for 'step'
_C.SOLVER.MILESTONES = [30, 60, 90]  # for 'multistep'
_C.SOLVER.T_MAX = 100  # for 'CosineAnnealing'

# another method: 'poly', 'step', 'cosine'
# (lr update by batch size method)
_C.SOLVER.LR_POLICY = 'poly'
# Warm up to SOLVER.LR over this number of sgd epochs
_C.SOLVER.WARM_UP_EPOCH = 0
# LR of warm up beginning
_C.SOLVER.WARM_UP_LR = 0.002
# For 'ploy', the power in poly to drop LR
_C.SOLVER.LR_POW = 0.9
# For 'STEP', Non-uniform step iterations
_C.SOLVER.STEPS = [30, 60, 90]

# ---------------------------------------------------------------------------- #
# Misc options
# ---------------------------------------------------------------------------- #

_C.ROOT = "../data/"

# Use GPU for training or testing if True
_C.GPU_USE = True

# Specify using GPU ids
_C.GPU_IDS = u'0,1,2,3,4,5,6,7'

# random seed
_C.SEED = 1024

# Directory for saving checkpoints and loggers
_C.CKPT = '../ckpts/ade20k/ade20k_contextnet'


def merge_cfg_from_file(file):
    if os.path.isfile(file) and file.endswith('.yaml'):
        cfg.merge_from_file(file)
    else:
        raise Exception('{} is not a yaml file'.format(file))


def merge_cfg_from_list(cfg_list):
    cfg.merge_from_list(cfg_list)


# for shown
def logger_cfg_from_file(file):
    return cfg.load_cfg(open(file))

