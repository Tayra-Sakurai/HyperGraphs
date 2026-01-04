"""Functions to calculate the same phase dimention of the output voltage.

This module is for high pass filters.
"""
from typing import Any
import numpy as np
from .._types import _ArrayInShape, _Array1D


def calc_voutcosphi_direct[
    _shape1D: tuple[int]
](
    v_out: _ArrayInShape[
        _shape1D,
        np.floating[Any]
    ],
    phi: _ArrayInShape[
        _shape1D,
        np.floating[Any]
    ]
) -> _ArrayInShape[
    _shape1D,
    np.floating[Any]
]:
    """Calculates the value of the same-phase component of the output.

    This calculates it directly from the value.

    Parameters
    ----------
    v_out : _Array1D
        The array of the output voltages.
    phi : _Array1D
        The same shape array which represents the phase changes.

    Returns
    -------
    voutcosphi : _Array1D
        The calculated values.
    """
    return v_out * np.cos(phi)


def calc_voutcosphi_from_theory(
    frequency: _Array1D,
    tau: np.floating[Any],
    v_in: np.floating[Any],
    phi_1: np.floating[Any]
) -> _Array1D:
    """Calculates the theoetical value of the component.

    The value is derived from the time constant, input voltage,
    and the phase change of the voltage follower.

    Parameters
    ----------
    frequency : _Array1D
        The frequency data.
    tau : floating[Any]
        The time constant.
    v_in : floating[Any]
        The input voltage.
    phi_1 : floating[Any]
        The phase change of the voltage follower.

    Returns
    -------
    voutcosphi : _Array1D
        The same-phase value of the output voltage.
    """
    omegatau = 2 * np.pi * tau * frequency
    den = omegatau ** 2 + 1
    den = np.sqrt(den)
    sine = 1 / den
    cosine = - omegatau / den
    cosineval = cosine * np.cos(phi_1) - sine * np.sin(phi_1)
    vout = v_in / np.sqrt(omegatau ** (-2) + 1)
    return vout * cosineval
