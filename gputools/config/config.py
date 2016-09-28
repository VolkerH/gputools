import logging

logging.basicConfig(level=logging.INFO)

import os
import numpy as np
import pyopencl
from gputools.config.myconfigparser import MyConfigParser
from gputools.core.ocldevice import OCLDevice

cl_datatype_dict = {pyopencl.channel_type.FLOAT: np.float32,
                    pyopencl.channel_type.UNSIGNED_INT8: np.uint8,
                    pyopencl.channel_type.UNSIGNED_INT16: np.uint16,
                    pyopencl.channel_type.SIGNED_INT8: np.int8,
                    pyopencl.channel_type.SIGNED_INT16: np.int16,
                    pyopencl.channel_type.SIGNED_INT32: np.int32}

cl_datatype_dict.update({dtype: cltype for cltype, dtype in cl_datatype_dict.iteritems()})

__CONFIGFILE__ = os.path.expanduser("~/.gputools")

config_parser = MyConfigParser(__CONFIGFILE__)

__ID_DEVICE__ = int(config_parser.get("id_device", 0))
__ID_PLATFORM__ = int(config_parser.get("id_platform", 0))
__USE_GPU__ = int(config_parser.get("use_gpu", 1))


class _ocl_globals(object):
    device = OCLDevice(id_platform=__ID_PLATFORM__,
                       id_device=__ID_DEVICE__,
                       use_gpu=__USE_GPU__)


def init_device(**kwargs):
    """same arguments as OCLDevice.__init__
    e.g.
    id_platform = 0
    id_device = 1
    ....
    """
    new_device = OCLDevice(**kwargs)

    # just change globals if new_device is different from old
    if _ocl_globals.device.device!=new_device.device:
        _ocl_globals.device = new_device


def get_device():
    return _ocl_globals.device