# python-eeprom

python-eeprom is a pure Python 3 library for initializing, reading, and writing
EEPROM devices in userspace Linux. It is useful in embedded Linux environments,
including custom hardware based platforms. python-eeprom also includes a
wrapper class for managing storage and retrieval of CBOR files in EEPROM (using
'cbor' library). python-eeprom is MIT licensed.

## Installing

Install using pip:

```
pip install eeprom
```

Install using easy_install:

```
easy_install eeprom
```

Install using setup.py:

```
python setup.py install
```

## Examples

Using the EEPROM class directly:

```python3
from eeprom import EEPROM

eeprom = EEPROM("24c64", 0, 0x50)

test_string = "This is a string of test data."
test_length = len(test_string)

eeprom.write(bytes(test_string))
verify = eeprom.read(test_length)

assert str(verify) == test_string
```

## Documentation

Coming soon.

## License

python-periphery is MIT licensed. See the included [LICENSE](LICENSE) file.
