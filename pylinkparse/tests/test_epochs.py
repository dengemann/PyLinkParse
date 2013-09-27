import numpy as np
from numpy.testing import assert_equal
from pylinkparse import Raw, Epochs

path = 'pylinkparse/tests/data/'
fname = path + 'test_raw.asc'


def test_epochs_io():
    """Test essential basic IO functionality"""
    tmin, tmax, event_id = -0.5, 1.5, 999
    events = np.array([[1000, 999], [10000, 999], [12000, 77]])
    raw = Raw(fname)
    epochs = Epochs(raw, events, event_id, tmin, tmax)
    print epochs  # test repr works
    assert_equal(len(epochs.events), 2)
    assert_equal(epochs._samples.shape[0] / epochs._n_times,
                 len(epochs.events))
