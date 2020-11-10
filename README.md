# python-eeprom

`python-eeprom` is a pure Python 3 library for initializing, reading, and writing
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

eeprom.write(test_string.encode())
verify = eeprom.read(test_length).decode()

print(verify)

assert verify == test_string
```

Using CBOR EEPROM class:

```python3
from eeprom import CBOR_EEPROM

eeprom = CBOR_EEPROM("24c64", 0, 0x50)

# Write sample data file
test_data = { 'some_key' : "This is a sample value." }
eeprom.write_file(test_data)

# Re-initialize to clear cached file
del eeprom
eeprom = CBOR_EEPROM("24c64", 0, 0x50)

# Read data file
verify_data = eeprom.read_file()
print(verify_data)
assert verify_data == test_data

# Re-initialize to clear cached file
del eeprom
eeprom = CBOR_EEPROM("24c64", 0, 0x54)

# Read data object
val = eeprom.get('some_key')
print(val)
assert val == test_data['some_key']

# Erase data file
eeprom.erase_file()
erased = eeprom.read_file()
print(erased)
assert erased == {}
```

## Documentation

Coming soon.

## License

python-eeprom is MIT licensed. See the included [LICENSE](LICENSE) file.
