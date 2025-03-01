#!/usr/bin/env python
import yaml

""" Configuration file."""

import os
import os.path as osp

import sys
from easydict import EasyDict as edict

from enum import Enum
import pdb


class phase(Enum):
    TRAIN = "train"
    VAL = "val"
    TESTDEV = "test-dev"
    TRAINVAL = "train-val"


__C = edict()

# Public access to configuration settings
cfg = __C

# Number of CPU cores used to parallelize evaluation.
__C.N_JOBS = 32

# Paths to dataset folders
__C.PATH = edict()

# Dataset resolution: ("480p","1080p")
__C.RESOLUTION = "480p"

# Dataset year: ("2016","2017")
__C.YEAR = "2016"

__C.PHASE = phase.VAL

# Multiobject evaluation (Set to False only when evaluating DAVIS 2016)
__C.MULTIOBJECT = True

# Root folder of project
__C.PATH.ROOT = osp.abspath("../../VIDNet/")

# Data folder
__C.PATH.DATA = osp.abspath("../databases/DAVIS2016/")

# Path to input images
__C.PATH.ORIGINAL = osp.join(__C.PATH.DATA, "JPEGImages", __C.RESOLUTION)

__C.PATH.SEQUENCES2 = "/#FIXME/model/Deep-Video-Inpainting/results/vi_davis"  # FIXME
__C.PATH.SEQUENCES = "/#FIXME/model/opn-demo/vi_davis"  # FIXME

__C.PATH.FLOW = "../../flownet2-pytorch/result/inference/run.epoch-0-flow-field"

# Path to annotations
__C.PATH.ANNOTATIONS = osp.join(__C.PATH.DATA, "Annotations", __C.RESOLUTION)

# Color palette
__C.PATH.PALETTE = osp.abspath(osp.join(__C.PATH.ROOT, "src/dataloader/palette.txt"))

# Paths to files
__C.FILES = edict()

# Path to property file, holding information on evaluation sequences.
__C.FILES.DB_INFO = osp.abspath(osp.join(__C.PATH.ROOT, "src/dataloader/db_info.yaml"))
# __C.FILES.DB_INFO = osp.abspath(osp.join(__C.PATH.ROOT,"src/dataloader/freeform_db.yaml"))

# Measures and Statistics
__C.EVAL = edict()

# Metrics: J: region similarity, F: contour accuracy, T: temporal stability
__C.EVAL.METRICS = ["J", "F"]

# Statistics computed for each of the metrics listed above
__C.EVAL.STATISTICS = ["mean", "recall", "decay"]


def db_read_info():
    """Read dataset properties from file."""
    with open(cfg.FILES.DB_INFO, "r") as f:
        return edict(yaml.load(f))


def db_read_attributes():
    """Read list of sequences."""
    return db_read_info().attributes


def db_read_years():
    """Read list of sequences."""
    return db_read_info().years


def db_read_sequences(year=None, db_phase=None):
    """Read list of sequences."""
    # pdb.set_trace()
    sequences = db_read_info().sequences

    if year is not None:
        sequences = filter(lambda s: int(s.year) <= int(year), sequences)

    if db_phase is not None:
        if db_phase == phase.TRAINVAL:
            sequences = filter(lambda s: ((s.set == phase.VAL) or (s.set == phase.TRAIN)), sequences)
        else:
            sequences = filter(
                lambda s: s.set == db_phase and osp.isdir(osp.join(__C.PATH.SEQUENCES, s.name)), sequences
            )
    return sequences


# Load all sequences
__C.SEQUENCES = dict([(sequence.name, sequence) for sequence in db_read_sequences()])

import numpy as np

__C.palette = np.loadtxt(__C.PATH.PALETTE, dtype=np.uint8).reshape(-1, 3)
