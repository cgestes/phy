# -*- coding: utf-8 -*-

"""Mock Kwik files."""

#------------------------------------------------------------------------------
# Imports
#------------------------------------------------------------------------------

import os.path as op

import numpy as np

from ...io.mock.artificial import (artificial_spike_samples,
                                   artificial_spike_clusters,
                                   artificial_features,
                                   artificial_masks,
                                   artificial_traces)
from ...electrode.mea import staggered_positions
from ..h5 import open_h5
from ..kwik_model import _kwik_filenames, _create_clustering


#------------------------------------------------------------------------------
# Mock Kwik file
#------------------------------------------------------------------------------

def create_mock_kwik(dir_path, n_clusters=None, n_spikes=None,
                     n_channels=None, n_features_per_channel=None,
                     n_samples_traces=None,
                     with_kwx=True, with_kwd=True):
    """Create a test kwik file."""
    filename = op.join(dir_path, '_test.kwik')
    filenames = _kwik_filenames(filename)
    kwx_filename = filenames['kwx']
    kwd_filename = filenames['raw.kwd']

    # Create the kwik file.
    with open_h5(filename, 'w') as f:
        f.write_attr('/', 'kwik_version', 2)

        def _write_metadata(key, value):
            f.write_attr('/application_data/spikedetekt', key, value)

        _write_metadata('sample_rate', 20000.)

        # Filter parameters.
        _write_metadata('filter_low', 500.)
        _write_metadata('filter_high', 0.95 * .5 * 20000.)
        _write_metadata('filter_butter_order', 3)

        _write_metadata('extract_s_before', 15)
        _write_metadata('extract_s_after', 25)

        _write_metadata('nfeatures_per_channel', n_features_per_channel)

        # Create spike times.
        spike_samples = artificial_spike_samples(n_spikes).astype(np.int64)
        spike_recordings = np.zeros(n_spikes, dtype=np.uint16)
        # Size of the first recording.
        recording_size = 2 * n_spikes // 3
        # Find the recording offset.
        recording_offset = spike_samples[recording_size]
        recording_offset += spike_samples[recording_size + 1]
        recording_offset //= 2
        spike_recordings[recording_size:] = 1
        # Make sure the spike samples of the second recording start over.
        spike_samples[recording_size:] -= spike_samples[recording_size]
        spike_samples[recording_size:] += 10

        if spike_samples.max() >= n_samples_traces:
            raise ValueError("There are too many spikes: decrease 'n_spikes'.")

        f.write('/channel_groups/1/spikes/time_samples', spike_samples)
        f.write('/channel_groups/1/spikes/recording', spike_recordings)
        f.write_attr('/channel_groups/1',
                     'channel_order',
                     np.arange(1, n_channels - 1)[::-1],
                     )

        # Create channels.
        positions = staggered_positions(n_channels)
        for channel in range(n_channels):
            group = '/channel_groups/1/channels/{0:d}'.format(channel)
            f.write_attr(group, 'name', str(channel))
            f.write_attr(group, 'position', positions[channel])

        # Create spike clusters.
        clusterings = [('main', n_clusters),
                       ('automatic', n_clusters * 2),
                       ]
        for clustering, n_clusters_rec in clusterings:
            spike_clusters = artificial_spike_clusters(n_spikes,
                                                       n_clusters_rec)
            _create_clustering(f, clustering, 1, spike_clusters)

        # Create recordings.
        f.write_attr('/recordings/0', 'name', 'recording_0')
        f.write_attr('/recordings/1', 'name', 'recording_1')

    # Create the kwx file.
    if with_kwx:
        with open_h5(kwx_filename, 'w') as f:
            f.write_attr('/', 'kwik_version', 2)
            features = artificial_features(n_spikes,
                                           (n_channels - 2) *
                                           n_features_per_channel)
            masks = artificial_masks(n_spikes,
                                     (n_channels - 2) *
                                     n_features_per_channel)
            fm = np.dstack((features, masks)).astype(np.float32)
            f.write('/channel_groups/1/features_masks', fm)

    # Create the raw kwd file.
    if with_kwd:
        with open_h5(kwd_filename, 'w') as f:
            f.write_attr('/', 'kwik_version', 2)
            traces = artificial_traces(n_samples_traces, n_channels)
            # TODO: int16 traces
            f.write('/recordings/0/data',
                    traces[:recording_offset, ...].astype(np.float32))
            f.write('/recordings/1/data',
                    traces[recording_offset:, ...].astype(np.float32))

    return filename
