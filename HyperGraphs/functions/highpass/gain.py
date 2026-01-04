"""This is the module to calculate gains."""
import numpy as np
from typing import Any
from .._types import _Array1D, _ArrayInShape


def calc_gain_direct[
    _shape1D: tuple[int]
](
    v_in: _ArrayInShape[
        _shape1D,
        np.floating[Any]
    ],
    v_out: _ArrayInShape[
        _shape1D,
        np.floating[Any]
    ]
) -> _ArrayInShape[
    _shape1D,
    np.float64
]:
    """Calculates the gain directly from the input and output voltage.

    Parameters
    ----------
    v_in : _Array1D
        The input voltages.
    v_out : _Array1D
        The output voltages. Must be one-to-one correspondent onto ``v_in``.

    Returns
    -------
    gain : _Array1D
        The gain values.

    Notes
    -----
    Please do not call this function directly.
    """
    return 20 * np.log10(v_out / v_in)


def calc_gain_from_theory(
    frequency: _Array1D,
    tau: np.floating[Any]
) -> _Array1D:
    """Calculates the theoretical gain value.

    Parameters
    ----------
    frequency : _Array1D
        The values of frequencies of the voltage of source.
    tau : floating[Any]
        The time constant.

    Returns
    -------
    gain : _Array1D
        The derived gain values.

    Notes
    -----
    This is made to be used in the ``scipy.optimize.curve_fit`` function.

    The function is not considered to be called by users directly.
    """
    omega = 2 * np.pi * frequency
    squared = (1 / (omega * tau)) ** 2 + 1
    denominator = np.sqrt(squared)
    return 20 * np.log10(1 / denominator)
