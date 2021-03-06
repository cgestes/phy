# -*- coding: utf-8 -*-

"""Test CCG plotting."""

#------------------------------------------------------------------------------
# Imports
#------------------------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt

from ..ccg import plot_ccg
from ...utils.logging import set_level
from ..ccg import CorrelogramView
from ...utils._color import _random_color
from ...io.mock.artificial import artificial_correlograms
from ...utils.testing import show_test


#------------------------------------------------------------------------------
# Tests matplotlib
#------------------------------------------------------------------------------

def test_plot_ccg():
    n_bins = 51
    ccg = np.random.randint(size=n_bins, low=10, high=50)
    plot_ccg(ccg, baseline=20, color='g')
    # plt.show()


#------------------------------------------------------------------------------
# Tests VisPy
#------------------------------------------------------------------------------

def _test_correlograms(n_clusters=None):
    n_samples = 51

    correlograms = artificial_correlograms(n_clusters, n_samples)

    c = CorrelogramView()
    c.cluster_ids = np.arange(n_clusters)
    c.visual.correlograms = correlograms
    c.visual.cluster_colors = np.array([_random_color()
                                        for _ in range(n_clusters)])

    show_test(c)


def test_correlograms_empty():
    _test_correlograms(n_clusters=0)


def test_correlograms_full():
    _test_correlograms(n_clusters=3)
