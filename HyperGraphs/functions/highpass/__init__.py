"""This is the functions about the values of the high-pass filter.

Gain Functions
--------------
Functions to calculate gain.

.. autosummary::
   :toctree: generated/

   calc_gain_direct
   calc_gain_from_theory

Same-Phase Component
--------------------
Functions to calculate the same-phase voltage of the output.

.. autosummary::
   :toctree: generated/

   calc_voutcosphi_direct
   calc_voutcosphi_from_theory

Orthological-Phase Component
----------------------------
Clalculates the orthological component of the output voltage.

.. autosummary::
   :toctree: generated/

   calc_voutsinphi_direct
   calc_voutsinphi_from_theory
"""
from ._gain import *
from ._voutc import *
from ._vouts import *
