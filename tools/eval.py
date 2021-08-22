import os
import time
import torch
import shutil
import random
import argparse

from tqdm import tqdm
from torchvision import transforms

import _init_path
from config.config import cfg, merge_cfg_from_file, merge_cfg_from_list, logger_cfg_from_file
from dataset import dataset, set_augmentations
from models.backbone.build import load_trained_model
from models.model_zone import generate_model
from utils.utils import setup_logger, AverageMeter
from utils.metrics import accuracy, intersectionAndUnion


def main():
    # Setup Config
    parser = argparse.ArgumentParser(description='Semantic Segmentation Model Evaluating')
    parser.add_argument('--cfg', dest='cfg_file', default='../config/ade20k/ade20k_psp.yaml',
                        type=str, help='config file')
    parser.add_argument('opts', help='see ../config/config.py for all options', default=None,
                        nargs=argparse.REMAINDER)
    args = parser.parse_args()
    if args.cfg_file is not None:
        merge_cfg_from_file(args.cfg_file)
    if args.opts is not None:
        merge_cfg_from_list(args.opts)
    logger = setup_logger('main-logger')
    logger.info("Called with args: {}".format(args))
    logger.info("Running with cfg:\n{}".format(logger_cfg_from_file(args.cfg_file)))

    # Setup Device
    if torch.cuda.is_available() and cfg.GPU_USE:
        # Set temporary environment variables
        os.environ["CUDA_VISIBLE_DEVICES"] = ','.join(str(x) for x in cfg.GPU_IDS)
        device = "cuda"
    else:
        device = 'cpu'

    # Setup input_transform and augmentations
    input_transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(cfg.DATA.MEAN, cfg.DATA.STD),
    ])

    # Setup Dataloader
    eval_set = dataset.JsonDataset(json_path=cfg.DATA.VAL_JSON,
                                   split=cfg.MODEL.PHASE,
                                   batch_size=cfg.EVAL.BATCH_SIZE,
                                   crop_size=cfg.EVAL.CROP_SIZE,
                                   padding=cfg.EVAL.PADDING,
                                   ignore_label=cfg.EVAL.IGNORE_LABEL,
                                   transform=input_transform)
    eval_loader = torch.utils.data.DataLoader(eval_set, batch_size=cfg.EVAL.BATCH_SIZE, shuffle=None,
                                               pin_memory=True, sampler=None, drop_last=False)

    # Setup Model
    model = generate_model()
    logger.info("Evaluating model:\n\033[1;34m{} \033[0m".format(model))

    # load trained model weights
    model = load_trained_model(model)
    # # Setup result dir
    # if not os.path.isdir(os.path.join(cfg.CKPT, 'results')):
    #     check_mkdir(os.path.join(cfg.CKPT, 'results'))

    # main loop
    logger.info("\n\t\t\t>>>>> Start Evaluating >>>>>")
    eval(model, eval_loader, device, logger)


def eval(model, loader, device, logger):
    # switch to eval model
    model.to(device).eval()

    acc_meter = AverageMeter()
    intersection_meter = AverageMeter()
    union_meter = AverageMeter()

    data_time = AverageMeter()
    infer_time = AverageMeter()

    num_images = len(loader) * cfg.EVAL.BATCH_SIZE
    tic = time.time()
    logger.info('num_images: {} | batch_size: {}'.format(num_images, cfg.EVAL.BATCH_SIZE))
    for index, (images, masks) in enumerate(loader):
        # load data to device
        images = images.to(device)
        labels = masks.numpy()

        # measure data loading time
        data_time.update((time.time() - tic) / cfg.EVAL.BATCH_SIZE)
        tic_ = time.time()

        with torch.no_grad():
            # forward
            outputs = model(images)
            preds = outputs.data.max(1)[1].cpu().numpy()

        infer_time.update((time.time() - tic_) / cfg.EVAL.BATCH_SIZE)

        acc, pix = accuracy(preds, labels)
        intersection, union = intersectionAndUnion(preds, labels, cfg.DATA.CLASSES, cfg.EVAL.IGNORE_LABEL)

        acc_meter.update(acc, pix)
        intersection_meter.update(intersection)
        union_meter.update(union)
        tic = time.time()
        logger.info('Evaluating: Iter_Size:{} | Mean_ACC: {:4.4f} % | Cur_ACC: {:4.4f} % | '
                    'Data_Time_Avg: {:.3f} s | Infer_Time_Avg: {:.3f} s'
                    .format(len(loader), acc_meter.avg * 100., acc * 100., data_time.avg, infer_time.avg))
    iou = intersection_meter.sum / (union_meter.sum + 1e-10)
    for i, _iou in enumerate(iou):
        logger.info('class [{}], IoU: {}'.format(i+1, _iou))
    logger.info('[Eval Summary]: Mean IoU: {:.4}, Accuracy: {:.2f}%'.format(iou.mean(), acc_meter.avg * 100.))


if __name__ == '__main__':
    main()
