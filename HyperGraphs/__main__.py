"""This file is conducted on command line.

Please call this.
"""
import argparse
import HyperGraphs
from pathlib import Path

def main() -> None:
    """Main suite."""
    parser = argparse.ArgumentParser()
    parser.add_argument('csvfile',
                        type=Path,
                        help='The data file path.')
    hiloswitch = parser.add_mutually_exclusive_group(required=True)
    hiloswitch.add_argument('--highpass',
                            action='store_true',
                            help='Turn on the high pass filter mode.')
    hiloswitch.add_argument('--lowpass',
                            action='store_true',
                            help='Turn on the low pass mode.')
    parser.add_argument('--encoding',
                        type=str,
                        help='The file encoding.')
    parser.add_argument('-v',
                        '--verbose',
                        help='Indicates whether the parameters are displayed.',
                        action='store_true')
    parser.add_argument('-o',
                        '--output',
                        type=Path,
                        help='Output file path.')
    parser.add_argument('-t',
                        '--tau',
                        type=float,
                        help='The expected value of time constant.',
                        default=1e-4)
    parser.add_argument('--nophi1',
                        action='store_true',
                        help='Ignore the phase changes in voltage follower.')
    args = parser.parse_args()
    data = HyperGraphs.load_data(args.csvfile,
                                 args.encoding)
    hilo: bool
    verbose: bool = False
    if args.highpass:
        hilo = True
    elif args.lowpass:
        hilo = False
    else:
        raise TypeError('Invalid args.')
    if args.verbose:
        verbose = True
    k = HyperGraphs.plotter(
        hilo,
        verbose,
        data,
        args.tau,
        args.nophi1
    )
    if args.output is not None:
        HyperGraphs.save_point(args.output, *k)


if __name__ == '__main__':
    main()
