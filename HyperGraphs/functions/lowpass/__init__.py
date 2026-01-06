"""This is the functions about the values of the low-pass filter.

Gain Functions
--------------
.. autosummary::
   :toctree: generated/

   calc_gain_direct
   calc_gain_from_theory

Same-Phase Component
--------------------
.. autosummary::
   :toctree: generated/

   calc_voutcosphi_direct
   calc_voutcosphi_from_theory

Orthological-Phase Component
----------------------------
.. autosummary::
   :toctree: generated/

   calc_voutsinphi_direct
   calc_voutsinphi_from_theory
"""
from ._gain import *
from ._voutc import *
from ._vouts import *
