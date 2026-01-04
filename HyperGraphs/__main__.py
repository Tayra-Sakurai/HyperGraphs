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
                            action='store_false',
                            help='Turn on the low pass mode.')
    parser.add_argument('--encoding',
                        type=str,
                        help='The file encoding.')
    parser.add_argument('-o',
                        '--output',
                        type=Path,
                        help='Output file path.')
    args = parser.parse_args()
    data = HyperGraphs.load_data(args.csvfile,
                                 args.encoding)
    hilo: bool
    if args.highpass:
        hilo = True
    elif args.lowpass:
        hilo = False
    else:
        raise TypeError('Invalid args.')
    k = HyperGraphs.plotter(hilo,
                        data)
    if args.output is not None:
        HyperGraphs.save_point(args.output, *k)


if __name__ == '__main__':
    main()
