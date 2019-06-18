import numpy as np
import pytest
from functools import partial

from pyeparse import read_raw, Epochs
from pyeparse.viz import _epochs_axes_onclick, _epochs_navigation_onclick
from pyeparse.utils import _get_test_fnames, _requires_edfapi

fnames = _get_test_fnames()


class DummyEvent(object):
    """Dummy event."""

    def __init__(self, ax):
        self.inaxes = ax


@_requires_edfapi
def test_raw_plot():
    """Test plotting of raw."""
    for fi, fname in enumerate(fnames):
        raw = read_raw(fname)
        raw.plot_calibration()
        raw.plot_heatmap(0., 10., vmax=1)
        raw.plot_heatmap(0., 10., kernel=None)
        raw.plot()


@_requires_edfapi
def test_epochs_plot():
    """Test plotting of epochs."""
    tmin, tmax, event_id = -0.5, 1.5, 999
    # create some evil events
    events = np.array([[1000, 999], [2000, 999], [3000, 999]])
    for fname in fnames:
        raw = read_raw(fname)
        epochs = Epochs(raw, events, event_id, tmin, tmax)
        pytest.raises(ValueError, epochs.plot, picks=['whatever'])
        epochs.plot(picks=['ps'])
        fig = epochs.plot(n_chunks=2)
        epochs.plot(draw_discrete='saccades')

    # test clicking: find our callbacks
    for func in fig.canvas.callbacks.callbacks['button_press_event'].items():
        func = func[1]
        try:
            func = func()
        except Exception:  # old MPL
            func = func.func
        if isinstance(func, partial):
            break
    params = func.keywords['params']
    for ax in fig.axes:
        _epochs_axes_onclick(DummyEvent(ax), params)

    # nav clicking
    _epochs_navigation_onclick(DummyEvent(params['next'].ax), params)
    _epochs_navigation_onclick(DummyEvent(params['back'].ax), params)
    _epochs_navigation_onclick(DummyEvent(params['reject-quit'].ax), params)
