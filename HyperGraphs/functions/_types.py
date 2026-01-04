"""The typing module for the function type anntations.

This includes some major types.
"""
import numpy as np
from typing import Any

type _Array1D = np.ndarray[
    tuple[int],
    np.dtype[np.number[Any]]
]
type _ArrayInShape[
    _shape: tuple[int, ...],
    _type: Any
] = np.ndarray[
    _shape,
    np.dtype[_type]
]
