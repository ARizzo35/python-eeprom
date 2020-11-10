#!/usr/bin/env python3

import cbor2
from eeprom.eeprom import EEPROM
from eeprom.util import check_device_exists


class CBOR_EEPROM(EEPROM):

    _chunk_size = 1024
    _data = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def write(self, *args, **kwargs):
        super().write(*args, **kwargs)
        self._data = None

    def read_file(self):
        if self._data is None:
            # Pre-check if EEPROM is empty
            if self.read(1) == b'\xff':
                self._data = {}
                return self._data
            rd_data = b''
            for x in range(0, self._size, self._chunk_size):
                remaining = self._size - x
                sz = self._chunk_size if remaining > self._chunk_size else remaining
                rd_data += self.read(sz, addr=x)
                try:
                    self._data = cbor2.loads(rd_data)
                    break
                except Exception:
                    self._data = None
            if self._data is None or len(self._data) == 0:
                self._data = {}
        return self._data

    def write_file(self, d):
        if self._data is None:
            if self._data == d:
                return
        self._data = None # Clear cache before writing new data
        self.write(cbor2.dumps(d))
        self._data = d # Update cached data

    def erase_file(self):
        # Invalidate file
        self.write(b'\xff')
        self._data = {}

    def get(self, name):
        if self._data is None:
            self.read_file()
        return self._data.get(name, None)

    def put(self, name, val):
        if self._data is None:
            self.read_file()
        update_data = self._data.copy()
        update_data[name] = val
        self.write_file(update_data)

def main():
    import argparse
    import ast
    import sys

    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
            description="EEPROM data storage using CBOR files")
    subparsers = parser.add_subparsers(dest='command', required=True, title="commands",
            description="available commands")

    check_help = "Check if EEPROM device is present"
    check_cmd = subparsers.add_parser('check', help=check_help, description=check_help)
    check_cmd.add_argument("-b", "--bus", type=int, default=None, required=True,
            help="EEPROM I2C bus (required)")
    check_cmd.add_argument("-a", "--address", type=str, default=None, required=True,
            help="EEPROM I2C address (required)")

    file_cmd = subparsers.add_parser('file', help="Manage file stored in EEPROM")
    file_cmd.add_argument('file_cmd', type=str, choices=["read", "write", "erase"],
            help="Read/write CBOR data file stored in EEPROM")
    file_cmd.add_argument("-t", "--type", type=str, default=None, required=True,
            help="EEPROM device type string (required)")
    file_cmd.add_argument("-b", "--bus", type=int, default=None, required=True,
            help="EEPROM I2C bus (required)")
    file_cmd.add_argument("-a", "--address", type=str, default=None, required=True,
            help="EEPROM I2C address (required)")
    file_cmd.add_argument("-f", "--file", type=str, default=None, required=False,
            help="Local file path (required for write)")

    data_cmd = subparsers.add_parser('data', help="Manage CBOR data objects stored in EEPROM")
    data_cmd.add_argument("data_cmd", type=str, choices=["get", "put"],
            help="Get/put CBOR object")
    data_cmd.add_argument("-t", "--type", type=str, default=None, required=True,
            help="EEPROM device type string (required)")
    data_cmd.add_argument("-b", "--bus", type=int, default=None, required=True,
            help="EEPROM I2C bus (required)")
    data_cmd.add_argument("-a", "--address", type=str, default=None, required=True,
            help="EEPROM I2C address (required)")
    data_cmd.add_argument("-n", "--name", type=str, default=None, required=True,
            help="CBOR data name (required)")
    data_cmd.add_argument("-v", "--value", type=str, default=None, required=False,
            help="CBOR data value (required for put)")

    args = parser.parse_args()
    if args.command == 'check':
        ret = check_device_exists(args.bus, int(args.address, 0))
        if ret:
            print("Device detected")
            sys.exit(0)
        else:
            print("Device not detected")
            sys.exit(1)
    elif args.command == 'file':
        eeprom = CBOR_EEPROM(args.type, args.bus, int(args.address, 0))
        if args.file_cmd == 'read':
            print(eeprom.read_file())
        elif args.file_cmd == 'erase':
            eeprom.erase_file()
        elif args.file_cmd == 'write':
            if args.file is None:
                sys.stderr.write("File path missing (use -f/--file)\n")
                sys.exit(1)
            with open(args.file, 'r') as f:
                s = f.read()
                d = ast.literal_eval(s)
                if isinstance(d, dict):
                    eeprom.write_file(d)
                    print("File stored")
                else:
                    raise ValueError("File contents must be dictionary")
    elif args.command == 'data':
        eeprom = CBOR_EEPROM(args.type, args.bus, int(args.address, 0))
        if args.data_cmd == 'get':
            print(eeprom.get(args.name))
        elif args.data_cmd == 'put':
            if args.value is None:
                sys.stderr.write("Value missing (use -v/--value)\n")
                sys.exit(1)
            eeprom.put(args.name, args.value)

if __name__ == '__main__':
    main()
