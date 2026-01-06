"""This module is the tools to run on command line."""
from collections.abc import Callable
from typing import Any
from functions import highpass, lowpass
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import csv
import matplotlib as mpl
from pathlib import Path

type _ShapedFArray[
    shape: tuple[int, ...]
] = np.ndarray[
    shape,
    np.dtype[
        np.floating[Any]
    ]
]

type _Array1DF = np.ndarray[
    tuple[int],
    np.dtype[np.floating[Any]]
]


class ExperimentData[
    shape: tuple[int]
]:
    """The data class of the experiment.

    Parameters
    ----------
    v_in : _ShapedFArray[shape]
        The input voltage.
    v_out : _ShapedFArray[shape]
        The output voltage.
    frequency : _ShapedFArray[shape]
        The frequency.
    phi : _ShapedFArray[shape]
        The phase displacement.
    """
    def __init__(
        self,
        v_in: _ShapedFArray[shape],
        v_out: _ShapedFArray[shape],
        frequency: _ShapedFArray[shape],
        phi: _ShapedFArray[shape]
    ) -> None:
        self.v_in = v_in
        self.v_out = v_out
        self.frequency = frequency
        self.phi = phi


def load_data(
    fname: Path,
    encoding: str | None = None
) -> ExperimentData[tuple[int]]:
    """Automatically loads the csv file handed as a command line argument.

    This assumes that the first row is the header and the columns represent

    - Frequency
    - Input Voltage
    - Output Voltage
    - Phase Transition

    respectively.

    Parameters
    ----------
    fname : Path
        The path to the csv file.
    encoding : str | None, optional
        The encoding codec of the file.

    Returns
    -------
    data : ExperimentData[tuple[int]]
        The data.
    """
    lvin: list[float] = list()
    lvout: list[float] = list()
    lf: list[float] = list()
    lphi: list[float] = list()
    if encoding is None:
        encoding = 'utf_8_sig'
    with open(fname, encoding=encoding) as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.read(1024))
        csvfile.seek(0)
        reader = csv.reader(csvfile, dialect=dialect)
        for row in reader:
            if len(row) < 4:
                raise ValueError('Invalid CSV.')
            elif reader.line_num == 1:
                continue
            for i, l in enumerate((lf, lvin, lvout, lphi)):
                l.append(float(row[i]))
    v_in = np.array(lvin)
    v_out = np.array(lvout)
    f = np.array(lf)
    phi = np.array(lphi)
    return ExperimentData(v_in, v_out, f, phi)


