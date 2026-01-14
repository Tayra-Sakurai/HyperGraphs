"""Calculates the voltage component orthorogical to the input voltage.

Both theoretical and experimental values are supported.
"""
from .._types import _Array1D
import numpy as np
from typing import Any
from ..highpass import _vouts

calc_voutsinphi_direct = _vouts.calc_voutsinphi_direct


def calc_voutsinphi_from_theory(
    frequency: _Array1D,
    tau: np.floating[Any],
    v_in: np.floating[Any],
    phi_1: np.floating[Any] = 0
) -> _Array1D:
    """This is the theoretical value calculator.

    Parameters
    ----------
    v_out : _Array1D
        The frequency.
    tau : floating[Any]
        The time constant.
    v_in : floating[Any]
        The input voltage.
    phi_1 : floating[Any], optional
        The phase change.

    Returns
    -------
    voutcosphi : _Array1D
        The value.

    Notes
    -----
    Please do not call this function directly.
    Instead, please give this to ``scipy.optimize.curve_fit``.

    See Also
    --------
    highpass.calc_voutsinphi_from_theory : for details.
    """
    tauomega = 2 * np.pi * tau * frequency
    den = np.sqrt(tauomega ** 2 + 1)
    cosine = 1 / den
    sine = - tauomega / den
    sineval = sine * np.cos(phi_1) + cosine * np.sin(phi_1)
    v_out = v_in / den
    return v_out * sineval
