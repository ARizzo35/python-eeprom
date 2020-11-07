#!/usr/bin/env python3

import os
from eeprom.device_types import EEPROM_TYPES
from eeprom.util import check_device_exists

SYSFS_I2C_DEVICES_DIR = os.environ.get("SYSFS_I2C_DEVICES_DIR", "/sys/bus/i2c/devices")


class EEPROMError(IOError):
    pass

class EEPROM():

    _eeprom_fd = None
    _busdir = None
    _devdir = None

    @property
    def name(self):
        if getattr(self, '_name', None) is None:
            self._name = f"{self._bus}-{self._addr:04x}"
        return self._name

    def __init__(self, dev_type, i2c_bus, i2c_addr):
        # Check device type
        if not isinstance(dev_type, str) or dev_type not in EEPROM_TYPES.keys():
            raise ValueError(f"Invalid dev_type: {dev_type}")
        self._type = dev_type
        self._size = EEPROM_TYPES[dev_type]
        # Check I2C bus
        self._busdir = os.path.join(SYSFS_I2C_DEVICES_DIR, f"i2c-{i2c_bus}")
        if not isinstance(i2c_bus, int) or not os.path.isdir(self._busdir):
            raise ValueError(f"Invalid i2c_bus: {i2c_bus}")
        self._bus = i2c_bus
        # Check I2C address
        if not isinstance(i2c_addr, int) or not check_device_exists(i2c_bus, i2c_addr):
            raise ValueError(f"Invalid i2c_addr: {i2c_addr}")
        self._addr = i2c_addr
        # Open device
        self.open()

    def __del__(self):
        self.close()

    def __enter__(self):
        return self

    def __exit__(self, t, value, traceback):
        self.close()

    def _create_device(self):
        try:
            with open(os.path.join(self._busdir, "new_device"), 'w') as f:
                f.write(f"{self._type} {self._addr}\n")
        except IOError as e:
            raise EEPROMError(e.errno, f"Creating Device: {e.strerror}")

    def _delete_device(self):
        if self._devdir and os.path.isdir(self._devdir):
            try:
                fd = os.open(os.path.join(self._busdir, "delete_device"), os.O_WRONLY)
                os.write(fd, f"{self._addr}\n".encode())
                os.close(fd)
            except OSError as e:
                raise EEPROMError(e.errno, f"Deleting Device: {e.strerror}")

    def open(self):
        if self._devdir is None:
            self._devdir = os.path.join(SYSFS_I2C_DEVICES_DIR, self.name)
        if not os.path.isdir(self._devdir):
            self._create_device()
        if not os.path.isfile(os.path.join(self._devdir, 'eeprom')):
            raise EEPROMError("Error creating device, eeprom file not found")
        try:
            self._eeprom_fd = os.open(os.path.join(self._devdir, 'eeprom'), os.O_RDWR)
        except OSError as e:
            raise EEPROMError(e.errno, f"Opening EEPROM: {e.strerror}")

    def close(self):
        if self._eeprom_fd:
            os.close(self._eeprom_fd)
        self._delete_device()

    def read(self, size, addr=0):
        if (size + addr) > self._size:
            raise EEPROMError(f"Cannot read {size} bytes @ address 0x{addr:x} (EEPROM Size: {self._size})")
        try:
            os.lseek(self._eeprom_fd, addr, os.SEEK_SET)
            data = b''
            while len(data) < size:
                data += os.read(self._eeprom_fd, size - len(data))
        except OSError as e:
            raise EEPROMError(e.errno, f"EEPROM Read: {e.strerror}")
        return data

    def write(self, data, addr=0):
        size = len(data)
        if (size + addr) > self._size:
            raise EEPROMError(f"Cannot write {size} bytes @ address 0x{addr:08x} (EEPROM Size: {self._size})")
        try:
            os.lseek(self._eeprom_fd, addr, os.SEEK_SET)
            written = 0
            while written < size:
                written += os.write(self._eeprom_fd, data[written:])
        except OSError as e:
            raise EEPROMError(e.errno, f"EERPOM Write: {e.strterror}")
        return written

