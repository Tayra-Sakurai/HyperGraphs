"""This calculates the gain of the low-pass filter."""
import numpy as np
from ..highpass import _gain
from typing import Any
from .._types import _Array1D

calc_gain_direct = _gain.calc_gain_direct


def calc_gain_from_theory(
    frequency: _Array1D,
    tau: np.floating[Any]
) -> _Array1D:
    """Calculates the gain theoretically.

    Parameters
    ----------
    frequency : _Array1D
        The frequency.
    tau : floating[Any]
        The time constant.

    Returns
    -------
    gain : _Array1D
        The gain.
    """
    tauomega = 2 * np.pi * tau * frequency
    return 10 * np.log10(1 / (tauomega ** 2 + 1))
