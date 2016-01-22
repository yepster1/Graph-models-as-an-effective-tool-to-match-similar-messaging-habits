from distutils.core import setup
from Cython.Build import cythonize
import os
from scipy.sparse import csr_matrix
import scipy.sparse.linalg as lin
import numpy as np
from scipy import sparse
import copy
import shutil
import time

cdef numpy.ndarray unitVector(vector):
    return np.divide(vector,np.linalg.norm(vector))
