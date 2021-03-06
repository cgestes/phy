# -*- coding: utf-8 -*-

"""Test feature plotting."""

#------------------------------------------------------------------------------
# Imports
#------------------------------------------------------------------------------

import numpy as np

from ...utils.logging import set_level
from ..features import FeatureView
from ...utils._color import _random_color
from ...io.mock.artificial import (artificial_features,
                                   artificial_masks,
                                   artificial_spike_clusters,
                                   artificial_spike_samples)
from ...utils.testing import show_test


#------------------------------------------------------------------------------
# Fixtures
#------------------------------------------------------------------------------

def setup():
    set_level('debug')


def teardown():
    pass


#------------------------------------------------------------------------------
# Tests
#------------------------------------------------------------------------------

def _test_features(n_spikes=None, n_clusters=None):
    n_channels = 32
    n_features = 3

    features = artificial_features(n_spikes, n_channels, n_features)
    masks = artificial_masks(n_spikes, n_channels)
    spike_clusters = artificial_spike_clusters(n_spikes, n_clusters)
    spike_samples = artificial_spike_samples(n_spikes).astype(np.float32)

    c = FeatureView()
    c.visual.features = features
    # Useful to test depth.
    # masks[n_spikes//2:, ...] = 0
    c.visual.masks = masks
    c.dimensions = ['time', (0, 0), (1, 0), (2, 0)]
    c.visual.spike_clusters = spike_clusters
    c.visual.spike_samples = spike_samples
    c.visual.cluster_colors = np.array([_random_color()
                                        for _ in range(n_clusters)])

    show_test(c)


def test_features_empty():
    _test_features(n_spikes=0, n_clusters=0)


def test_features_full():
    _test_features(n_spikes=100, n_clusters=3)
