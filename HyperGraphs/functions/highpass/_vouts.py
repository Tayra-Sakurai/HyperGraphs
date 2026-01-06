"""Calculates the voltage component orthorogical to the input voltage.

Both theoretical and experimental values are supported.
"""
from .._types import _Array1D, _ArrayInShape
import numpy as np
from typing import Any


def calc_voutsinphi_direct[
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
    """Calculates the orthorogical component experimentally.

    Parameters
    ----------
    v_out : _Array1D
        The outputs.
    phi : _Array1D
        The displacement of the phases.

    Returns
    -------
    voutsinphi : _Array1D
        The experimental value.
    """
    return v_out * np.sin(phi)


def calc_voutsinphi_from_theory(
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
        The value of the output voltage component orthological to the input.
    """
    omegatau = 2 * np.pi * tau * frequency
    den = omegatau ** 2 + 1
    den = np.sqrt(den)
    sine = 1 / den
    cosine = - omegatau / den
    sineval = sine * np.cos(phi_1) + cosine * np.sin(phi_1)
    vout = v_in / np.sqrt(omegatau ** (-2) + 1)
    return vout * sineval
