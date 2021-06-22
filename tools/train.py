import os
import torch
import argparse

from torchvision import transforms

import _init_path
from config.config import cfg, merge_cfg_from_file, merge_cfg_from_list, logger_cfg_from_file
from dataset import dataset, set_augmentations
from models.model_zone import generate_model
from solver.loss import set_loss
from solver.optimizer import set_optimizer
from solver.scheduler import set_scheduler
from utils.utils import setup_logger, setup_seed


def main():
    # Setup Config
    parser = argparse.ArgumentParser(description='Semantic Segmentation Model Training')
    parser.add_argument('--cfg', dest='cfg_file', default='config/ade20k/ade20k_bisenet.yaml',
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

    # Setup Random Seed
    setup_seed(cfg.SEED)

    # Setup input_transform and augmentations
    input_transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(cfg.DATA.MEAN, cfg.DATA.STD),
    ])
    input_augmentation = set_augmentations(cfg)
    # Setup Dataloader
    train_set = dataset.JsonDataset(json_path=cfg.DATA.TRAIN_JSON, transform=input_transform,
                                    augmentations=input_augmentation)
    train_loader = torch.utils.data.DataLoader(train_set, batch_size=8, shuffle=None, pin_memory=True, sampler=None, drop_last=True)
    # Setup Model
    model = generate_model()
    logger.info("Training model:\n\033[1;34m{} \033[0m".format(model))
    x = torch.rand((2, 3, 512, 512))
    o = model(x)
    print(o[0].size())
    # Setup Loss
    criterion = set_loss()
    # Setup Optimizer
    optimizer = set_optimizer(model)
    # Setup Scheduler
    scheduler = set_scheduler(optimizer)

    # main loop
    for epoch in range(1, cfg.TRAIN.EPOCHS+1):
        train(model, train_loader, criterion, optimizer, scheduler, epoch)


def train(model, loader, criterion, optimizer, scheduler, epoch):
    pass


if __name__ == '__main__':
    main()
