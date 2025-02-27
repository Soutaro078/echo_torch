# -*- coding: utf-8 -*-
#
# File : echotorch/utils/matrix_generation/MatrixGenerator.py
# Description : Matrix generator base class.
# Date : 29th of October, 2019
#
# This file is part of EchoTorch.  EchoTorch is free software: you can
# redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright Nils Schaetti <nils.schaetti@unine.ch>

# Import
import torch
import scipy.io as io
import numpy as np
from .MatrixGenerator import MatrixGenerator
from .MatrixFactory import matrix_factory
import echotorch.utils
import scipy.sparse


# Load matrix from Numpy file
class NumpyLoader(MatrixGenerator):
    """
    Load matrix from Numpy file
    """

    # Constructor
    def __init__(self, **kwargs):
        """
        Constructor
        :param kwargs: Parameters of the generator
        """
        # Set default parameter values
        super(NumpyLoader, self).__init__(
            spectral_radius=1.0,
            apply_spectral_radius=False,
            scale=1.0
        )

        # Set parameters
        self._set_parameters(args=kwargs)
    # end __init__

    #region PRIVATE

    # Generate the matrix
    def _generate_matrix(self, size, dtype=torch.float64):
        """
        Generate the matrix
        :param size: Matrix size (ignored)
        :param dtype: Data type
        :return: Generated matrix
        """
        # Params
        file_name = self.get_parameter('file_name')

        # Load matrix
        m = np.load(file_name)

        # Reshape
        if 'shape' in list(self._parameters.keys()):
            m = np.reshape(m, self.get_parameter('shape'))
        # end if

        # Dense or not
        if isinstance(m, scipy.sparse.csc_matrix):
            m = torch.from_numpy(m.todense()).type(dtype)
        else:
            m = torch.from_numpy(m).type(dtype)
        # end if

        return m
    # end _generate_matrix

    #endregion PRIVATE

# end MatlabLoader


# Add
matrix_factory.register_generator("numpy", NumpyLoader)