def plotter(
    hilo: bool,
    verbose: bool,
    data: ExperimentData,
    tau: float | None = None
) -> tuple[
    _Array1DF,
    _Array1DF,
    _Array1DF,
    Callable[
        [
            _Array1DF,
            np.floating[Any]
        ],
        _Array1DF
    ],
    Callable[
        [
            _Array1DF,
            np.floating[Any],
            np.floating[Any],
            np.floating[Any]
        ],
        _Array1DF
    ],
    Callable[
        [
            _Array1DF,
            np.floating[Any],
            np.floating[Any],
            np.floating[Any]
        ],
        _Array1DF
    ]
]:
    """Fit the curve and outputs the graphs.

    Parameters
    ----------
    hilo : bool
        Whether the data is about the high pass filter or not.
        ``True`` indicates that the value is about high pass filter.
    verbose : bool
        Indicates whether to print parameters or not.
    data : ExperimentData
        The data.
    tau : float | None, optional
        The time constant.

    Returns
    -------
    fit_gain : _Array1DF
        The fitted curve parameters of gain.
    fit_voutcosphi : _Array1DF
        The fitted parameters.
    fit_voutsinphi : _Array1DF
        The fitted parameters.
    f2 : Callable
        The gain function.
    g2 : Callable
        The function of ``v_out * np.cos(phi)``.
    h2 : Callable
        The function to calculate ``v_out \\* np.sin(phi)``.
    """
    f1: Callable[[_Array1DF, _Array1DF], _Array1DF]
    f2: Callable[
        [
            _Array1DF,
            np.floating[Any]
        ],
        _Array1DF
    ]
    g1: Callable[
        [
            _Array1DF,
            _Array1DF
        ],
        _Array1DF
    ]
    g2: Callable[
        [
            _Array1DF,
            np.floating[Any],
            np.floating[Any],
            np.floating[Any]
        ],
        _Array1DF
    ]
    h1: Callable[
        [
            _Array1DF,
            _Array1DF
        ],
        _Array1DF
    ]
    h2: Callable[
        [
            _Array1DF,
            np.floating[Any],
            np.floating[Any],
            np.floating[Any]
        ],
        _Array1DF
    ]
    if tau is None:
        tau = 1e-4
    if hilo:
        f1 = highpass.calc_gain_direct
        f2 = highpass.calc_gain_from_theory
        g1 = highpass.calc_voutcosphi_direct
        g2 = highpass.calc_voutcosphi_from_theory
        h1 = highpass.calc_voutsinphi_direct
        h2 = highpass.calc_voutsinphi_from_theory
    else:
        f1 = lowpass.calc_gain_direct
        f2 = lowpass.calc_gain_from_theory
        g1 = lowpass.calc_voutcosphi_direct
        g2 = lowpass.calc_voutcosphi_from_theory
        h1 = lowpass.calc_voutsinphi_direct
        h2 = lowpass.calc_voutsinphi_from_theory
    points_gain = f1(data.v_in, data.v_out)
    fit_gain, err_gain = curve_fit(
        f2,
        data.frequency,
        points_gain,
        np.array(
            (
                tau,
            )
        )
    )
    points_voutcosphi = g1(data.v_out, data.phi)
    fit_voutcosphi, err_voutcosphi = curve_fit(
        g2,
        data.frequency,
        points_voutcosphi,
        np.array(
            (
                tau,
                np.mean(data.v_in),
                0
            )
        )
    )
    points_voutsinphi = h1(data.v_out, data.phi)
    fit_voutsinphi, err_voutsinphi = curve_fit(
        h2,
        data.frequency,
        points_voutsinphi,
        np.array(
            (
                tau,
                np.mean(data.v_in),
                0
            )
        )
    )
    ax1: mpl.axes.Axes
    ax2: mpl.axes.Axes
    ax3: mpl.axes.Axes
    _, (ax1, ax2, ax3) = plt.subplots(1, 3,
                                      subplot_kw=dict(box_aspect=8 / 13))
    frange = np.log10(np.max(data.frequency) / np.min(data.frequency))
    fremin = np.log10(np.min(data.frequency)) - frange * .05
    fremin = 10 ** fremin
    fremax = np.log10(np.max(data.frequency)) + frange * .05
    fremax = 10 ** fremax
    ax1.plot(data.frequency, points_gain, '.')
    fs1 = np.geomspace(fremin, fremax)
    ax1.plot(fs1, f2(fs1, *fit_gain), '-')
    ax1.set_xscale('log')
    ax2.plot(data.frequency, points_voutcosphi, '.')
    ax2.plot(fs1, g2(fs1, *fit_voutcosphi), '-')
    ax2.set_xscale('log')
    ax3.plot(data.frequency, points_voutsinphi, '.')
    ax3.plot(fs1, h2(fs1, *fit_voutsinphi), '-')
    ax3.set_xscale('log')
    plt.show()
    if verbose:
        print('Gain Parameter:', fit_gain)
        print('Standard error of the gain parameter:')
        print(np.sqrt(np.diag(err_gain)))
        print('V_out cos Phi')
        print('[tau, V_in, Phi_1] =', fit_voutcosphi)
        print('Satandard Errors:')
        print(np.sqrt(np.diag(err_voutcosphi)))
        print('V_out sin Phi')
        print('[tau, V_in, Phi_1] =', fit_voutsinphi)
        print('Standard Errors:')
        print(np.sqrt(np.diag(err_voutsinphi)))
    return fit_gain, fit_voutcosphi, fit_voutsinphi, f2, g2, h2


def save_point(
    target: Path,
    fit_gain: _Array1DF,
    fit_voutcosphi: _Array1DF,
    fit_voutsinphi: _Array1DF,
    f2: Callable[
        [
            _Array1DF,
            np.floating[Any]
        ],
        _Array1DF
    ],
    g2: Callable[
        [
            _Array1DF,
            np.floating[Any],
            np.floating[Any],
            np.floating[Any]
        ],
        _Array1DF
    ],
    h2: Callable[
        [
            _Array1DF,
            np.floating[Any],
            np.floating[Any],
            np.floating[Any]
        ],
        _Array1DF
    ]
) -> None:
    """Outputs the result points onto a csv file.

    This also outputs the raw parameters.

    Parameters
    ----------
    target : Path
        The output path.
    fit_gain : _Array1DF
        The parameters of ``f2``.
    fit_voutcosphi : _Array1DF
        The parameters of ``g2``.
    fit_voutsinphi : _Array1DF
        The parameters of ``h2``.
    f2 : Callable
    g2 : Callable
    h2 : Callable
    """
    r1 = np.arange(10, 50, 1)
    r2 = np.arange(50, 100, 2)
    r3 = np.arange(100, 500, 10)
    r4 = np.arange(500, 1000, 20)
    r5 = np.arange(1000, 5000, 100)
    r6 = np.arange(5000, 10000, 200)
    r7 = np.arange(1e4, 5e4, 1e3)
    r8 = np.arange(5e4, 1e5, 2e3)
    r9 = np.arange(1e5, 5e5, 1e4)
    r10 = np.arange(5e5, 1e6, 2e4)
    frequency = np.array((*r1, *r2, *r3, *r4, *r5, *r6, *r7, *r8, *r9, *r10,))
    with open(target, 'w', encoding='utf_8_sig', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                'f / Hz',
                'G / dB',
                'V(out) cos Phi / V',
                'V(out) sin Phi / V',
            )
        )
        gain = f2(frequency, *fit_gain)
        voutcosphi = g2(frequency, *fit_voutcosphi)
        voutsinphi = h2(frequency, *fit_voutsinphi)
        for i in range(len(gain)):
            writer.writerow(
                (
                    frequency[i],
                    gain[i],
                    voutcosphi[i],
                    voutsinphi[i],
                )
            )
